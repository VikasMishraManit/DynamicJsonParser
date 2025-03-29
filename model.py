import streamlit as st
import pandas as pd
import json
import glob
import os

def flatten_json(nested_json, parent_key='', sep='.'):
    """Recursively flattens a nested JSON object into a list of dictionaries, handling arrays as multiple rows."""
    flattened_rows = []

    def recursive_flatten(obj, parent, row):
        if isinstance(obj, dict):
            for k, v in obj.items():
                recursive_flatten(v, parent + [(k, None)], row)
        elif isinstance(obj, list):
            if all(isinstance(item, (str, int, float)) for item in obj):
                key = sep.join(k for k, _ in parent)
                row[key] = ', '.join(map(str, obj))
            else:
                for item in obj:
                    new_row = row.copy()
                    recursive_flatten(item, parent, new_row)
                    flattened_rows.append(new_row)
        else:
            key = sep.join(k for k, _ in parent)
            row[key] = obj

    recursive_flatten(nested_json, [], {})
    return flattened_rows if flattened_rows else [{}]

def json_to_csv(json_files):
    """Converts multiple nested JSON files to a DataFrame."""
    all_rows = []

    for json_file in json_files:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, dict):
                data = [data]

            for entry in data:
                all_rows.extend(flatten_json(entry))

    return pd.DataFrame(all_rows)

st.title("JSON to CSV Converter")
st.write("Upload multiple JSON files to convert them into a single CSV file.")

uploaded_files = st.file_uploader("Upload JSON Files", type=["json"], accept_multiple_files=True)

if uploaded_files:
    json_files = []

    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        temp_file = f"temp_{uploaded_file.name}"
        with open(temp_file, 'wb') as f:
            f.write(bytes_data)
        json_files.append(temp_file)

    df = json_to_csv(json_files)

    st.subheader("Preview of the Flattened Data")
    st.dataframe(df.head())

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV File",
        data=csv,
        file_name="output_combined.csv",
        mime="text/csv"
    )

    # Clean up temporary files
    for file in json_files:
        os.remove(file)
