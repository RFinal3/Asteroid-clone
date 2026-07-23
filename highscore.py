from pathlib import Path
import json


class HighScoreManager:
    def __init__(self):
        self.file_path = (
            Path.home()
            / ".modernsteroids"
            / "high_scores.json"
        )
        self.entries = []
        self.load()

    
    def load(self):
        if not self.file_path.exists():
            return

        try:
            data = json.loads(self.file_path.read_text())
            self.entries = data.get("scores", [])
        except (OSError, json.JSONDecodeError):
            self.entries = []


    def save(self):
        try:
            self.file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            data = {
                "scores": self.entries,
            }

            self.file_path.write_text(
                json.dumps(data, indent=4)
            )

        except OSError:
            return False

        return True


    def qualifies(self, score):
        if score <= 0:
            return False

        if len(self.entries) < 10:
            return True

        return score > self.entries[-1]["score"]


    def add_score(self, name, score):
        if not self.qualifies(score):
            return False

        cleaned_name = name.strip()

        if not cleaned_name:
            cleaned_name = "Anonymous"

        entry = {
            "name": cleaned_name,
            "score": score,
        }

        self.entries.append(entry)
        self.entries.sort(
            key=lambda entry: entry["score"],
            reverse=True,
        )
        self.entries = self.entries[:10]

        self.save()
        return True