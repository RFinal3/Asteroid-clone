import pygame
import sys
from constants import *
from player import *
from logger import *
from asteroidfield import *
from shot import *
from player import *
from game import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0

    print(f"Starting Asteroids with pygame version {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, drawable, updatable)
    asteroid_field = AsteroidField()
    game = Game()

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        updatable.update(dt)
        
        for obj in asteroids:
            if player.invulnerability_timer <= 0 and obj.collides_with(player):
                log_event("player_hit")
                player.lives -= 1
                player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                player.velocity = pygame.Vector2(0, 0)
                player.invulnerability_timer = 1


            if player.lives == 0:
                print("Game over!")
                sys.exit()

        
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    game.score += 1
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()


        for obj in drawable:
            obj.draw(screen)


        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
