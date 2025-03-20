import yaml
import os


def read_config():
    file_path = "./config.yaml"

    if not os.path.exists(file_path):
        return {}

    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file) or {}
    except Exception as e:
        print(f"Error reading config file: {e}")
        return {}
