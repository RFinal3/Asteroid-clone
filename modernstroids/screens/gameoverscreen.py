import pygame

from modernstroids.screens.selectablemenu import SelectableMenu


class GameOverScreen(SelectableMenu):
    def __init__(self) -> None:
        super().__init__(("Restart", "High Scores", "Quit"))
        self.title_font = pygame.font.Font(None, 72)
        self.option_font = pygame.font.Font(None, 40)

    def draw(self, screen, score, score_qualified) -> None:
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = self.title_font.render("Game over!", True, "white")
        title_rect = title.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(title, title_rect)

        score_text = self.option_font.render(f"Final Score: {score}", True, "white")

        score_rect = score_text.get_rect(
            center=(screen.get_width() // 2, title_rect.bottom + 50)
        )

        if score_qualified:
            message = "You made the Top 10!"
            color = "yellow"
        else:
            message = "You did not make the Top 10."
            color = "white"

        message_text = self.option_font.render(
            message,
            True,
            color,
        )

        message_rect = message_text.get_rect(
            center=(screen.get_width() // 2, score_rect.bottom + 40)
        )

        screen.blit(score_text, score_rect)
        screen.blit(message_text, message_rect)
        next_y = message_rect.bottom + 40

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
