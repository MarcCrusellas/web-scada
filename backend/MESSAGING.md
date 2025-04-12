# Messaging Protocol for DynamicStorage

This document outlines the messaging protocol for interacting with the `DynamicStorage` class. It is intended for both frontend and backend teams to ensure seamless communication.

## Message Types

### 1. `get`
- **Description**: Retrieves the content of a specified file.
- **Request Format**:
  ```json
  {
    "type": "get",
    "fileName": "<file_name>"
  }
  ```
- **Response Format**:
  - **Success**:
    ```json
    {
      "content": { <file_content> }
    }
    ```
  - **Error**:
    ```json
    {
      "error": "File not found."
    }
    ```

### 2. `set`
- **Description**: Saves the provided content to a specified file.
- **Request Format**:
  ```json
  {
    "type": "set",
    "fileName": "<file_name>",
    "fileContent": { <file_content> }
  }
  ```
- **Response Format**:
  - **Success**:
    ```json
    {
      "status": "success"
    }
    ```
  - **Error**:
    ```json
    {
      "error": "File content is required for 'set' requests."
    }
    ```

## Error Handling
- If a required field is missing, the service will send an error response instead of raising an exception to ensure continuity.
- Example:
  ```json
  {
    "error": "File name is required in the request."
  }

## Notes
- All file paths are relative to the base directory specified during the initialization of the `DynamicStorage` class.
- Ensure that all JSON content is properly formatted to avoid serialization errors.

---

## Attached Class

```python
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

    def get_file_content(self, file_path):
        with self.lock:
            if not file_path.exists():
                return {"error": "File not found."}
            with open(file_path, 'r') as file:
                try:
                    return {"content": json.load(file)}
                except json.JSONDecodeError:
                    return {"error": "Failed to decode JSON content."}

    def set_file_content(self, file_path, file_content):
        with self.lock:
            with open(file_path, 'w') as file:
                json.dump(file_content, file, indent=4)
```
