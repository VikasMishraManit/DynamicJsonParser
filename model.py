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

def json_to_csv(json_files, output_file):
    """Converts multiple nested JSON files to a CSV format with hierarchical column names and multiple rows for arrays."""
    all_rows = []

    for json_file in json_files:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, dict):
                data = [data]

            for entry in data:
                all_rows.extend(flatten_json(entry))

    df = pd.DataFrame(all_rows)
    df.to_csv(output_file, index=False)
    print(f"CSV file saved to {output_file}")

# Example usage
json_folder = "./json_files/"  # Replace with the folder containing JSON files
csv_output_file = "output_combined.csv"

# Get all JSON files in the folder
json_files = glob.glob(os.path.join(json_folder, "*.json"))

# Convert JSON files to CSV
json_to_csv(json_files, csv_output_file)
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

def json_to_csv(json_files, output_file):
    """Converts multiple nested JSON files to a CSV format with hierarchical column names and multiple rows for arrays."""
    all_rows = []

    for json_file in json_files:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, dict):
                data = [data]

            for entry in data:
                all_rows.extend(flatten_json(entry))

    df = pd.DataFrame(all_rows)
    df.to_csv(output_file, index=False)
    print(f"CSV file saved to {output_file}")

# Example usage
json_folder = "./json_files/"  # Replace with the folder containing JSON files
csv_output_file = "output_combined.csv"

# Get all JSON files in the folder
json_files = glob.glob(os.path.join(json_folder, "*.json"))

# Convert JSON files to CSV
json_to_csv(json_files, csv_output_file)
