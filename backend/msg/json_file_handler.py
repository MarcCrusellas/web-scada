import re
from pathlib import Path
from typing import Any

class JsonFileHandler:

    @staticmethod
    def handle_json_file(message_args, uuid):
        # Extracting arguments from the message
        project = message_args.get('project')
        file_name = message_args.get('file_name')
        operation_type = message_args.get('type')
        value = message_args.get('value')

        if not JsonFileHandler.is_valid_file_name(file_name):
            return {"type": "error", "message": f"Invalid file name: '{file_name}'.", "uuid": uuid}

        match operation_type:
            case 'get_file':
                return JsonFileHandler.get_file(project, file_name, uuid)
            case 'set_file':
                return JsonFileHandler.set_file(project, file_name, value, uuid)
            case _:
                return {"type": "error", "message": "Unsupported operation type.", "uuid": uuid}

    @staticmethod
    def get_file(project, file_name, uuid):
        try:
            file_path = Path.home() / "WSCADA" / project / file_name
            if not file_path.exists():
                return {"type": "error", "message": f"File '{file_name}' not found in project '{project}'.", "uuid": uuid}

            with open(file_path, 'r') as file:
                content = file.read()
            return {"type": "ok", "project": project, "file_name": file_name, "content": content, "uuid": uuid}
        except Exception as e:
            return {"type": "error", "message": f"Failed to read file '{file_name}': {e}", "uuid": uuid}

    @staticmethod
    def set_file(project, file_name, value, uuid):
        try:
            file_path = Path.home() / "WSCADA" / project / file_name
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w') as file:
                file.write(value)
            return {"type": "ok", "project": project, "file_name": file_name, "uuid": uuid}
        except Exception as e:
            return {"type": "error", "message": f"Failed to write to file '{file_name}': {e}", "uuid": uuid}
