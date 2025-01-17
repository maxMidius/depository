import streamlit as st
import websockets

async def connect_websocket(topic):
    async with websockets.connect(f"ws://localhost:8000/ws/{topic}") as websocket:
        await websocket.send("Hello from Streamlit!")
        while True:
            message = await websocket.recv()
            st.write(message)

def main():
    st.title("WebSocket Client")
    topic = st.text_input("Topic")
    if st.button("Connect"):
        asyncio.run(connect_websocket(topic))
