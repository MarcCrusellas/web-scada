import asyncio
import threading
import websockets
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

class BaseService:
    def __init__(self):
        self.websocket_clients = set()  # Track connected WebSocket clients
        self.icon = None

    def create_taskbar_icon(self, loop):
        def create_image():
            # Create a simple icon
            image = Image.new('RGB', (64, 64), color=(255, 255, 255))
            draw = ImageDraw.Draw(image)
            draw.rectangle((16, 16, 48, 48), fill=(0, 0, 255))
            return image

        def send_notification():
            print("Sending notification from taskbar icon...")
            if self.websocket_clients:
                for client in self.websocket_clients:
                    try:
                        asyncio.run_coroutine_threadsafe(client.send("notification:Taskbar notification"), loop)
                    except Exception as e:
                        print(f"Failed to send notification: {e}")
            else:
                print("No connected WebSocket clients.")

        def exit_service():
            print("Exiting service from taskbar icon...")
            if self.icon:
                self.icon.stop()

        menu = Menu(
            MenuItem("Send Notification", send_notification),
            MenuItem("Exit", exit_service)
        )
        self.icon = Icon("WebSocketService", create_image(), menu=menu)

    def start_taskbar_icon(self):
        def run_icon():
            self.icon.run()

        icon_thread = threading.Thread(target=run_icon)
        icon_thread.daemon = True
        icon_thread.start()

    async def websocket_handler(self, websocket):
        print("Client connected")
        self.websocket_clients.add(websocket)
        try:
            async for message in websocket:
                if message == 'hello':
                    print("Hello World")
                elif message == 'notify':
                    await websocket.send("notification:This is a notification from the server!")
                else:
                    print(f"Received: {message}")
        except websockets.ConnectionClosed:
            print("Client disconnected")
        finally:
            self.websocket_clients.remove(websocket)

    async def start_websocket_server(self):
        async with websockets.serve(self.websocket_handler, "localhost", 8080):
            print("WebSocket server started on ws://localhost:8080")
            await asyncio.Future()  # Run forever
