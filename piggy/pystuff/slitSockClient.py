import streamlit as st
import websockets
import asyncio
import json
import time
from datetime import datetime

# Initialize session state
if 'websocket' not in st.session_state:
  st.session_state.websocket = None
if 'messages' not in st.session_state:
  st.session_state.messages = []
if 'connected' not in st.session_state:
  st.session_state.connected = False

async def connect_websocket():
  """Establish WebSocket connection"""
  try:
      websocket = await websockets.connect('ws://localhost:8765')
      st.session_state.websocket = websocket
      st.session_state.connected = True
      return True
  except Exception as e:
      st.error(f"Connection failed: {e}")
      st.session_state.connected = False
      return False

async def disconnect_websocket():
  """Close WebSocket connection"""
  if st.session_state.websocket:
      await st.session_state.websocket.close()
      st.session_state.websocket = None
      st.session_state.connected = False

async def receive_message():
  """Receive message from WebSocket"""
  if st.session_state.websocket:
      try:
          message = await st.session_state.websocket.recv()
          data = json.loads(message)
          timestamp = datetime.now().strftime("%H:%M:%S")
          st.session_state.messages.append(f"{timestamp} - {data}")
      except Exception as e:
          st.error(f"Error receiving message: {e}")
          await disconnect_websocket()

def main():
  st.title("WebSocket Data Viewer")

  # Connection controls
  col1, col2 = st.columns(2)
  with col1:
      if st.button("Connect" if not st.session_state.connected else "Disconnect"):
          if not st.session_state.connected:
              asyncio.run(connect_websocket())
          else:
              asyncio.run(disconnect_websocket())

  with col2:
      st.write("Status:", "Connected" if st.session_state.connected else "Disconnected")

  # Display messages
  st.subheader("Received Messages")
  message_container = st.empty()

  # Auto-refresh messages
  if st.session_state.connected:
      asyncio.run(receive_message())

  # Display messages in reverse chronological order
  messages = "\n".join(reversed(st.session_state.messages[-10:]))  # Show last 10 messages
  message_container.code(messages)

  # Clear messages button
  if st.button("Clear Messages"):
      st.session_state.messages = []

if __name__ == "__main__":
  main()
