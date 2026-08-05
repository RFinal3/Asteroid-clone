import json

from modernstroids.core.constants import (
    CONTROLLER_SCHEME_CLASSIC,
    CONTROLLER_SCHEME_MODERN,
    CONTROLLER_SCHEMES,
    PLAYER_TURN_SPEED,
    PLAYER_TURN_SPEED_MAX,
    PLAYER_TURN_SPEED_MIN,
)
from modernstroids.storage import USER_DATA_DIRECTORY


class SettingsManager:
    def __init__(self):
        self.file_path = USER_DATA_DIRECTORY / "settings.json"
        self.player_turn_speed = PLAYER_TURN_SPEED
        self.controller_scheme = CONTROLLER_SCHEME_CLASSIC
        self.load()

    def load(self):
        if not self.file_path.exists():
            return

        try:
            data = json.loads(self.file_path.read_text())

            loaded_speed = data.get(
                "player_turn_speed",
                PLAYER_TURN_SPEED,
            )

            self.player_turn_speed = max(
                PLAYER_TURN_SPEED_MIN,
                min(loaded_speed, PLAYER_TURN_SPEED_MAX),
            )

            loaded_controller_scheme = data.get(
                "controller_scheme",
                CONTROLLER_SCHEME_CLASSIC,
            )

            if loaded_controller_scheme in CONTROLLER_SCHEMES:
                self.controller_scheme = loaded_controller_scheme
            else:
                self.controller_scheme = CONTROLLER_SCHEME_CLASSIC

        except (OSError, json.JSONDecodeError, TypeError):
            self.player_turn_speed = PLAYER_TURN_SPEED
            self.controller_scheme = CONTROLLER_SCHEME_CLASSIC

    def save(self):
        try:
            self.file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            data = {
                "player_turn_speed": self.player_turn_speed,
                "controller_scheme": self.controller_scheme,
            }

            self.file_path.write_text(json.dumps(data, indent=4))

        except OSError:
            return False

        return True

    def set_player_turn_speed(self, value):
        self.player_turn_speed = max(
            PLAYER_TURN_SPEED_MIN,
            min(value, PLAYER_TURN_SPEED_MAX),
        )

        return self.save()

    def set_controller_scheme(self, value):
        if value not in CONTROLLER_SCHEMES:
            return False

        self.controller_scheme = value
        return self.save()

    def toggle_controller_scheme(self):
        if self.controller_scheme == CONTROLLER_SCHEME_CLASSIC:
            new_scheme = CONTROLLER_SCHEME_MODERN
        else:
            new_scheme = CONTROLLER_SCHEME_CLASSIC

        return self.set_controller_scheme(new_scheme)
