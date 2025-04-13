import json
from pathlib import Path
from threading import RLock
import re

class InMemoryStorage:
    VALID_FILE_NAME_REGEX = re.compile(r'^[\w,\s-]+\.[A-Za-z]{3}$')

    def __init__(self, storage_path):
        self.state = {}
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = RLock()  # Changed from Lock to RLock
        self.load_state()

    def load_state(self):
        with self.lock:
            if self.storage_path.exists():
                with open(self.storage_path, 'r') as file:
                    try:
                        self.state = json.load(file)
                    except json.JSONDecodeError:
                        print("Failed to decode JSON. Starting with an empty state.")
                        self.state = {}

    def save_state(self):
        with self.lock:
            try:
                if not isinstance(self.state, dict):
                    raise ValueError(f"State is not a dictionary: {type(self.state)}")

                if not self.storage_path.exists():
                    self.storage_path.touch()

                with open(self.storage_path, 'w') as file:
                    json.dump(self.state, file, indent=4)
            except json.JSONDecodeError as e:
                print(f"JSON serialization error: {e}")
            except Exception as e:
                print(f"Error saving state to {self.storage_path}: {e}")

    def update_state(self, key, value):
        with self.lock:
            try:
                self.state[key] = value
                self.save_state()
            except Exception as e:
                print(f"Error updating state for key {key}: {e}")

    def get_state(self, key):
        with self.lock:
            return self.state.get(key, None)

    @staticmethod
    def is_valid_file_name(file_name):
        """
        Validate the file name using a regex pattern.
        :param file_name: The file name to validate.
        :return: True if valid, False otherwise.
        """
        return bool(InMemoryStorage.VALID_FILE_NAME_REGEX.match(file_name))
