from standalone_service import StandaloneService
from windows_service import WebSocketService

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "standalone":
        standalone_service = StandaloneService()
        standalone_service.run_service()
    else:
        win32serviceutil.HandleCommandLine(WebSocketService)
