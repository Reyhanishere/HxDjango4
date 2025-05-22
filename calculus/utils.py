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

def find_LMS_whole(
    weight,
    height,
    gender,
    age_months,
):
    age_key = str(age_months)
    bmi = weight / ((height / 100) ** 2)
    if age_key in weight_data[gender]:
        LW, MW, SW = weight_data[gender][age_key]
        LHe, MHe, SHe = length_data[gender][age_key]
        LB, MB, SB = bmi_data[gender][age_key]

        z_score_w = calculate_z_score(weight, LW, MW, SW)
        z_score_he = calculate_z_score(height, LHe, MHe, SHe)
        z_score_b = calculate_z_score(bmi, LB, MB, SB)

        average_z_score_w = z_score_w
        average_z_score_he = z_score_he
        average_z_score_b = z_score_b

        # if int(hc) and age_months<=36:            
        #     LHc, MHc, SHc = head_circumference_data[gender][age_key]
        #     z_score_hc = calculate_z_score(hc, LHc, MHc, SHc)
        #     average_z_score_hc = z_score_hc

    else:
        lower_age = str(age_months - 0.5)
        upper_age = str(age_months + 0.5)

        try:
            LW_lower, MW_lower, SW_lower = weight_data[gender][lower_age]
            LW_upper, MW_upper, SW_upper = weight_data[gender][upper_age]
            
            LHe_lower, MHe_lower, SHe_lower = length_data[gender][lower_age]
            LHe_upper, MHe_upper, SHe_upper = length_data[gender][upper_age]
            
            LB_lower, MB_lower, SB_lower = bmi_data[gender][lower_age]
            LB_upper, MB_upper, SB_upper = bmi_data[gender][upper_age]
        
            # if int(hc) and age_months<=36:            
            #     LHc_lower, MHc_lower, SHc_lower = head_circumference_data[gender][lower_age]
            #     LHc_upper, MHc_upper, SHc_upper = head_circumference_data[gender][upper_age]
            
        except KeyError:
            return JsonResponse(
                {"error": "No data found for the nearest ages."}, status=404
            )

        z_score_lower_w = calculate_z_score(weight, LW_lower, MW_lower, SW_lower)
        z_score_upper_w = calculate_z_score(weight, LW_upper, MW_upper, SW_upper)
        average_z_score_w = round(((z_score_lower_w + z_score_upper_w) / 2), 2)


        z_score_lower_he = calculate_z_score(height, LHe_lower, MHe_lower, SHe_lower)
        z_score_upper_he = calculate_z_score(height, LHe_upper, MHe_upper, SHe_upper)
        average_z_score_he = round(((z_score_lower_he + z_score_upper_he) / 2), 2)


        z_score_lower_b = calculate_z_score(bmi, LB_lower, MB_lower, SB_lower)
        z_score_upper_b = calculate_z_score(bmi, LB_upper, MB_upper, SB_upper)
        average_z_score_b = round(((z_score_lower_b + z_score_upper_b) / 2), 2)

        # if int(hc) and age_months<=36:            
        #     z_score_lower_hc = calculate_z_score(hc, LHc_lower, MHc_lower, SHc_lower)
        #     z_score_upper_hc = calculate_z_score(hc, LHc_upper, MHc_upper, SHc_upper)
        #     average_z_score_hc = round(((z_score_lower_hc + z_score_upper_hc) / 2), 2)
        #     percentile_hc = percentile_calculator(average_z_score_hc)
        # else:
        #     average_z_score_hc = None
        #     percentile_hc = None


    percentile_w = percentile_calculator(average_z_score_w)
    percentile_he = percentile_calculator(average_z_score_he)
    percentile_b = percentile_calculator(average_z_score_b)

    return JsonResponse(
        {"weight": {
            "value": weight,
            "z_score": round(average_z_score_w, 2),
            "percentile": percentile_w
            },
        "height": {
            "value": height,
            "z_score": round(average_z_score_he, 2),
            "percentile": percentile_he
            },
        "bmi": {
            "value": bmi,
            "z_score": round(average_z_score_b, 2),
            "percentile": percentile_b
            }
        }
    )
