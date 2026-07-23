import pygame


class HighScoreScreen:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 72)
        self.entry_font = pygame.font.Font(None, 36)
        self.info_font = pygame.font.Font(None, 28)

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