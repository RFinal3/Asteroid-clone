import pygame


class HighScoreScreen:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 72)
        self.entry_font = pygame.font.Font(None, 36)
        self.info_font = pygame.font.Font(None, 28)
        self.back_rect = None
        self.back_hovered = False

    def draw(self, screen, entries):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))

        title = self.title_font.render("HIGH SCORES", True, "white")

        title_rect = title.get_rect(center=(screen.get_width() // 2, 100))

        screen.blit(title, title_rect)

        next_y = title_rect.bottom + 40

        for rank, entry in enumerate(entries, start=1):
            entry_text = self.entry_font.render(f"{rank}. {entry['name']} | Score: {entry['score']}", True, "white")

            entry_rect = entry_text.get_rect(center=(screen.get_width() // 2, next_y))

            screen.blit(entry_text, entry_rect)
            next_y = entry_rect.bottom + 15

        if not entries:
            no_scores_text = self.entry_font.render("No high scores yet.", True, "white")

            no_scores_rect = no_scores_text.get_rect(center=(screen.get_width() // 2, next_y))

            screen.blit(no_scores_text, no_scores_rect)

        if self.back_hovered:
            back_color = "yellow"
        else:
            back_color = "white"

        back_text = self.entry_font.render(
            "Back",
            True,
            back_color,
        )

        self.back_rect = back_text.get_rect(
            center=(
                screen.get_width() // 2,
                screen.get_height() - 60,
            )
        )

        screen.blit(back_text, self.back_rect)


    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.back_rect is not None:
                self.back_hovered = self.back_rect.collidepoint(
                    event.pos
                )

        if event.type == pygame.MOUSEBUTTONDOWN:
            if (
                event.button == 1
                and self.back_rect is not None
                and self.back_rect.collidepoint(event.pos)
            ):
                return "Back"

        return None