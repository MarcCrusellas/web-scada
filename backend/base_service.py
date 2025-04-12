import asyncio
import threading
import websockets
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import json
from pathlib import Path

from request_handler import RequestHandler
from in_memory_storage import InMemoryStorage

class BaseService:
    def __init__(self):
        self.websocket_clients = set()  # Track connected WebSocket clients
        self.icon = None
        self.storage = InMemoryStorage(Path.home() / "WSCADA" / "state.json")

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

        self.transmitting = False

        def update_taskbar_menu():
            menu_items = [
                MenuItem("Send Notification", send_notification),
                MenuItem("Start Transmission", start_transmission, visible=not self.transmitting),
                MenuItem("Stop Transmission", stop_transmission, visible=self.transmitting),
                MenuItem("Exit", exit_service)
            ]
            self.icon.menu = Menu(*menu_items)

        def start_transmission():
            print("Starting data transmission...")
            self.transmitting = True
            asyncio.run_coroutine_threadsafe(self.generate_fake_data(), loop)
            self.update_taskbar_menu()

        def stop_transmission():
            print("Stopping data transmission...")
            self.transmitting = False
            self.update_taskbar_menu()

        self.update_taskbar_menu = update_taskbar_menu
        self.icon = Icon("WebSocketService", create_image(), menu=Menu())
        self.update_taskbar_menu()

    def start_taskbar_icon(self):
        def run_icon():
            self.icon.run()

        icon_thread = threading.Thread(target=run_icon)
        icon_thread.daemon = True
        icon_thread.start()

    async def websocket_handler(self, websocket):
        def log_websocket_event(event):
            print(f"WebSocket event: {event}")

        # Add logging to WebSocket events
        log_websocket_event("Client connected")
        self.websocket_clients.add(websocket)
        request_handler = RequestHandler(self.storage)
        try:
            async for message in websocket:
                await request_handler.handle_request(websocket, message)
        except websockets.ConnectionClosed:
            log_websocket_event("Client disconnected")
        finally:
            self.websocket_clients.remove(websocket)

    async def start_websocket_server(self):
        async with websockets.serve(self.websocket_handler, "localhost", 8080):
            print("WebSocket server started on ws://localhost:8080")
            await asyncio.Future()  # Run forever

    async def generate_fake_data(self):
        import random
        while self.transmitting:
            if self.websocket_clients:
                data = random.randint(1, 100)
                for client in self.websocket_clients:
                    try:
                        await client.send(f"data:{data}")
                    except Exception as e:
                        print(f"Failed to send data: {e}")
            else:
                print("No WebSocket clients connected.")
            await asyncio.sleep(1)

    def stop_service(self):
        print("Stopping service...")
        self.transmitting = False
        if self.icon:
            self.icon.stop()


