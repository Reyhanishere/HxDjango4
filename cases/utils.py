import json
import os

def load_pedi_weight_data():
    json_file_path = os.path.join(os.path.dirname(__file__), '../static/data/weight_MLS_0-240.json')
    with open(json_file_path, 'r') as file:
        return json.load(file)

weight_data = load_pedi_weight_data()
