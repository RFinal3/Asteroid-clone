from gamestate import GameState
from constants import (
    STARTING_SCORE, 
    ASTEROID_MAX_SCALING_LEVEL, 
    DIFFICULTY_INCREASE_INTERVAL_SECONDS
    )

class Game:
    def __init__(self):
        self.score = STARTING_SCORE
        self.elapsed_time = 0.0
        self.difficulty_level = 1
        self.state = GameState.PLAYING

    
    def update(self, dt):
        self.elapsed_time += dt

        completed_intervals = int(self.elapsed_time // DIFFICULTY_INCREASE_INTERVAL_SECONDS)
        
        self.difficulty_level = min(completed_intervals + 1, ASTEROID_MAX_SCALING_LEVEL)

    
    def pause(self):
        self.state = GameState.PAUSED


    def resume(self):
        self.state = GameState.PLAYING


    def toggle_pause(self):
        if self.state == GameState.PLAYING:
            self.pause()
        elif self.state == GameState.PAUSED:
            self.resume()