import pygame
from pygame._sdl2 import controller

from constants import CONTROLLER_DEADZONE


class InputManager:
    def __init__(self):
        self.controller = None
        self.controller_name = None
        self.controller_instance_id = None
        self.shooting_suppressed = False
        self.menu_axis_latched = {
            pygame.CONTROLLER_AXIS_LEFTX: False,
            pygame.CONTROLLER_AXIS_LEFTY: False,
        }

        controller.init()

        for device_index in range(controller.get_count()):
            if not controller.is_controller(device_index):
                continue

            self.controller = controller.Controller(device_index)
            self.controller_name = controller.name_forindex(device_index)

            selected_joystick = self.controller.as_joystick()
            self.controller_instance_id = selected_joystick.get_instance_id()
            break

    def _controller_button_pressed(self, event, button):
        return (
            self.controller is not None
            and event.type == pygame.CONTROLLERBUTTONDOWN
            and event.instance_id == self.controller_instance_id
            and event.button == button
        )

        
    def _get_axis(self, axis):
        if self.controller is None:
            return 0.0

        raw_value = self.controller.get_axis(axis)
        normalized_value = raw_value / 32767.0
        normalized_value = max(-1.0, min(1.0, normalized_value))
        if abs(normalized_value) <= CONTROLLER_DEADZONE:
            return 0.0

        return normalized_value


    def get_turn_input(self):
        return self._get_axis(pygame.CONTROLLER_AXIS_LEFTX)


    def get_thrust_input(self):
        return -self._get_axis(pygame.CONTROLLER_AXIS_LEFTY)


    def is_shooting(self):
        if self.controller is None:
            return False

        shooting = self.controller.get_button(
            pygame.CONTROLLER_BUTTON_A
        )

        if not shooting:
            self.shooting_suppressed = False
            return False

        return not self.shooting_suppressed

    
    def suppress_shooting_until_released(self):
        self.shooting_suppressed = True


    def is_bomb_pressed(self, event):
        keyboard_requested = (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_b
        )

        controller_requested = self._controller_button_pressed(
            event,
            pygame.CONTROLLER_BUTTON_B,
        )

        return keyboard_requested or controller_requested


    def is_pause_pressed(self, event):
        keyboard_requested = (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        )

        controller_requested = self._controller_button_pressed(
            event,
            pygame.CONTROLLER_BUTTON_START,
        )

        return keyboard_requested or controller_requested


    def get_menu_action(self, event):
        keyboard_actions = {
            pygame.K_UP: "up",
            pygame.K_DOWN: "down",
            pygame.K_LEFT: "left",
            pygame.K_RIGHT: "right",
            pygame.K_RETURN: "select",
            pygame.K_KP_ENTER: "select",
            pygame.K_ESCAPE: "back"
        }

        controller_actions = {
            pygame.CONTROLLER_BUTTON_DPAD_UP: "up",
            pygame.CONTROLLER_BUTTON_DPAD_DOWN: "down",
            pygame.CONTROLLER_BUTTON_DPAD_LEFT: "left",
            pygame.CONTROLLER_BUTTON_DPAD_RIGHT: "right",
            pygame.CONTROLLER_BUTTON_A: "select",
            pygame.CONTROLLER_BUTTON_B: "back",
        }

        if event.type == pygame.KEYDOWN:
            return keyboard_actions.get(event.key)

        elif (
            self.controller is not None
            and event.type == pygame.CONTROLLERBUTTONDOWN
            and event.instance_id == self.controller_instance_id
        ):
            return controller_actions.get(event.button)

        elif (
            self.controller is not None
            and event.type == pygame.CONTROLLERAXISMOTION
            and event.instance_id == self.controller_instance_id
        ):
            axis = event.axis

            if axis not in self.menu_axis_latched:
                return None

            normalized_value = event.value / 32767.0
            normalized_value = max(
                -1.0,
                min(1.0, normalized_value),
            )

            if abs(normalized_value) <= 0.5:
                self.menu_axis_latched[axis] = False
                return None

            if self.menu_axis_latched[axis]:
                return None

            self.menu_axis_latched[axis] = True

            if axis == pygame.CONTROLLER_AXIS_LEFTY:
                if normalized_value < 0:
                    return "up"

                return "down"

            if axis == pygame.CONTROLLER_AXIS_LEFTX:
                if normalized_value < 0:
                    return "left"

                return "right"

        return None


    def has_controller(self):
        return self.controller is not None

    
    def is_name_character_pressed(self, event):
        return self._controller_button_pressed(
            event,
            pygame.CONTROLLER_BUTTON_A,
        )

    
    def is_name_submit_pressed(self, event):
        return self._controller_button_pressed(
            event,
            pygame.CONTROLLER_BUTTON_START,
        )


    def is_name_delete_pressed(self, event):
        return self._controller_button_pressed(
            event,
            pygame.CONTROLLER_BUTTON_B,
        )