import json
import os

def load_pedi_weight_data():
    json_file_path = os.path.join(os.path.dirname(__file__), '../static/data/weight_MLS_0-240.json')
    with open(json_file_path, 'r') as file:
        return json.load(file)

weight_data = load_pedi_weight_data()

#### ------------------ ####

def load_z_score_table():
    json_file_path = os.path.join(os.path.dirname(__file__), '../static/data/z_table_abstract.json')
    with open(json_file_path, 'r') as file:
        return json.load(file)

z_score_table_data = load_z_score_table()

#### ------------------ ####
