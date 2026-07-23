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
        self.previous_state = None
        self.score_qualified = False

    
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


    def open_high_scores(self):
        self.previous_state = self.state
        self.state = GameState.HIGH_SCORES


    def close_high_scores(self):
        self.state = self.previous_state
        self.previous_state = None


    def end_game(self, score_qualifies):
        self.score_qualified = score_qualifies

        if score_qualifies:
            self.state = GameState.NAME_ENTRY
        else:
            self.state = GameState.GAME_OVER


    def finish_name_entry(self):
        self.state = GameState.GAME_OVER
        self.open_high_scores()