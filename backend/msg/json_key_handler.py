from storage.in_memory_storage import InMemoryStorage
from pathlib import Path

class JsonKeyHandler:

    storage_cache = {}

    @staticmethod
    def get_storage(env):
        """
        Dynamically get or create an InMemoryStorage instance for the given environment.
        :param env: The environment or state file name.
        :return: An instance of InMemoryStorage.
        """
        if env not in JsonKeyHandler.storage_cache:
            storage_path = Path.home() / "WSCADA" / f"{env}.json"
            JsonKeyHandler.storage_cache[env] = InMemoryStorage(storage_path)
        return JsonKeyHandler.storage_cache[env]

    @staticmethod
    def handle_json_key(message_args, uuid):
        # Extracting arguments from the message
        env = message_args.get('env', 'state')
        operation_type = message_args.get('type')
        key = message_args.get('key')
        value = message_args.get('value')

        storage = JsonKeyHandler.get_storage(env)

        match operation_type:
            case 'fetch':
                return JsonKeyHandler.fetch_key(storage, env, key, uuid)
            case 'update':
                return JsonKeyHandler.update_key(storage, env, key, value, uuid)
            case _:
                return {"type": "error", "message": "Unsupported operation type.", "uuid": uuid}

    @staticmethod
    def fetch_key(storage, env, key, uuid):
        value = storage.get_state(key)
        if value is None:
            return {"type": "error", "message": f"Key '{key}' not found in environment '{env}'.", "uuid": uuid}
        return {"type": "ok", "env": env, "key": key, "value": value, "uuid": uuid}

    @staticmethod
    def update_key(storage, env, key, value, uuid):
        storage.update_state(key, value)
        return {"type": "ok", "env": env, "key": key, "value": value, "uuid": uuid}
