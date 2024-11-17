import asyncio
import websockets
import json
import random
from datetime import datetime

async def send_data(websocket):
  """Send random data to client"""
  try:
      while True:
          # Generate sample data
          data = {
              "timestamp": datetime.now().isoformat(),
              "value": random.uniform(0, 100),
              "sensor": f"sensor_{random.randint(1,5)}"
          }
          
          # Send data
          await websocket.send(json.dumps(data))
          
          # Wait before sending next data
          await asyncio.sleep(1)
  except websockets.exceptions.ConnectionClosed:
      print("Client disconnected")

async def handler(websocket, path):
  """Handle client connection"""
  print("Client connected")
  await send_data(websocket)

async def main():
  async with websockets.serve(handler, "localhost", 8765):
      await asyncio.Future()  # run forever

if __name__ == "__main__":
  asyncio.run(main())
