import pygame
import random
from player import Player
from logger import log_state, log_event
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from game import Game
from gamestate import GameState
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
from shipfragment import ShipFragment, spawn_ship_fragments
from combat import handle_player_hit
from debugmanager import DebugManager
from screenflash import ScreenFlash
from pausemenu import PauseMenu
from highscore import HighScoreManager
from highscorescreen import HighScoreScreen
from nameentryscreen import NameEntryScreen
from gameoverscreen import GameOverScreen
from settingsmanager import SettingsManager
from optionsscreen import OptionsScreen
from titlemenu import TitleMenu
from menustate import MenuState
from soundmanager import SoundManager
from inputmanager import InputManager
from constants import (
    SCREEN_WIDTH, 
    SCREEN_HEIGHT, 
    MIN_STAR_COUNT, 
    MAX_STAR_COUNT,
    UFO_SCORE_VALUE,
    SCREEN_FLASH_DURATION_SECONDS,
    BOMB_SPAWN_PAUSE_SECONDS,
    PLAYER_TURN_SPEED_STEP,
    GAME_OVER_SOUND_DELAY_SECONDS
)


def run_title_menu(screen, clock, high_scores, settings, sound_manager, input_manager):
    title_menu = TitleMenu()
    starfield = StarField(SCREEN_WIDTH, SCREEN_HEIGHT, MIN_STAR_COUNT, MAX_STAR_COUNT)
    high_score_screen = HighScoreScreen()
    options_screen = OptionsScreen()
    current_state = MenuState.TITLE

    dt = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            pause_requested = input_manager.is_pause_pressed(event)

            if pause_requested:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if current_state == MenuState.OPTIONS:
                            sound_manager.play("menu_back")

                            if options_screen.confirming_clear:
                                options_screen.cancel_clear_confirmation()
                            else:
                                current_state = MenuState.TITLE

                            continue

                        elif current_state == MenuState.HIGH_SCORES:
                            sound_manager.play("menu_back")
                            current_state = MenuState.TITLE
                            continue

            if current_state == MenuState.TITLE:
                previous_index = title_menu.selected_index
                action = title_menu.handle_event(event, input_manager)

                if title_menu.selected_index != previous_index:
                    sound_manager.play("menu_option_change")

                if action == "Start Game":
                    sound_manager.play("menu_forward")
                    return "start"

                elif action == "High Scores":
                    sound_manager.play("menu_forward")
                    current_state = MenuState.HIGH_SCORES

                elif action == "Options":
                    sound_manager.play("menu_forward")
                    current_state = MenuState.OPTIONS

                elif action == "Quit":
                    return "quit"

            elif current_state == MenuState.OPTIONS:
                previous_index = options_screen.selected_index
                previous_confirmation = options_screen.confirmation_selected

                action = options_screen.handle_event(event, input_manager)

                if (
                    options_screen.selected_index != previous_index
                    or options_screen.confirmation_selected
                    != previous_confirmation
                ):
                    sound_manager.play("menu_option_change")

                if (isinstance(action, tuple) and action[0] == "Set Rotation"):
                    settings.set_player_turn_speed(action[1])

                elif action == "Decrease Rotation":
                    settings.set_player_turn_speed(settings.player_turn_speed - PLAYER_TURN_SPEED_STEP)

                elif action == "Increase Rotation":
                    settings.set_player_turn_speed(settings.player_turn_speed + PLAYER_TURN_SPEED_STEP)

                elif action == "Clear High Scores":
                    options_screen.open_clear_confirmation()

                elif action == "Confirm Clear":
                    high_scores.clear()

                elif action == "Back":
                    sound_manager.play("menu_back")
                    current_state = MenuState.TITLE

            elif current_state == MenuState.HIGH_SCORES:
                action = high_score_screen.handle_event(event, input_manager)

                if action == "Back":
                    sound_manager.play("menu_back")
                    current_state = MenuState.TITLE

            

        starfield.update(dt)

        screen.fill("black")
        starfield.draw(screen)
        if current_state == MenuState.TITLE:
            title_menu.draw(screen)

        elif current_state == MenuState.HIGH_SCORES:
            high_score_screen.draw(screen, high_scores.entries)

        elif current_state == MenuState.OPTIONS:
            options_screen.draw(screen, settings)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


