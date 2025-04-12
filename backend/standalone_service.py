import asyncio
import threading
from base_service import BaseService

class StandaloneService(BaseService):
    def run_service(self):
        print("Running in standalone mode...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Start WebSocket server
        server_thread = threading.Thread(target=loop.run_until_complete, args=(self.start_websocket_server(),))
        server_thread.start()

        # Start taskbar icon with the event loop
        self.create_taskbar_icon(loop)
        self.start_taskbar_icon()

        # Keep running
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("Standalone mode stopped.")
