import pygame
import sys
import random
from constants import (
    SCREEN_WIDTH, 
    SCREEN_HEIGHT, 
    MIN_STAR_COUNT, 
    MAX_STAR_COUNT,
    UFO_SCORE_VALUE
)
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
from speedpickup import SpeedPickup
from bombpickup import BombPickup
from pickup_spawner import PickupSpawner
from ufo import UFO
from ufospawner import UFOSpawner
from ufobullet import UFOBullet


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
    bomb_targets = pygame.sprite.Group()
    ufos = pygame.sprite.Group()
    ufo_bullets = pygame.sprite.Group()

    PickupSpawner.containers = (updatable,)
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, bomb_targets, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, drawable, updatable)
    ExplosionParticle.containers = (explosionparticles, updatable, drawable)
    Pickup.containers = (pickups, drawable, updatable)
    UFO.containers = (ufos, bomb_targets, drawable, updatable)
    UFOSpawner.containers = (updatable,)
    UFOBullet.containers = (ufo_bullets, drawable, updatable)

    asteroid_field = AsteroidField(asteroids)
    pickup_spawner = PickupSpawner()

    game = Game()
    text_font = pygame.font.Font(None, 36)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    starfield = StarField(SCREEN_WIDTH, SCREEN_HEIGHT, MIN_STAR_COUNT, MAX_STAR_COUNT)
    ufo_spawner = UFOSpawner(player, ufos)


    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_b:
                    if player.consume_bomb():
                        for target in bomb_targets:
                            particle_number = random.randint(6, 24)
                    
                            for _ in range(particle_number):
                                ExplosionParticle(target.position.x, target.position.y)
                            
                            target.kill()

        
        fps = clock.get_fps()


        screen.fill("black")
        starfield.update(dt)
        updatable.update(dt)

        for pickup in pickups:
            if circle_collides_with_polygon(pickup.position, pickup.radius, player.triangle()):
                pickup.collect(player)


        for ufo_bullet in ufo_bullets:
            if circle_collides_with_polygon(ufo_bullet.position, ufo_bullet.radius, player.triangle()):
                ufo_bullet.kill()
                if player.take_damage():
                    log_event("ufo_hit_player")

        
        for asteroid in asteroids:
            if polygons_collide(player.triangle(), asteroid.world_vertices()):
                if player.take_damage():
                    log_event("player_hit")


            if player.lives == 0:
                print(f"Game over! Final score: {game.score}")
                
                if game.score <= 10:
                    print("ROFL.")
                
                elif game.score <= 25:
                    print("LOL.")

                elif game.score <= 50:
                    print("Okay.")

                elif game.score <= 100:
                    print("Okurt.")

                elif game.score <= 200:
                    print("Okkkkuuurrrrttt.")

                elif game.score <= 300:
                    print("Bro.")

                elif game.score <= 400:
                    print("Chill bro.")

                elif game.score <= 500:
                    print("Gyatt.")

                elif game.score <= 600:
                    print("Gyatt damn.")

                elif game.score <= 700:
                    print("Are you cheating bro?")

                elif game.score <= 800:
                    print("Someone check this dudes screen while he plays, I think he's cheating.")

                elif game.score <= 900:
                    print("So, you watched and it looks legit?")

                elif game.score <= 1000:
                    print("Yeah, definitely cheating.")

                else:
                    print("Okay, checking the logs now.")

                sys.exit()

        
        for asteroid in asteroids:
            for shot in shots:
                if circle_collides_with_polygon(shot.position, shot.radius, asteroid.world_vertices()):
                    game.score += 1
                    log_event("asteroid_shot")
                    pickup_spawner.try_spawn(asteroid.position)
                    ufo_spawner.try_spawn()
                    particle_number = random.randint(6, 24)
                    
                    for _ in range(particle_number):
                        ExplosionParticle(asteroid.position.x, asteroid.position.y)

                    asteroid.split()
                    shot.kill()

                    break

        
        for ufo in ufos:
            for shot in shots:
                if circle_collides_with_polygon(shot.position, shot.radius, ufo.world_vertices()):
                    game.score += UFO_SCORE_VALUE
                    log_event("ufo_hit")
                    particle_number = random.randint(12, 36)

                    for _ in range(particle_number):
                        ExplosionParticle(ufo.position.x, ufo.position.y)

                    ufo.kill()
                    shot.kill()

                    break


        starfield.draw(screen)
                    

        for obj in drawable:
            obj.draw(screen)
        
        score_text = text_font.render(f"Score: {game.score}", True, "white")
        lives_text = text_font.render(f"Lives: {player.lives}", True, "white")
        shield_text = text_font.render(f"Shields: {player.shield_count}", True, "white")
        bombs_text = text_font.render(f"Bombs: {player.bomb_count}", True, "white")

        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (20, 60))
        screen.blit(shield_text, (20, 100))
        screen.blit(bombs_text, (20, 140))


        pygame.display.flip()

        dt = clock.tick(60) / 1000

        pygame.display.set_caption(
            f"Modernsteroids! | FPS: {clock.get_fps():.2f} | "
            f"A: {len(asteroids)} | S: {len(shots)} | "
            f"P: {len(pickups)} | D: {len(drawable)}"
        )

if __name__ == "__main__":
    main()