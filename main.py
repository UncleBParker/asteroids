# main.py:
import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from hud import HUD


def main():
    
    debug = "--debug" in sys.argv

    print(f"------------------------------------------------------------")
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    print(f"------------------------------------------------------------")

    # innitialize pygame and set variables used later
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    dt = 0

    # innitialize pygame.sprinte groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # add classes to group containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    HUD.containers = (drawable)

    # innitialize instances of static classes
    asteroidfield = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    hud = HUD(font)
    
    # start game loop
    while True:
        log_state()

        # check for force quit from user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(f"Game quit. \n{hud.scoreboard()}")
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print(f"Game quit. \n{hud.scoreboard()}")
                return
    
        # fill screenspace with black background
        screen.fill("black")
        updatable.update(dt)

        # check if player or asteroids left screen and wrap them to other side
        player.wrap_around_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
        for asteroid in asteroids:
            asteroid.wrap_around_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        # start checking for game element collisions
        for asteroid in asteroids:
            
            # handle player/asteroid collisions
            if player.collides_with(asteroid):
                log_event("player_hit")
                hud.lives -= 1

                # option to continue playing if lives > 0
                if hud.lives <= 0:
                    print(f"Game over! \n{hud.scoreboard()}")
                    sys.exit()
                else:
                    waiting = True
                    space_down = False
                    while waiting:
                        for event in pygame.event.get():
                            # option to quit during "continue?" pause
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    print(f"Game quit. \n{hud.scoreboard()}")
                                    sys.exit()
                                # look for space key press
                                if event.key == pygame.K_SPACE:
                                    space_down = True
                            # stop waiting loop when space key is released
                            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and space_down:
                                waiting = False

                        # darken / clear screen for the prompt
                        screen.fill("black")
                        # redraw HUD so player sees current lives/score
                        hud.draw(screen)
                        # draw "Continue?" message
                        msg_surf = font.render(f"{hud.lives}/3 Lives Continue?", True, (255, 255, 255))
                        msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                        screen.blit(msg_surf, msg_rect)

                        # update display and clock
                        pygame.display.flip()
                        clock.tick(60)

                    # reset player
                    player.position.update(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.rotation = 0
                    player.shot_cooldown_timer = 0

                    # clear asteroids and shots
                    for asteroid in list(asteroids):
                        asteroid.kill()
                    for shot in list(shots):
                        shot.kill()

                    # reset spawn timer so a new field starts fresh
                    asteroidfield.spawn_timer = 0.0

            # handle shot/asteroid collisions
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    hud.asteroids_destroyed[asteroid.kind] += 1

        # handle asteroid/asteroid collisions:
        asteroid_list = list(asteroids)
        for i in range(len(asteroid_list)):
            a = asteroid_list[i]
            for j in range(i + 1, len(asteroid_list)):
                b = asteroid_list[j]
                # skip if they’re in each other’s ignore sets
                if (b in a.ignore_collisions_with) or (a in b.ignore_collisions_with):
                    continue
                # collide if not in each other's ignore sets
                if a.collides_with(b):
                    a.split()
                    b.split()

        # clear ignore flags after split asteriods stop overlapping
        for a in asteroids:
            for other in list(a.ignore_collisions_with):
                # if other died or they no longer overlap, stop ignoring
                if (not other.alive()) or (not a.collides_with(other)):
                    a.ignore_collisions_with.remove(other)

        # --- debug: draw lines between asteroids that are ignoring collisions ---
        if debug:
            debug_color = (0, 255, 0)  # bright green

            for a in asteroids:
                for other in a.ignore_collisions_with:
                    # Only draw one line per pair (avoid duplicates)
                    if id(a) < id(other):
                        pygame.draw.line(
                            screen,
                            debug_color,
                            a.position,
                            other.position,
                            1,  # line width
                        )

        # draw all drawable objects
        for each in drawable:
            each.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()