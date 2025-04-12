import json
from pathlib import Path
from threading import RLock

class DynamicStorage:
    def __init__(self, base_directory):
        self.base_directory = Path(base_directory)
        self.base_directory.mkdir(parents=True, exist_ok=True)
        self.lock = RLock()

    def handle_request(self, request):
        request_type = request.get('type')
        file_name = request.get('fileName')
        if not file_name:
            return {"error": "File name is required in the request."}

        file_path = self.base_directory / file_name

        if request_type == 'get':
            return self.get_file_content(file_path)
        elif request_type == 'set':
            file_content = request.get('fileContent')
            if file_content is None:
                return {"error": "File content is required for 'set' requests."}
            self.set_file_content(file_path, file_content)
            return {"status": "success"}
        else:
            return {"error": f"Unsupported request type: {request_type}"}

    def set_file_content(self, file_path, file_content):
        with self.lock:
            try:
                # Ensure the file path is within the user folder/WSCADA/files
                user_files_directory = self.base_directory / "files"
                user_files_directory.mkdir(parents=True, exist_ok=True)
                safe_file_path = user_files_directory / file_path.name

                with open(safe_file_path, 'w') as file:
                    json.dump(file_content, file, indent=4)
            except Exception as e:
                print(f"Error writing to file {file_path}: {e}")

    def get_file_content(self, file_path):
        with self.lock:
            try:
                # Ensure the file path is within the user folder/WSCADA/files
                user_files_directory = self.base_directory / "files"
                safe_file_path = user_files_directory / file_path.name

                if not safe_file_path.exists():
                    return {"error": "File not found."}

                with open(safe_file_path, 'r') as file:
                    try:
                        return {"content": json.load(file)}
                    except json.JSONDecodeError:
                        return {"error": "Failed to decode JSON content."}
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                return {"error": "Unexpected error occurred."}
