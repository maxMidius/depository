from fastapi import FastAPI, WebSocket
import asyncio
import datetime
import json
import uvicorn
import random

app = FastAPI()

class DataGenerator:
  @staticmethod
  def generate_sample_data():
      """Generate sample data"""
      return {
          "timestamp": datetime.datetime.now().isoformat(),
          "sensor_id": f"SENSOR_{random.randint(1, 100)}",
          "temperature": round(random.uniform(20, 30), 2),
          "humidity": round(random.uniform(40, 80), 2)
      }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  try:
      while True:
          # Generate and send sample data
          data = DataGenerator.generate_sample_data()
          await websocket.send_json(data)
          # Wait for 2 seconds before sending next data
          await asyncio.sleep(2)
  except Exception as e:
      print(f"Error: {e}")

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
