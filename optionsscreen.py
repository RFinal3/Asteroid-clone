import pygame

from constants import (
    PLAYER_TURN_SPEED_MAX,
    PLAYER_TURN_SPEED_MIN,
    PLAYER_TURN_SPEED_STEP,
)


class OptionsScreen:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 72)
        self.option_font = pygame.font.Font(None, 40)
        self.info_font = pygame.font.Font(None, 28)
        self.selected_index = 0
        self.option_rects = []
        self.slider_rect = None
        self.slider_knob_rect = None
        self.confirming_clear = False
        self.confirmation_selected = 0
        self.confirmation_rects = []

    def draw(self, screen, settings):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))

        title = self.title_font.render("OPTIONS", True, "white")
        title_rect = title.get_rect(center=(screen.get_width() // 2, 120))
        screen.blit(title, title_rect)

        if self.selected_index == 0:
            rotation_color = "yellow"
        else:
            rotation_color = "white"

        self.option_rects = []

        rotation_text = self.option_font.render(
            f"Rotation Speed: {settings.player_turn_speed}", True, rotation_color
        )
        rotation_rect = rotation_text.get_rect(center=(screen.get_width() // 2, 230))
        self.option_rects.append(rotation_rect)
        screen.blit(rotation_text, rotation_rect)

        self.slider_rect = pygame.Rect(0, 0, 400, 8)
        self.slider_rect.center = (screen.get_width() // 2, 290)

        pygame.draw.rect(screen, "white", self.slider_rect)

        speed_range = PLAYER_TURN_SPEED_MAX - PLAYER_TURN_SPEED_MIN

        progress = (settings.player_turn_speed - PLAYER_TURN_SPEED_MIN) / speed_range

        knob_x = self.slider_rect.left + int(progress * self.slider_rect.width)

        self.slider_knob_rect = pygame.Rect(0, 0, 20, 30)
        self.slider_knob_rect.center = (knob_x, self.slider_rect.centery)

        rotation_area = rotation_rect.union(self.slider_rect.inflate(40, 40))

        self.option_rects[0] = rotation_area

        pygame.draw.rect(screen, "yellow", self.slider_knob_rect)

        menu_options = (("Clear High Scores", 400), ("Back", 475))

        for index, (label, y_position) in enumerate(menu_options, start=1):
            if index == self.selected_index:
                color = "yellow"
            else:
                color = "white"

            option_text = self.option_font.render(label, True, color)

            option_rect = option_text.get_rect(
                center=(screen.get_width() // 2, y_position)
            )

            self.option_rects.append(option_rect)
            screen.blit(option_text, option_rect)

        if self.confirming_clear:
            confirmation_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            confirmation_overlay.fill((0, 0, 0, 220))
            screen.blit(confirmation_overlay, (0, 0))

            prompt = self.option_font.render("Clear all high scores?", True, "white")
            prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, 300))
            screen.blit(prompt, prompt_rect)

            confirmation_options = (
                ("No", screen.get_width() // 2 - 100),
                ("Yes", screen.get_width() // 2 + 100),
            )

            self.confirmation_rects = []

            for index, (label, x_position) in enumerate(confirmation_options):
                if index == self.confirmation_selected:
                    color = "yellow"
                else:
                    color = "white"

                option_text = self.option_font.render(label, True, color)
                option_rect = option_text.get_rect(center=(x_position, 380))

                self.confirmation_rects.append(option_rect)
                screen.blit(option_text, option_rect)

    def handle_event(self, event, input_manager):
        menu_action = input_manager.get_menu_action(event)

        if self.confirming_clear:
            return self.handle_confirmation_event(event, input_manager)

        if menu_action == "up":
            self.selected_index -= 1
            self.selected_index %= 3

        elif menu_action == "down":
            self.selected_index += 1
            self.selected_index %= 3

        elif menu_action == "left" and self.selected_index == 0:
            return "Decrease Rotation"

        elif menu_action == "right" and self.selected_index == 0:
            return "Increase Rotation"

        elif menu_action == "select":
            if self.selected_index == 1:
                return "Clear High Scores"

            if self.selected_index == 2:
                return "Back"

        elif menu_action == "back":
            return "Back"

        if event.type == pygame.MOUSEMOTION:
            for index, option_rect in enumerate(self.option_rects):
                if option_rect.collidepoint(event.pos):
                    self.selected_index = index
                    break

            if (
                self.slider_rect is not None
                and event.buttons[0]
                and self.slider_rect.collidepoint(event.pos)
            ):
                return ("Set Rotation", self.get_slider_value(event.pos[0]))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.slider_rect.inflate(20, 30).collidepoint(event.pos):
                self.selected_index = 0
                return ("Set Rotation", self.get_slider_value(event.pos[0]))

            for index, option_rect in enumerate(self.option_rects):
                if option_rect.collidepoint(event.pos):
                    self.selected_index = index

                    if index == 1:
                        return "Clear High Scores"

                    if index == 2:
                        return "Back"

        return None

    def get_slider_value(self, mouse_x):
        clamped_x = max(self.slider_rect.left, min(mouse_x, self.slider_rect.right))

        progress = (clamped_x - self.slider_rect.left) / self.slider_rect.width

        raw_value = PLAYER_TURN_SPEED_MIN + progress * (
            PLAYER_TURN_SPEED_MAX - PLAYER_TURN_SPEED_MIN
        )

        steps = round((raw_value - PLAYER_TURN_SPEED_MIN) / PLAYER_TURN_SPEED_STEP)

        return PLAYER_TURN_SPEED_MIN + steps * PLAYER_TURN_SPEED_STEP

    def open_clear_confirmation(self):
        self.confirming_clear = True
        self.confirmation_selected = 0

    def handle_confirmation_event(self, event, input_manager):
        menu_action = input_manager.get_menu_action(event)

        if menu_action in ("left", "right"):
            self.confirmation_selected = 1 - self.confirmation_selected

        elif menu_action == "select":
            if self.confirmation_selected == 1:
                self.confirming_clear = False
                return "Confirm Clear"

            self.confirming_clear = False
            return None

        elif menu_action == "back":
            self.cancel_clear_confirmation()
            return None

        if event.type == pygame.MOUSEMOTION:
            for index, option_rect in enumerate(self.confirmation_rects):
                if option_rect.collidepoint(event.pos):
                    self.confirmation_selected = index
                    break

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for index, option_rect in enumerate(self.confirmation_rects):
                if option_rect.collidepoint(event.pos):
                    self.confirming_clear = False

                    if index == 1:
                        return "Confirm Clear"

                    return None

        return None

    def cancel_clear_confirmation(self):
        self.confirming_clear = False
        self.confirmation_selected = 0
