import streamlit as st
import pandas as pd
import os
from model import json_to_csv

st.title("Deploying model.py - JSON to CSV Converter")
st.write("Upload your JSON files to flatten and convert them into a CSV format.")

uploaded_files = st.file_uploader("Upload JSON Files", type=["json"], accept_multiple_files=True)

if uploaded_files:
    json_files = []
    output_file = "output_combined.csv"

    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        temp_file = f"temp_{uploaded_file.name}"
        with open(temp_file, 'wb') as f:
            f.write(bytes_data)
        json_files.append(temp_file)

    # Call the function from model.py
    json_to_csv(json_files, output_file)

    # Load and display the CSV
    df = pd.read_csv(output_file)
    st.subheader("Preview of the Converted CSV")
    st.dataframe(df.head())

    # Provide download button
    st.download_button(
        label="Download CSV File",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="output_combined.csv",
        mime="text/csv"
    )

    # Clean up temporary files
    for file in json_files:
        os.remove(file)
