from .json_key_handler import JsonKeyHandler
from .json_file_handler import JsonFileHandler

class MessageService:

    @staticmethod
    def handle_message(message):
        # get uuid from message
        uuid = message.get('uuid')
        if uuid is None:
            return {"type": "error", "message": "UUID not found in message."}
        match message['type']:
            case 'json-key':
                return JsonKeyHandler.handle_json_key(message.get('args'), uuid)
            case 'file-content':
                return JsonFileHandler.handle_json_file(message.get('args'), uuid)
            case _:
                return {"type": "error", "message": "Unsupported message type.", "uuid": uuid}

