#!/bin/env python
#------------------------------------
import streamlit as st
import pandas as pd
import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer

# Title of the Streamlit app
st.title("Data Visualization with PygWalker")

# File uploader to upload a CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)

    # Check the file size
    file_size = uploaded_file.size
    if file_size > 1 * 1024 * 1024 * 1024:  # 1 Gigabyte
        st.error("File size exceeds 1 Gigabyte. Please upload a smaller file.")
    else:
        # Display the dataframe using PygWalker
        st.write("Dataframe:")
        #st.write(df)

        st.write("PygWalker Visualization:")
        pygApp = StreamlitRenderer(df)
        pygApp.explorer()
        