def run_game(screen, clock, high_scores, settings, sound_manager, input_manager):
    dt = 0.0
    game_over_sound_timer = None

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
    UFOBullet.containers = (ufo_bullets, drawable, updatable)
    ShipFragment.containers = (drawable, updatable)
    ScreenFlash.containers = (updatable, drawable)

    game = Game()
    asteroid_field = AsteroidField(asteroids, game)
    pickup_spawner = PickupSpawner(sound_manager)
    debug_instance = DebugManager()
    pause_menu = PauseMenu()
    high_score_screen = HighScoreScreen()
    name_entry_screen = NameEntryScreen()
    game_over_screen = GameOverScreen()
    options_screen = OptionsScreen()

    text_font = pygame.font.Font(None, 36)

    input_manager.suppress_shooting_until_released()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, sound_manager, input_manager)
    player.turn_speed = settings.player_turn_speed
    triangle_points = player.triangle()
    starfield = StarField(SCREEN_WIDTH, SCREEN_HEIGHT, MIN_STAR_COUNT, MAX_STAR_COUNT)
    ufo_spawner = UFOSpawner(player, ufos, game, sound_manager)


    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if game.state == GameState.NAME_ENTRY:
                submitted_name = name_entry_screen.handle_event(
                    event,
                    input_manager,
                )

                if submitted_name is not None:
                    high_scores.add_score(submitted_name, game.score)
                    name_entry_screen.stop()
                    game.finish_name_entry()

                continue

            pause_requested = input_manager.is_pause_pressed(event)

            if pause_requested:
                if game.state == GameState.HIGH_SCORES:
                    sound_manager.play("menu_back")
                    game.close_high_scores()

                elif game.state == GameState.OPTIONS:
                    sound_manager.play("menu_back")

                    if options_screen.confirming_clear:
                        options_screen.cancel_clear_confirmation()
                    else:
                        game.close_options()

                else:
                    if game.state == GameState.PLAYING:
                        player.stop_engine_sound()
                        sound_manager.play("pause_game")

                    elif game.state == GameState.PAUSED:
                        sound_manager.play("menu_back")

                    input_manager.suppress_shooting_until_released()
                    game.toggle_pause()

                continue

            if game.state == GameState.HIGH_SCORES:
                high_score_action = high_score_screen.handle_event(event, input_manager)

                if high_score_action == "Back":
                    sound_manager.play("menu_back")
                    game.close_high_scores()

                continue


            if game.state == GameState.OPTIONS:
                previous_index = options_screen.selected_index
                previous_confirmation = options_screen.confirmation_selected

                options_action = options_screen.handle_event(event, input_manager)

                if (
                    options_screen.selected_index != previous_index
                    or options_screen.confirmation_selected != previous_confirmation
                ):
                    sound_manager.play("menu_option_change")

                if (
                    isinstance(options_action, tuple)
                    and options_action[0] == "Set Rotation"
                ):
                    settings.set_player_turn_speed(options_action[1])
                    player.turn_speed = settings.player_turn_speed

                elif options_action == "Decrease Rotation":
                    settings.set_player_turn_speed(
                        settings.player_turn_speed
                        - PLAYER_TURN_SPEED_STEP
                    )
                    player.turn_speed = settings.player_turn_speed

                elif options_action == "Increase Rotation":
                    settings.set_player_turn_speed(
                        settings.player_turn_speed
                        + PLAYER_TURN_SPEED_STEP
                    )
                    player.turn_speed = settings.player_turn_speed

                elif options_action == "Clear High Scores":
                    options_screen.open_clear_confirmation()

                elif options_action == "Confirm Clear":
                    high_scores.clear()

                elif options_action == "Back":
                    sound_manager.play("menu_back")
                    game.close_options()

                continue


            if game.state == GameState.GAME_OVER:
                game_over_action = game_over_screen.handle_event(event, input_manager)

                if game_over_action == "Restart":
                    return "restart"

                elif game_over_action == "High Scores":
                    game.open_high_scores()

                elif game_over_action == "Quit":
                    return "quit"

                continue

            if game.state == GameState.PAUSED:
                previous_index = pause_menu.selected_index
                pause_action = pause_menu.handle_event(event, input_manager)

                if pause_menu.selected_index != previous_index:
                    sound_manager.play("menu_option_change")

                if pause_action == "Resume":
                    sound_manager.play("menu_back")
                    input_manager.suppress_shooting_until_released()
                    game.resume()

                elif pause_action == "Restart":
                    sound_manager.play("menu_forward")
                    return "restart"

                elif pause_action == "High Scores":
                    sound_manager.play("menu_forward")
                    game.open_high_scores()

                elif pause_action == "Options":
                    sound_manager.play("menu_forward")
                    game.open_options()

                elif pause_action == "Quit to Menu":
                    sound_manager.play("menu_back")
                    return "menu"

                elif pause_action == "Quit Program":
                    return "quit"

                continue

            bomb_requested = input_manager.is_bomb_pressed(event)

            if bomb_requested:
                if player.consume_bomb():
                    sound_manager.play("bomb_used")
                    for target in bomb_targets:
                        particle_number = random.randint(6, 24)

                        for _ in range(particle_number):
                            ExplosionParticle(target.position.x, target.position.y)

                        target.kill()

                    ScreenFlash(SCREEN_FLASH_DURATION_SECONDS)
                    asteroid_field.pause_spawning(BOMB_SPAWN_PAUSE_SECONDS)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    debug_instance.toggle()

                debug_instance.handle_event(
                    event,
                    player,
                    asteroid_field,
                    pickup_spawner,
                    ufo_spawner,
                )

        
        fps = clock.get_fps()
        screen.fill("black")

        
        if game.state == GameState.PLAYING:
            game.update(dt)
            starfield.update(dt)
            updatable.update(dt)

        elif game.state == GameState.OPTIONS:
            options_screen.draw(screen, settings)

        if game.state == GameState.PLAYING:
            for pickup in pickups:
                if circle_collides_with_polygon(pickup.position, pickup.radius, player.triangle()):
                    pickup.collect(player)


            for ufo_bullet in ufo_bullets:
                if circle_collides_with_polygon(ufo_bullet.position, ufo_bullet.radius, player.triangle()):
                    ufo_bullet.kill()
                    handle_player_hit(player, "ufo_hit_player")

            
            for asteroid in asteroids:
                if polygons_collide(player.triangle(), asteroid.world_vertices()):
                    handle_player_hit(player, "player_hit")
                        

            if player.lives == 0:
                game_over_sound_timer = GAME_OVER_SOUND_DELAY_SECONDS
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

                score_qualifies = high_scores.qualifies(game.score)
                game.end_game(score_qualifies)

                if game.state == GameState.NAME_ENTRY:
                    name_entry_screen.start()

            
            for asteroid in asteroids:
                for shot in shots:
                    if circle_collides_with_polygon(shot.position, shot.radius, asteroid.world_vertices()):
                        sound_manager.play("asteroid_death")
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
                        sound_manager.play("ufo_death")
                        game.score += UFO_SCORE_VALUE
                        log_event("ufo_hit")
                        particle_number = random.randint(12, 36)

                        for _ in range(particle_number):
                            ExplosionParticle(ufo.position.x, ufo.position.y)

                        ufo.kill()
                        shot.kill()

                        break

        
        if game_over_sound_timer is not None:
            game_over_sound_timer -= dt

            if game_over_sound_timer <= 0:
                sound_manager.play("game_over")
                game_over_sound_timer = None


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

        debug_counts = {
            "Asteroids": len(asteroids),
            "Shots": len(shots),
            "Pickups": len(pickups),
            "UFOs": len(ufos),
            "UFO bullets": len(ufo_bullets),
            "Drawables": len(drawable),
            "Invunerable": player.debug_invulnerability,
            "Asteroid spawning paused": asteroid_field.spawning_paused,
            "Difficulty": game.difficulty_level,
            "Asteroid spawn rate": f"{asteroid_field.get_current_spawn_rate():.2f}",
            "Asteroid cap": asteroid_field.get_current_cap(),
            "UFO cap": ufo_spawner.get_current_cap()
        }

        debug_instance.draw(screen, fps, debug_counts)

        if game.state == GameState.PAUSED:
            pause_menu.draw(screen)

        elif game.state == GameState.HIGH_SCORES:
            high_score_screen.draw(screen, high_scores.entries)

        elif game.state == GameState.OPTIONS:
            options_screen.draw(screen, settings)

        elif game.state == GameState.NAME_ENTRY:
            name_entry_screen.draw(screen, game.score, input_manager)

        elif game.state == GameState.GAME_OVER:
            game_over_screen.draw(screen, game.score, game.score_qualified)

        pygame.display.flip()


        dt = clock.tick(60) / 1000


        pygame.display.set_caption(f"Modernsteroids!")


def main():
    pygame.mixer.pre_init(frequency=48000, size=-16, channels=2, buffer=256)
    pygame.init()
    pygame.mixer.set_num_channels(32)
    input_manager = InputManager()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    high_scores = HighScoreManager()
    settings = SettingsManager()
    sound_manager = SoundManager()

    print(f"Starting Asteroids with pygame version {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    while True:
        title_action = run_title_menu(screen, clock, high_scores, settings, sound_manager, input_manager)

        if title_action == "quit":
            break

        while True:
            session_action = run_game(
                screen,
                clock,
                high_scores,
                settings,
                sound_manager,
                input_manager
            )

            if session_action == "restart":
                continue

            break

        if session_action == "quit":
            break

    pygame.quit()


if __name__ == "__main__":
    main()