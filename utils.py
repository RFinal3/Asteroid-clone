from constants import *

def wrap_position(position, radius):
    if position.x > SCREEN_WIDTH + radius:
        position.x = -radius

    elif position.x < -radius:
        position.x = SCREEN_WIDTH + radius

    if position.y > SCREEN_HEIGHT + radius:
        position.y = -radius
        
    elif position.y < -radius:
        position.y = SCREEN_HEIGHT + radius
