import os
import json

# Function that loads the configuration file
def load_config():    
    # Determine the path of the configuration file
    config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
    config_file_path = os.path.abspath(config_file_path)
    # Read and load the configuration file as JSON
    with open(config_file_path, 'r', encoding="utf-8") as config_file:
        return json.load(config_file)