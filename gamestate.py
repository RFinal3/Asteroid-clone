from enum import Enum, auto

class GameState(Enum):
    PLAYING = auto()
    PAUSED = auto()
    HIGH_SCORES = auto()
    GAME_OVER = auto()
    NAME_ENTRY = auto()