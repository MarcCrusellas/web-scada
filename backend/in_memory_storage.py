import json
from pathlib import Path
from threading import RLock

class InMemoryStorage:
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
        print("Attempting to acquire lock for save_state...")
        with self.lock:
            print("Lock acquired for save_state.")
            try:
                # Validate state before saving
                if not isinstance(self.state, dict):
                    raise ValueError(f"State is not a dictionary: {type(self.state)}")

                if not self.storage_path.exists():
                    print(f"File {self.storage_path} does not exist. Creating it.")
                    self.storage_path.touch()

                print(f"Attempting to save state to file: {self.storage_path}")
                with open(self.storage_path, 'w') as file:
                    json.dump(self.state, file, indent=4)
                print("State saved successfully.")
            except json.JSONDecodeError as e:
                print(f"JSON serialization error: {e}")
            except Exception as e:
                print(f"Error saving state to {self.storage_path}: {e}")
            finally:
                print("Releasing lock for save_state.")

    def update_state(self, key, value):
        print(f"Attempting to acquire lock for update_state with key: {key}, value: {value}...")
        with self.lock:
            print("Lock acquired for update_state.")
            try:
                self.state[key] = value
                print(f"State updated in memory: {self.state}")
                self.save_state()
                print(f"State successfully persisted for key: {key}")
            except Exception as e:
                print(f"Error updating state for key {key}: {e}")
            finally:
                print("Releasing lock for update_state.")

    def get_state(self, key):
        with self.lock:
            return self.state.get(key, None)
