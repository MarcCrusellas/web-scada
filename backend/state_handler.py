import json
from storage.in_memory_storage import InMemoryStorage

class StateHandler:
    def __init__(self, storage):
        self.storage = storage

    async def handle_fetch(self, websocket, data):
        print(f"Fetching state for key: {data['key']}")
        key = data['key']
        value = self.storage.get_state(key)
        await websocket.send(json.dumps({"type": "fetch", "key": key, "value": value}))

    async def handle_update(self, websocket, data):
        print(f"Updating state for key: {data['key']} with value: {data['value']}")
        key = data['key']
        value = data['value']

        if not isinstance(value, (str, int, float, list, dict, bool, type(None))):
            print(f"Unsupported value type: {type(value)}")
            await websocket.send(json.dumps({"type": "error", "message": "Unsupported value type"}))
            return

        try:
            self.storage.update_state(key, value)
            print(f"Updated state: {key} = {value}")
        except Exception as e:
            print(f"Error updating state: {e}")
            await websocket.send(json.dumps({"type": "error", "message": "Failed to update state"}))
