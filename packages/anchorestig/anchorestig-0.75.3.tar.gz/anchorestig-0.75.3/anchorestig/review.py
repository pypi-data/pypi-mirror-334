import json
import os
import subprocess as sp

def validate_file(file_path):
    if not os.path.isfile(file_path):
        print("Error: File does not exist.")
        return False

    if not file_path.lower().endswith('.json'):
        print("Error: File does not have a .json extension.")
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json.load(file)
        return True
    except json.JSONDecodeError:
        print("Error: File contains invalid JSON.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def create_output_rollup(output_file_path):
    review_command = ["saf", "view", "summary", "-i", output_file_path, "-r"]
    try:
        # Run the chosen installation command
        result = sp.run(review_command, capture_output=True, text=True)
        print(result.stdout)
    except sp.CalledProcessError as e:
        print(f"Failed to output document review: {e}")