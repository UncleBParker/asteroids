import pygame
import math

def point_in_triangle(p, tri):
    p = pygame.Vector2(p)
    a, b, c = [pygame.Vector2(v) for v in tri]

    v0 = c - a
    v1 = b - a
    v2 = p - a

    dot00 = v0.dot(v0)
    dot01 = v0.dot(v1)
    dot02 = v0.dot(v2)
    dot11 = v1.dot(v1)
    dot12 = v1.dot(v2)

    denom = dot00 * dot11 - dot01 * dot01
    if denom == 0:
        return False

    inv_denom = 1.0 / denom
    u = (dot11 * dot02 - dot01 * dot12) * inv_denom
    v = (dot00 * dot12 - dot01 * dot02) * inv_denom

    return (u >= 0) and (v >= 0) and (u + v <= 1)

def point_segment_distance(p, a, b):
    p = pygame.Vector2(p)
    a = pygame.Vector2(a)
    b = pygame.Vector2(b)

    ab = b - a
    ab_len2 = ab.length_squared()
    if ab_len2 == 0:
        return p.distance_to(a)

    t = max(0, min(1, (p - a).dot(ab) / ab_len2))
    proj = a + t * ab
    return p.distance_to(proj)

def triangle_circle_collision(tri, center, radius):
    center = pygame.Vector2(center)

    if point_in_triangle(center, tri):
        return True

    for i in range(3):
        a = tri[i]
        b = tri[(i + 1) % 3]
        if point_segment_distance(center, a, b) <= radius:
            return True

    return False

def score(asteroids_destroyed):
    return (
        asteroids_destroyed[1] * 100 +
        asteroids_destroyed[2] * 50 +
        asteroids_destroyed[3] * 10
    )

def scoreboard(asteroids_destroyed): #for print statements
    return f"Asteroids Destroyed: \n{asteroids_destroyed[1]} Small\n{asteroids_destroyed[2]} Medium\n{asteroids_destroyed[3]} Large\nFinal Score: {score(asteroids_destroyed)}"