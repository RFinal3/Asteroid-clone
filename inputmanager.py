from pygame._sdl2 import controller
import pygame
from constants import CONTROLLER_DEADZONE

class InputManager:
    def __init__(self):
        self.controller = None
        self.controller_name = None
        controller.init()

        for device_index in range(controller.get_count()):
            if not controller.is_controller(device_index):
                continue

            self.controller = controller.Controller(device_index)
            self.controller_name = controller.name_forindex(device_index)
            break

        
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

        return self.controller.get_button(pygame.CONTROLLER_BUTTON_A)