import pygame
import sys
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MIN_STAR_COUNT, MAX_STAR_COUNT
from player import Player
from logger import log_state, log_event
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from game import Game
from explosionparticle import ExplosionParticle
from starfield import StarField
from utils import circle_collides_with_polygon, polygons_collide
from pickup import Pickup
from shieldpickup import ShieldPickup


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0

    print(f"Starting Asteroids with pygame version {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.LayeredUpdates()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosionparticles = pygame.sprite.Group()
    pickups = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, drawable, updatable)
    ExplosionParticle.containers = (explosionparticles, updatable, drawable)
    Pickup.containers = (pickups, drawable)

    asteroid_field = AsteroidField()

    game = Game()
    text_font = pygame.font.Font(None, 36)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    starfield = StarField(SCREEN_WIDTH, SCREEN_HEIGHT, MIN_STAR_COUNT, MAX_STAR_COUNT)

    shield_pickup = ShieldPickup(
        SCREEN_WIDTH * 0.75,
        SCREEN_HEIGHT / 2,
    )


    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        starfield.update(dt)
        updatable.update(dt)

        for pickup in pickups:
            if circle_collides_with_polygon(pickup.position, pickup.radius, player.triangle()):
                pickup.collect(player)

        
        for asteroid in asteroids:
            if polygons_collide(player.triangle(), asteroid.world_vertices()):
                if player.take_damage():
                    log_event("player_hit")


            if player.lives == 0:
                print("Game over!")
                sys.exit()

        
        for asteroid in asteroids:
            for shot in shots:
                if circle_collides_with_polygon(shot.position, shot.radius, asteroid.world_vertices()):
                    game.score += 1
                    log_event("asteroid_shot")
                    particle_number = random.randint(6, 24)
                    
                    for _ in range(particle_number):
                        ExplosionParticle(asteroid.position.x, asteroid.position.y)

                    asteroid.split()
                    shot.kill()


        starfield.draw(screen)
                    

        for obj in drawable:
            obj.draw(screen)
        
        score_text = text_font.render(f"Score: {game.score}", True, "white")
        lives_text = text_font.render(f"Lives: {player.lives}", True, "white")

        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (20, 60))


        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()