import pygame

from modernstroids.screens.selectablemenu import SelectableMenu


class TitleMenu(SelectableMenu):
    def __init__(self) -> None:
        super().__init__(("Start Game", "High Scores", "Options", "Quit"))
        self.title_font = pygame.font.Font(None, 96)
        self.option_font = pygame.font.Font(None, 40)

    def draw(self, screen: pygame.Surface) -> None:
        title = self.title_font.render("Modernstroids!", True, "white")
        title_rect = title.get_rect(center=(screen.get_width() // 2, 170))
        screen.blit(title, title_rect)
        next_y = title_rect.bottom + 70
        self.option_rects = []

        for index, label in enumerate(self.options):
            if index == self.selected_index:
                color = "yellow"
            else:
                color = "white"

            option_text = self.option_font.render(label, True, color)
            option_rect = option_text.get_rect(center=(screen.get_width() // 2, next_y))

            self.option_rects.append(option_rect)
            screen.blit(option_text, option_rect)

            next_y = option_rect.bottom + 25
