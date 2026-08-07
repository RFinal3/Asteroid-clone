import pygame

from modernstroids.screens.selectablemenu import SelectableMenu


class PauseMenu(SelectableMenu):
    def __init__(self) -> None:
        super().__init__(
            (
                "Resume",
                "Restart",
                "High Scores",
                "Options",
                "Quit to Menu",
                "Quit Program",
            )
        )
        self.title_font = pygame.font.Font(None, 72)
        self.option_font = pygame.font.Font(None, 40)

    def draw(self, screen) -> None:
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = self.title_font.render("PAUSED", True, "white")
        title_rect = title.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(title, title_rect)

        next_y = title_rect.bottom + 60
        self.option_rects = []

        for index, option in enumerate(self.options):
            if index == self.selected_index:
                color = "yellow"
            else:
                color = "white"

            option_text = self.option_font.render(option, True, color)

            option_rect = option_text.get_rect(center=(screen.get_width() // 2, next_y))

            self.option_rects.append(option_rect)
            screen.blit(option_text, option_rect)

            next_y = option_rect.bottom + 25
