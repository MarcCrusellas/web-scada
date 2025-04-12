# Features

## Backend
- WebSocket server to handle real-time communication.
- Can run as a standalone application or as a Windows service.
- Taskbar icon with the following options:
  - **Send Notification**: Sends a notification to connected WebSocket clients.
  - **Exit**: Stops the service or standalone application.
- Handles multiple WebSocket clients simultaneously.

## Frontend
- Simple web interface with the following features:
  - **Send Hello**: Sends a "Hello World" message to the backend.
  - **Request Notification**: Requests a notification from the backend.
- Displays notifications received from the backend in the DOM.

## Build and Deployment
- `Makefile` for managing installation, building, running, and cleaning up.
- `requirements.txt` for dependency management.
- PyInstaller configuration for building standalone executables.
