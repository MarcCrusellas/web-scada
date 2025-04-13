### Get Set key
Get set key of a environment, environment are dynamic, but always json, so assing .json its not necesary
```json
{
    "type": "json-key",
    "args": {
        "env": "state", // usualy name of the file, in the base path 
        "type": "fetch", // "fetch" | "update"
        "key": "(any key)",
        "value": "(any value)" // if update
    }
}
```
### Get Set file
get set file content
```json
{
    "type": "file-content",
    "args": {
        "project": "", // project name, same as folder
        "file_name": "", // ^[\w,\s-]+\.[A-Za-z]{3}$
        "type": "get_file", // "get_file" | "set_file"
        "value": "(any value)" // if set_file
    }
}
```
### Error Handling
```json
{
    "type": "error",
    "message": "(error message)"
}
```
- **Description**: Sent when an unsupported message type is received or an error occurs.

## Notes
- The WebSocket server listens on `ws://localhost:8080`.
- All WebSocket messages are JSON-encoded.
- File operations are restricted to the `WSCADA/files` directory for security.