import asyncio
import threading
import win32serviceutil
import win32service
import win32event
import servicemanager
from base_service import BaseService

class WebSocketService(win32serviceutil.ServiceFramework, BaseService):
    _svc_name_ = "WebSocketService"
    _svc_display_name_ = "WebSocket Service with Taskbar Icon"
    _svc_description_ = "A WebSocket server with a taskbar icon for notifications."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        BaseService.__init__(self)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.is_stopping = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.is_stopping = True

    def SvcDoRun(self):
        servicemanager.LogInfoMsg("WebSocket Service is starting...")
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)

        try:
            self.run_service()
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            servicemanager.LogInfoMsg("WebSocket Service is running.")
        except Exception as e:
            servicemanager.LogErrorMsg(f"WebSocket Service failed to start: {e}")
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def run_service(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Start WebSocket server in a separate thread
        server_thread = threading.Thread(target=loop.run_until_complete, args=(self.start_websocket_server(),))
        server_thread.start()

        # Start taskbar icon with the event loop
        self.create_taskbar_icon(loop)
        self.start_taskbar_icon()

        # Wait for stop event
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
        self.is_stopping = True
        loop.stop()
        server_thread.join()
