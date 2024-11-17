import streamlit as st
import asyncio
import time

def poll_data():
    while True:
        # Simulate fetching data from an API or database
        new_data = fetch_data_from_api()
        st.session_state.data = new_data
        time.sleep(5)  # Adjust polling interval as needed

async def main():
    if "data" not in st.session_state:
        st.session_state.data = []

    st.write(st.session_state.data)

    # Start the polling task in the background
    asyncio.create_task(poll_data())

if __name__ == "__main__":
    main()
