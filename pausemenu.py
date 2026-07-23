import pygame


class PauseMenu:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 72)
        self.option_font = pygame.font.Font(None, 40)
        self.selected_index = 0
        self.option_rects = []

        self.options = (
            "Resume",
            "Restart",
            "Quit",
        )


    def draw(self, screen):
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


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index -= 1

            elif event.key == pygame.K_DOWN:
                self.selected_index += 1

            self.selected_index %= len(self.options)

        
        if event.type == pygame.MOUSEMOTION:
            for index, option_rect in enumerate(self.option_rects):
                if option_rect.collidepoint(event.pos):
                    self.selected_index = index
                    break

        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return self.options[self.selected_index]

        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for index, option_rect in enumerate(self.option_rects):
                    if option_rect.collidepoint(event.pos):
                        self.selected_index = index
                        return self.options[index]

        
        return None