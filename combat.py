from logger import log_event
from shipfragment import spawn_ship_fragments

def handle_player_hit(player, event_name):
    lives_before_damage = player.lives
    triangle_before_damage = player.triangle()
    position_before_damage = player.position.copy()
    result = player.take_damage()

    if not result:
        return False

    log_event(event_name)

    if player.lives < lives_before_damage:
        spawn_ship_fragments(triangle_before_damage, position_before_damage)
        
    return True