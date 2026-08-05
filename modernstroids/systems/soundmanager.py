import pygame

from modernstroids.resources import get_asset_path


class SoundManager:
    def __init__(self):
        self.sound_directory = get_asset_path("sounds")

        self.sounds = {}

        sound_files = {
            "asteroid_death": "asteroid_death.wav",
            "bomb_collected": "bomb_collected.wav",
            "bomb_used": "bomb_used.wav",
            "game_over": "game_over_sound.wav",
            "menu_back": "menu_back_sound.wav",
            "menu_forward": "menu_forward_sound.wav",
            "menu_option_change": "menu_option_change_sound.wav",
            "pause_game": "pause_game_sound.wav",
            "pickup_spawn": "pickup_spawn.wav",
            "shield_collected": "shield_collected.wav",
            "shield_consumed": "shield_consumed.wav",
            "ship_destruction": "ship_destruction.wav",
            "ship_engine": "ship_engine.wav",
            "ship_shot": "ship_shot.wav",
            "speed_boost_collected": "speed_boost_collected.wav",
            "ufo_death": "ufo_death.wav",
            "ufo_shot": "ufo_shot.wav",
            "ufo_spawn": "ufo_spawn.wav",
        }

        for name, filename in sound_files.items():
            file_path = self.sound_directory / filename
            self.sounds[name] = pygame.mixer.Sound(str(file_path))

    def play(self, name, loops=0):
        return self.sounds[name].play(loops=loops)

    def stop(self, name):
        self.sounds[name].stop()
