import pygame

NAME_CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.!?_- "


class NameEntryScreen:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 72)
        self.text_font = pygame.font.Font(None, 36)
        self.name = ""
        self.max_length = 10
        self.selected_character_index = 0
        self.info_font = pygame.font.Font(None, 26)

    
    def start(self):
        self.name = ""
        self.selected_character_index = 0
        pygame.key.start_text_input()


    def stop(self):
        pygame.key.stop_text_input()

    
    def handle_event(self, event, input_manager):
        menu_action = input_manager.get_menu_action(event)
        controller_delete_pressed = input_manager.is_name_delete_pressed(event)
        controller_character_pressed = (
            input_manager.is_name_character_pressed(event)
        )
        controller_submit_pressed = input_manager.is_name_submit_pressed(event)

        if event.type == pygame.TEXTINPUT:
            typed_text = event.text.upper()
            valid_text = ""

            for character in typed_text:
                if character in NAME_CHARACTERS:
                    valid_text += character

            remaining_space = self.max_length - len(self.name)
            self.name += valid_text[:remaining_space]

        if menu_action == "up":
            self.selected_character_index -= 1

        elif menu_action == "down":
            self.selected_character_index += 1

        self.selected_character_index %= len(NAME_CHARACTERS)

        if controller_character_pressed and len(self.name) < self.max_length:
            selected_character = NAME_CHARACTERS[
                self.selected_character_index
            ]
            self.name += selected_character

        if controller_delete_pressed:
            self.name = self.name[:-1]

        if controller_submit_pressed:
            cleaned_name = self.name.strip()

            if cleaned_name:
                return cleaned_name

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]

            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                cleaned_name = self.name.strip()

                if cleaned_name:
                    return cleaned_name

        return None


    def draw(self, screen, score, input_manager):
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

        if input_manager.has_controller():
            slot_width = 44
            slot_size = 36
            slots_y = 380

            total_width = self.max_length * slot_width
            starting_x = (screen.get_width() - total_width) // 2
            current_slot = len(self.name)

            for slot_index in range(self.max_length):
                slot_x = starting_x + slot_index * slot_width

                slot_rect = pygame.Rect(
                    slot_x,
                    slots_y,
                    slot_size,
                    slot_size,
                )

                if slot_index < len(self.name):
                    displayed_character = self.name[slot_index]

                elif slot_index == current_slot:
                    displayed_character = NAME_CHARACTERS[
                        self.selected_character_index
                    ]

                    if displayed_character == " ":
                        displayed_character = "SP"

                else:
                    displayed_character = ""

                if slot_index == current_slot:
                    slot_color = "yellow"
                else:
                    slot_color = "white"

                pygame.draw.rect(screen, slot_color, slot_rect, 2)

                character_text = self.text_font.render(
                    displayed_character,
                    True,
                    slot_color,
                )
                character_rect = character_text.get_rect(
                    center=slot_rect.center
                )
                screen.blit(character_text, character_rect)


            instruction_text = self.info_font.render(
                "D-Pad: Choose | A: Add | B: Delete | Start: Submit",
                True,
                "white",
            )
            instruction_rect = instruction_text.get_rect(
                center=(screen.get_width() // 2, 500)
            )
            screen.blit(instruction_text, instruction_rect)

        

            if current_slot < self.max_length:
                selector_x = (
                    starting_x
                    + current_slot * slot_width
                    + slot_size // 2
                )

                previous_index = (
                    self.selected_character_index - 1
                ) % len(NAME_CHARACTERS)

                next_index = (
                    self.selected_character_index + 1
                ) % len(NAME_CHARACTERS)

                previous_character = NAME_CHARACTERS[previous_index]
                next_character = NAME_CHARACTERS[next_index]

                if previous_character == " ":
                    previous_character = "SPACE"

                if next_character == " ":
                    next_character = "SPACE"

                previous_text = self.info_font.render(
                    previous_character,
                    True,
                    (130, 130, 130),
                )
                previous_rect = previous_text.get_rect(
                    center=(selector_x, slots_y - 25)
                )
                screen.blit(previous_text, previous_rect)

                next_text = self.info_font.render(
                    next_character,
                    True,
                    (130, 130, 130),
                )
                next_rect = next_text.get_rect(
                    center=(selector_x, slots_y + slot_size + 25)
                )
                screen.blit(next_text, next_rect)

        else:
            name_text = self.text_font.render(
                f"{self.name}| ({len(self.name)}/{self.max_length})",
                True,
                "yellow",
            )
            name_rect = name_text.get_rect(
                center=(screen.get_width() // 2, 360)
            )
            screen.blit(name_text, name_rect)

            instruction_text = self.info_font.render(
                "Type your name | Backspace: Delete | Enter: Submit",
                True,
                "white",
            )
            instruction_rect = instruction_text.get_rect(
                center=(screen.get_width() // 2, 430)
            )
            screen.blit(instruction_text, instruction_rect)