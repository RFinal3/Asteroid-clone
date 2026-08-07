import pygame

from modernstroids.systems.inputmanager import InputManager


class SelectableMenu:
    """Provide shared navigation and activation for a vertical menu."""

    def __init__(
        self,
        options: tuple[str, ...],
        back_action: str | None = None,
    ) -> None:
        self.options = options
        self.back_action = back_action
        self.selected_index = 0
        self.option_rects: list[pygame.Rect] = []

    def _activate_selected_option(self) -> str:
        return self.options[self.selected_index]

    def handle_event(
        self,
        event: pygame.event.Event,
        input_manager: InputManager,
    ) -> str | None:
        menu_action = input_manager.get_menu_action(event)

        if menu_action == "up":
            self.selected_index -= 1
        elif menu_action == "down":
            self.selected_index += 1

        self.selected_index %= len(self.options)

        if event.type == pygame.MOUSEMOTION:
            for index, option_rect in enumerate(self.option_rects):
                if option_rect.collidepoint(event.pos):
                    self.selected_index = index
                    break

        if menu_action == "select":
            return self._activate_selected_option()

        if menu_action == "back":
            return self.back_action

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for index, option_rect in enumerate(self.option_rects):
                if option_rect.collidepoint(event.pos):
                    self.selected_index = index
                    return self._activate_selected_option()

        return None
