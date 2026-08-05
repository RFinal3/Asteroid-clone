import json

from modernstroids.core.constants import (
    PLAYER_TURN_SPEED,
    PLAYER_TURN_SPEED_MAX,
    PLAYER_TURN_SPEED_MIN,
)
from modernstroids.storage import USER_DATA_DIRECTORY


class SettingsManager:
    def __init__(self):
        self.file_path = USER_DATA_DIRECTORY / "settings.json"
        self.player_turn_speed = PLAYER_TURN_SPEED
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

        except (OSError, json.JSONDecodeError, TypeError):
            self.player_turn_speed = PLAYER_TURN_SPEED

    def save(self):
        try:
            self.file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            data = {
                "player_turn_speed": self.player_turn_speed,
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
