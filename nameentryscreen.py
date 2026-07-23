import pygame


class NameEntryScreen:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 72)
        self.text_font = pygame.font.Font(None, 36)
        self.name = ""
        self.max_length = 16

    
    def start(self):
        self.name = ""
        pygame.key.start_text_input()


    def stop(self):
        pygame.key.stop_text_input()

    
    def handle_event(self, event):
        if event.type == pygame.TEXTINPUT:
            remaining_space = self.max_length - len(self.name)
            self.name += event.text[:remaining_space]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]

            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                cleaned_name = self.name.strip()

                if cleaned_name:
                    return cleaned_name

        return None


    def draw(self, screen, score):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 230))
        screen.blit(overlay, (0, 0))

        title = self.title_font.render("NEW HIGH SCORE!", True, "yellow")
        title_rect = title.get_rect(center=(screen.get_width() // 2, 140))
        screen.blit(title, title_rect)

        score_text = self.text_font.render(f"Score: {score}", True, "white")
        score_rect = score_text.get_rect(center=(screen.get_width() // 2, 230))
        screen.blit(score_text, score_rect)

        prompt_text = self.text_font.render("Enter your name:", True, "white")
        prompt_rect = prompt_text.get_rect(center=(screen.get_width() // 2, 300))
        screen.blit(prompt_text, prompt_rect)

        name_text = self.text_font.render(f"{self.name}|", True, "yellow")
        name_rect = name_text.get_rect(center=(screen.get_width() // 2, 360))
        screen.blit(name_text, name_rect)

        info_text = self.text_font.render("Press Enter to submit", True, "white")
        info_rect = info_text.get_rect(center=(screen.get_width() // 2, 430))
        screen.blit(info_text, info_rect)