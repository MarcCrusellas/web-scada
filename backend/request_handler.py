import json

class RequestHandler:
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

        # Check if storage is initialized
        if not self.storage:
            print("Storage is not initialized.")
            await websocket.send(json.dumps({"type": "error", "message": "Storage not initialized"}))
            return

        # Validate the value type
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

    async def handle_unsupported(self, websocket, data):
        print(f"Unsupported message type: {data.get('type')}")
        await websocket.send(json.dumps({"type": "error", "message": "Unsupported message type"}))

    async def handle_request(self, websocket, message):
        try:
            print(f"Received message: {message}")
            data = json.loads(message)
            print(f"Parsed message data: {data}")
            if data['type'] == 'fetch':
                print("Handling fetch request...")
                await self.handle_fetch(websocket, data)
                print("Fetch request handled successfully.")
            elif data['type'] == 'update':
                print("Handling update request...")
                await self.handle_update(websocket, data)
                print("Update request handled successfully.")
            else:
                print(f"Unsupported message type: {data['type']}")
                await self.handle_unsupported(websocket, data)
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Invalid message received: {e}")
            await websocket.send(json.dumps({"type": "error", "message": "Invalid message format"}))
        except Exception as e:
            print(f"Unexpected error: {e}")
            await websocket.send(json.dumps({"type": "error", "message": "Internal server error"}))
        finally:
            print("Exiting handle_request method.")
