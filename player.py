import pygame
from circleshape import CircleShape
from shot import Shot
from utils import wrap_position
from constants import (
    PLAYER_RADIUS, 
    PLAYER_STARTING_LIVES, 
    PLAYER_MAX_SPEED, 
    LINE_WIDTH, 
    PLAYER_TURN_SPEED, 
    PLAYER_ACCELERATION,
    PLAYER_DECELERATION, 
    PLAYER_SHOOT_COOLDOWN_SECONDS, 
    PLAYER_SHOOT_SPEED,
    LAYER_PLAYER,
    PLAYER_INVULNERABILITY_SECONDS,
    SPEED_BOOST_MULTIPLIER,
    SPEED_BOOST_DURATION_SECONDS,
    PLAYER_RESPAWN_DELAY_SECONDS,
    SHIP_FRAGMENT_LIFETIME_SECONDS,
    SHIP_ENGINE_MAX_VOLUME,
    SHIP_ENGINE_VOLUME_CHANGE_PER_SECOND,
    SHIP_ENGINE_STOP_FADE_MS,
    CONTROLLER_DEADZONE
    )

class Player(CircleShape):
    _layer = LAYER_PLAYER

    
    def __init__(self, x, y, sound_manager, game_controller):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.lives = PLAYER_STARTING_LIVES
        self.invulnerability_timer = 0
        self.spawn_position: pygame.Vector2 = pygame.Vector2(x, y)
        self.shield_count = 0
        self.bomb_count = 0
        self.velocity = pygame.Vector2(0, 0)
        self.base_acceleration = PLAYER_ACCELERATION
        self.base_max_speed = PLAYER_MAX_SPEED
        self.acceleration = self.base_acceleration
        self.max_speed = self.base_max_speed
        self.speed_boost_timers = []
        self.respawn_timer = 0.0
        self.debug_invulnerability = False
        self.turn_speed = PLAYER_TURN_SPEED
        self.sound_manager = sound_manager
        self.engine_channel = None
        self.game_controller = game_controller

    def draw(self, screen):
        if self.respawn_timer > 0:
            return

        points = self.triangle()
        pygame.draw.polygon(screen, "black", points, 0)
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    
    def rotate(self, dt):
        self.rotation += self.turn_speed * dt


    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        acceleration = rotated_vector * self.acceleration * dt
        self.velocity += acceleration
        self.velocity.clamp_magnitude_ip(self.max_speed)


    def decelerate(self, dt):
        self.velocity.move_towards_ip(pygame.Vector2(0, 0), PLAYER_DECELERATION * dt)
        

    def shoot(self):
        if self.shot_cooldown > 0:
            return
            
        self.sound_manager.play("ship_shot")

        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

        shot = Shot(self.position.x, self.position.y)
        shot_vector = pygame.Vector2(0, 1)
        shot_vector = shot_vector.rotate(self.rotation)
        shot_vector = shot_vector * PLAYER_SHOOT_SPEED
        shot.velocity = shot_vector
        

    def update(self, dt: float) -> None:
        if self.respawn_timer > 0:
            self.stop_engine_sound()
            self.respawn_timer -= dt

            if self.respawn_timer <= 0:
                self.respawn()
                self.respawn_timer = 0.0

            return

        keys = pygame.key.get_pressed()

        controller_turn = 0.0
        controller_thrust = 0.0
        controller_shoot = False

        if self.game_controller is not None:
            raw_turn_input = self.game_controller.get_axis(0)
            raw_thrust_input = -self.game_controller.get_axis(1)
            controller_shoot = bool(self.game_controller.get_button(0))

            if abs(raw_turn_input) > CONTROLLER_DEADZONE:
                controller_turn = raw_turn_input

            if abs(raw_thrust_input) > CONTROLLER_DEADZONE:
                controller_thrust = raw_thrust_input

        engine_active = (
            keys[pygame.K_w] 
            or keys[pygame.K_s] 
            or keys[pygame.K_a] 
            or keys[pygame.K_d] 
            or controller_turn != 0.0
            or controller_thrust != 0.0
            )

        self.update_engine_sound(dt, engine_active)

        if keys[pygame.K_a]:
            self.rotation -= self.turn_speed * dt

        if keys[pygame.K_d]:
            self.rotation += self.turn_speed * dt

        self.rotation += controller_turn * self.turn_speed * dt

        if keys[pygame.K_w]:
            self.move(dt) 

        if keys[pygame.K_s]:
            self.move(-dt)

        if controller_thrust != 0.0:
            self.move(controller_thrust * dt)

        if keys[pygame.K_SPACE] or controller_shoot:
            self.shoot()

        if (
            not keys[pygame.K_w] 
            and not keys[pygame.K_s]
            and controller_thrust == 0.0
        ):
            self.decelerate(dt)

        self.position += self.velocity * dt

        self.shot_cooldown -= dt
        self.invulnerability_timer -= dt
        self.update_speed_boosts(dt)

        wrap_position(self.position, self.radius)


    def respawn(self):
        self.position.update(self.spawn_position)
        self.velocity.update(0, 0)
        self.invulnerability_timer = PLAYER_INVULNERABILITY_SECONDS

    
    def take_damage(self):
        if (
            self.lives <= 0 or 
            self.invulnerability_timer > 0 or 
            self.respawn_timer > 0 or 
            self.debug_invulnerability
        ):
                return False
        

        if self.shield_count > 0:
            self.shield_count -= 1
            self.sound_manager.play("shield_consumed")
            self.invulnerability_timer = PLAYER_INVULNERABILITY_SECONDS
            return True

        self.lives -= 1
        self.stop_engine_sound()
        self.sound_manager.play("ship_destruction")

        if self.lives > 0:
            self.respawn_timer = PLAYER_RESPAWN_DELAY_SECONDS

        return True


    def recalculate_speed_stats(self):
        active_multiplier = SPEED_BOOST_MULTIPLIER ** len(self.speed_boost_timers)
        self.acceleration = self.base_acceleration * active_multiplier
        self.max_speed = self.base_max_speed * active_multiplier


    def add_speed_boost(self):
        self.speed_boost_timers.append(SPEED_BOOST_DURATION_SECONDS)
        self.recalculate_speed_stats()


    def add_shield(self):
        self.shield_count += 1


    def add_bomb(self):
        self.bomb_count += 1


    def update_speed_boosts(self, dt):
        active_speed_boost_timers = []
        for speed_boost in self.speed_boost_timers:
            speed_boost -= dt

            if speed_boost > 0:
                active_speed_boost_timers.append(speed_boost)
        
        self.speed_boost_timers = active_speed_boost_timers
        self.recalculate_speed_stats()


    def consume_bomb(self):
        if self.bomb_count <= 0:
            return False
        self.bomb_count -= 1
        return True


    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]


    def start_engine_sound(self):
        if self.engine_channel is None or not self.engine_channel.get_busy():
            self.engine_channel = self.sound_manager.play("ship_engine", loops=-1)

            if self.engine_channel is not None:
                self.engine_channel.set_volume(0.0)
                self.engine_volume = 0.0


    def stop_engine_sound(self):
        if self.engine_channel is not None:
            self.engine_channel.fadeout(SHIP_ENGINE_STOP_FADE_MS)

        self.engine_channel = None
        self.engine_volume = 0.0


    def update_engine_sound(self, dt, engine_active):
        if engine_active:
            self.start_engine_sound()

        if self.engine_channel is None:
            return

        if engine_active:
            target_volume = SHIP_ENGINE_MAX_VOLUME
        else:
            target_volume = 0.0

        volume_change = (SHIP_ENGINE_VOLUME_CHANGE_PER_SECOND * dt)

        if self.engine_volume < target_volume:
            self.engine_volume = min(target_volume, self.engine_volume + volume_change)

        elif self.engine_volume > target_volume:
            self.engine_volume = max(target_volume, self.engine_volume - volume_change)

        self.engine_channel.set_volume(self.engine_volume)