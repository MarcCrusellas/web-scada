# Web SCADA Project

## Overview
This project consists of a frontend and a backend for a Web SCADA system. The backend includes a WebSocket server that can run as a standalone application or as a Windows service. The frontend is a simple web interface.

## Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- PyInstaller (for building executables)

## Setup
1. Clone the repository.
2. Navigate to the project directory.
3. Install dependencies:
   ```bash
   make install
   ```

## Running the Project
### Standalone Mode
To run the backend in standalone mode:
```bash
make run
```

### Build Executable
To build the backend as a standalone executable:
```bash
make build
```

### Clean Up
To clean up build artifacts:
```bash
make clean
```

## Frontend
Open `frontend/index.html` in a web browser to access the frontend interface.

## Features
See `FEATURES.md` for a detailed list of features.
