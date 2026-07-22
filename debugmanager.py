import pygame

class DebugManager:
    def __init__(self):
        self.debug_mode = False
        self.text_font = pygame.font.Font(None, 36)
        self.debug_invulnerability = False
        self.controls_font = pygame.font.Font(None, 24)
        

    def toggle(self):
        self.debug_mode = not self.debug_mode
        print(f"Debug mode: {self.debug_mode}")


    def handle_event(self, event, player, asteroid_field, pickup_spawner, ufo_spawner):
        if not self.debug_mode:
            return

        position = player.position + pygame.Vector2(100, 0)

        if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_i:
                    player.debug_invulnerability = not player.debug_invulnerability
                    print(f"{player.debug_invulnerability}")

                if event.key == pygame.K_c:
                    asteroid_field.spawn_random_asteroid()

                
                if event.key == pygame.K_p:
                    asteroid_field.toggle_spawning()

                
                if event.key == pygame.K_0:
                    pickup_spawner.force_spawn("shield", position)


                if event.key == pygame.K_9:
                    pickup_spawner.force_spawn("bomb", position)


                if event.key == pygame.K_8:
                    pickup_spawner.force_spawn("speed", position)


                if event.key == pygame.K_1:
                    player.add_shield()


                if event.key == pygame.K_2:
                    player.add_bomb()


                if event.key == pygame.K_3:
                    player.add_speed_boost()

                
                if event.key == pygame.K_u:
                    ufo_spawner.spawn_random_ufo()

    
    def draw(self, screen, fps, counts):
        if not self.debug_mode:
            return

        debug_header = self.text_font.render("DEBUG MODE", True, "white")
        debug_header_rect = debug_header.get_rect(
            topright=(screen.get_width() - 20, 20)
        )
        screen.blit(debug_header, debug_header_rect)

        debug_fps = self.text_font.render(f"FPS: {fps:.0f}", True, "white")
        debug_fps_rect = debug_fps.get_rect(
            topright=(
                screen.get_width() - 20,
                debug_header_rect.bottom + 5,
            )
        )
        screen.blit(debug_fps, debug_fps_rect)

        next_y = debug_fps_rect.bottom + 5

        for label, value in counts.items():
            debug_line = self.text_font.render(
                f"{label}: {value}",
                True,
                "white",
            )
            debug_line_rect = debug_line.get_rect(
                topright=(screen.get_width() - 20, next_y)
            )

            screen.blit(debug_line, debug_line_rect)
            next_y = debug_line_rect.bottom + 5

        controls = (
            "I: Invulnerable | P: Pause asteroids",
            "C: Spawn asteroid | U: Spawn UFO",
            "1/2/3: Give shield/bomb/speed",
            "0/9/8: Spawn shield/bomb/speed",
        )

        next_y += 10

        for control in controls:
            control_line = self.controls_font.render(
                control,
                True,
                "white",
            )
            control_line_rect = control_line.get_rect(
                topright=(screen.get_width() - 20, next_y)
            )

            screen.blit(control_line, control_line_rect)
            next_y = control_line_rect.bottom + 3