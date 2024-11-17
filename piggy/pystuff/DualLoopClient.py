import asyncio
import websockets
import datetime
import logging
from typing import Optional

# Set up logging
logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DualLoopClient:
  def __init__(self, websocket_url: str = "ws://localhost:8000/ws"):
      self.websocket_url = websocket_url
      self.websocket: Optional[websockets.WebSocketClientProtocol] = None
      self.running = False
      self.last_received_data = None

  async def display_time(self):
      """Loop that displays current time every 5 seconds"""
      while self.running:
          current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          logger.info(f"Current Time: {current_time}")
          if self.last_received_data:
              logger.info(f"Last received data: {self.last_received_data}")
          await asyncio.sleep(5)

  async def websocket_listener(self):
      """Loop that handles WebSocket connection and data reception"""
      while self.running:
          try:
              if not self.websocket:
                  # Connect to WebSocket server
                  self.websocket = await websockets.connect(self.websocket_url)
                  logger.info("Connected to WebSocket server")

              # Receive data
              data = await self.websocket.recv()
              self.last_received_data = data
              logger.info(f"Received WebSocket data: {data}")

          except websockets.ConnectionClosed:
              logger.warning("WebSocket connection closed. Attempting to reconnect...")
              self.websocket = None
              await asyncio.sleep(5)  # Wait before reconnecting
          except Exception as e:
              logger.error(f"WebSocket error: {e}")
              self.websocket = None
              await asyncio.sleep(5)  # Wait before reconnecting

  async def start(self):
      """Start both loops concurrently"""
      self.running = True
      # Create tasks for both loops
      time_task = asyncio.create_task(self.display_time())
      websocket_task = asyncio.create_task(self.websocket_listener())
      
      # Wait for both tasks
      await asyncio.gather(time_task, websocket_task)

  async def stop(self):
      """Stop both loops and cleanup"""
      self.running = False
      if self.websocket:
          await self.websocket.close()
          self.websocket = None
      logger.info("Client stopped")

async def main():
  # Create client instance
  client = DualLoopClient()
  
  try:
      # Start the client
      await client.start()
  except KeyboardInterrupt:
      logger.info("Received keyboard interrupt")
  finally:
      # Cleanup
      await client.stop()

if __name__ == "__main__":
  asyncio.run(main())
