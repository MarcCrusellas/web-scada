import asyncio
import threading
import websockets
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import json
from pathlib import Path
from storage.in_memory_storage import InMemoryStorage
from state_handler import StateHandler
from dynamic_storage import DynamicStorage
import logging
from msg.msg_srv import MessageService

# Add logging setup
logger = logging.getLogger("BaseService")
logger.setLevel(logging.DEBUG)

# Add a handler for console output
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

class BaseService:
    def __init__(self):
        self.websocket_clients = set()
        self.icon = None

    def create_taskbar_icon(self, loop):
        try:
            def create_image():
                # Create a simple icon
                image = Image.new('RGB', (64, 64), color=(255, 255, 255))
                draw = ImageDraw.Draw(image)
                draw.rectangle((16, 16, 48, 48), fill=(0, 0, 255))
                return image

            def send_notification():
                if self.websocket_clients:
                    for client in self.websocket_clients:
                        try:
                            asyncio.run_coroutine_threadsafe(client.send("notification:Taskbar notification"), loop)
                        except Exception as e:
                            logger.error(f"Failed to send notification: {e}")
                else:
                    logger.warning("No connected WebSocket clients.")

            def exit_service():
                logger.info("Exiting service from taskbar icon...")
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
                logger.info("Starting data transmission...")
                self.transmitting = True
                asyncio.run_coroutine_threadsafe(self.generate_fake_data(), loop)
                self.update_taskbar_menu()

            def stop_transmission():
                logger.info("Stopping data transmission...")
                self.transmitting = False
                self.update_taskbar_menu()

            self.update_taskbar_menu = update_taskbar_menu
            self.icon = Icon("WebSocketService", create_image(), menu=Menu())
            self.update_taskbar_menu()
        except Exception as e:
            logger.error(f"Failed to initialize taskbar icon: {e}")

    def start_taskbar_icon(self):
        def run_icon():
            self.icon.run()

        icon_thread = threading.Thread(target=run_icon)
        icon_thread.daemon = True
        icon_thread.start()

    async def websocket_handler(self, websocket):
        self.websocket_clients.add(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                response = MessageService.handle_message(data)
                await websocket.send(json.dumps(response))
        except websockets.ConnectionClosed:
            logger.info("WebSocket connection closed.")
        finally:
            self.websocket_clients.remove(websocket)

    async def start_websocket_server(self):
        async with websockets.serve(self.websocket_handler, "localhost", 8080):
            print("WebSocket server started on ws://localhost:8080")
            await asyncio.Future()

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


