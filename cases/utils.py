import json, math

from django.http import JsonResponse
import os

def load_pedi_weight_data():
    json_file_path = os.path.join(os.path.dirname(__file__), '../static/data/weight_MLS_0-240.json')
    with open(json_file_path, 'r') as file:
        return json.load(file)

weight_data = load_pedi_weight_data()

#### ------------------ ####

def load_pedi_length_data():
    json_file_path = os.path.join(os.path.dirname(__file__), '../static/data/length_MLS_0-240.json')
    with open(json_file_path, 'r') as file:
        return json.load(file)

length_data = load_pedi_length_data()

#### ------------------ ####

def load_pedi_head_circumference_data():
    json_file_path = os.path.join(os.path.dirname(__file__), '../static/data/head_circumference_LMS_0-36.json')
    with open(json_file_path, 'r') as file:
        return json.load(file)

head_circumference_data = load_pedi_head_circumference_data()

def load_pedi_bmi_data():
    json_file_path = os.path.join(os.path.dirname(__file__), '../static/data/bmi_LMS_24-240.json')
    with open(json_file_path, 'r') as file:
        return json.load(file)

bmi_data = load_pedi_bmi_data()

#### ------------------ ####

def load_z_score_table():
    json_file_path = os.path.join(os.path.dirname(__file__), '../static/data/z_table_abstract.json')
    with open(json_file_path, 'r') as file:
        return json.load(file)

z_score_table_data = load_z_score_table()

#### ------------------ ####

def calculate_z_score(X, L, M, S):
    if L == 0:
        return ((math.log(X / M)) / S)
    else:
        return (((X / M) ** L - 1) / (L * S))
    
def find_LMS(value, data_set, gender, age_months,):
    age_key = str(age_months)
    if age_key in data_set[gender]:
        L, M, S = data_set[gender][age_key]
        z_score = calculate_z_score(value, L, M, S)
        average_z_score=z_score

    else:
        lower_age = str(age_months - 0.5)
        upper_age = str(age_months + 0.5)

        try:
            L_lower, M_lower, S_lower = data_set[gender][lower_age]
            L_upper, M_upper, S_upper = data_set[gender][upper_age]
        except KeyError:
            return JsonResponse({'error': 'No data found for the nearest ages.'}, status=404)

        z_score_lower = calculate_z_score(value, L_lower, M_lower, S_lower)
        z_score_upper = calculate_z_score(value, L_upper, M_upper, S_upper)

        average_z_score = round(((z_score_lower + z_score_upper) / 2), 2)
    
    if average_z_score < -3.9:
        percentile = 0
    elif average_z_score > 3.9:
        percentile=100
    else:
        percentile = z_score_table_data[str(round(average_z_score, 1))]
        percentile = round(float(percentile)*100,1)
    return JsonResponse({'value':value,
                        'z_score': round(average_z_score, 2),
                        'percentile': percentile})
