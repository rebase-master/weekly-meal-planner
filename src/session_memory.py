import json
import os
from typing import Dict

class SessionMemory:
    """
    Lightweight session memory storing:
    - dietary preferences
    - allergies
    - cuisine preferences
    - past meals (to avoid repetition)
    """

    def __init__(self, path: str = "memory.json"):
        self.path = path
        self.memory = self._load()

    def _load(self) -> Dict:
        """Load memory file from disk, create if not exists."""
        if not os.path.exists(self.path):
            return {"past_meals": []}
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except Exception:
            return {"past_meals": []}

    def get(self) -> Dict:
        """Return memory dictionary."""
        return self.memory

    def update_with_new_meals(self, meals):
        """Store newly planned meals for future runs."""
        past = set(self.memory.get("past_meals", []))
        for m in meals:
            past.add(m)
        self.memory["past_meals"] = list(past)
        self._save()

    def update_dietary_info(self, dietary_info: Dict):
        """Save most recent user dietary profile."""
        self.memory["dietary_info"] = dietary_info
        self._save()

    def _save(self):
        """Write memory to disk."""
        with open(self.path, "w") as f:
            json.dump(self.memory, f, indent=2)
