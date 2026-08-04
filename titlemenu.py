import pygame


class TitleMenu:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 96)
        self.option_font = pygame.font.Font(None, 40)
        self.options = ("Start Game", "High Scores", "Options", "Quit")
        self.selected_index = 0
        self.option_rect = []

    def draw(self, screen):
        title = self.title_font.render("Modernstroids!", True, "white")
        title_rect = title.get_rect(center=(screen.get_width() // 2, 170))
        screen.blit(title, title_rect)
        next_y = title_rect.bottom + 70
        self.options_rect = []

        for index, label in enumerate(self.options):
            if index == self.selected_index:
                color = "yellow"
            else:
                color = "white"

            option_text = self.option_font.render(label, True, color)
            option_rect = option_text.get_rect(center=(screen.get_width() // 2, next_y))

            self.option_rect.append(option_rect)
            screen.blit(option_text, option_rect)

            next_y = option_rect.bottom + 25

    def handle_event(self, event, input_manager):
        menu_action = input_manager.get_menu_action(event)

        if menu_action == "up":
            self.selected_index -= 1
        elif menu_action == "down":
            self.selected_index += 1

        self.selected_index %= len(self.options)

        if event.type == pygame.MOUSEMOTION:
            for index, option_rect in enumerate(self.option_rect):
                if option_rect.collidepoint(event.pos):
                    self.selected_index = index
                    break

        if menu_action == "select":
            return self.options[self.selected_index]

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for index, option_rect in enumerate(self.option_rect):
                    if option_rect.collidepoint(event.pos):
                        self.selected_index = index
                        return self.options[index]

        return None
