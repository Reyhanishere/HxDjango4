import json, math

from django.http import JsonResponse
import os

def load_pedi_growth_recommendations():
    json_file_path = os.path.join(
        os.path.dirname(__file__), "../static/data/full_growth_recommendations_bilingual.json"
    )
    with open(json_file_path, "r", encoding='utf-8') as file:
        return json.load(file)


def determine_zscore(zs):
    if zs < -2:
        return 'low'
    elif zs > 2:
        return 'high'
    else:
        return 'normal'


growth_recom_data = load_pedi_growth_recommendations()

def make_recom_and_considers(age_months, last_record):
    if age_months <= 6:
        age_title = '0-6_months'
    elif age_months <= 24:
        age_title = '6_months_to_2_years'
    else:
        age_title = 'above_2_years'

    considerations = {'وزن':[], 'قد':[], 'BMI':[]}
    recommendations = {'وزن':[], 'قد':[], 'BMI':[]}

    for c in growth_recom_data[age_title]['weight'][determine_zscore(last_record.weight_z)]['consider']:
        considerations['وزن'].append(c['fa'])
    for r in growth_recom_data[age_title]['weight'][determine_zscore(last_record.weight_z)]['tell']:
        recommendations['وزن'].append(r['fa'])
    for c in growth_recom_data[age_title]['height'][determine_zscore(last_record.height_z)]['consider']:
        considerations['قد'].append(c['fa'])
    for r in growth_recom_data[age_title]['height'][determine_zscore(last_record.height_z)]['tell']:
        recommendations['قد'].append(r['fa'])
    if age_months >= 24:
        for c in growth_recom_data[age_title]['bmi'][determine_zscore(last_record.bmi_z)]['consider']:
            considerations['BMI'].append(c['fa'])
        for r in growth_recom_data[age_title]['bmi'][determine_zscore(last_record.bmi_z)]['tell']:
            recommendations['BMI'].append(r['fa'])
    return considerations, recommendations

# _____________________________________ #

def load_pedi_weight_data():
    json_file_path = os.path.join(
        os.path.dirname(__file__), "../static/data/weight_MLS_0-240.json"
    )
    with open(json_file_path, "r") as file:
        return json.load(file)


weight_data = load_pedi_weight_data()

#### ------------------ ####


def load_pedi_length_data():
    json_file_path = os.path.join(
        os.path.dirname(__file__), "../static/data/length_MLS_0-240.json"
    )
    with open(json_file_path, "r") as file:
        return json.load(file)


length_data = load_pedi_length_data()

#### ------------------ ####


def load_pedi_head_circumference_data():
    json_file_path = os.path.join(
        os.path.dirname(__file__), "../static/data/head_circumference_LMS_0-36.json"
    )
    with open(json_file_path, "r") as file:
        return json.load(file)


head_circumference_data = load_pedi_head_circumference_data()


def load_pedi_bmi_data():
    json_file_path = os.path.join(
        os.path.dirname(__file__), "../static/data/bmi_LMS_24-240.json"
    )
    with open(json_file_path, "r") as file:
        return json.load(file)


bmi_data = load_pedi_bmi_data()

#### ------------------ ####


def load_z_score_table():
    json_file_path = os.path.join(
        os.path.dirname(__file__), "../static/data/z_table_abstract.json"
    )
    with open(json_file_path, "r") as file:
        return json.load(file)


z_score_table_data = load_z_score_table()

#### ------------------ ####


def calculate_z_score(X, L, M, S):
    if L == 0:
        return (math.log(X / M)) / S
    else:
        return ((X / M) ** L - 1) / (L * S)


def percentile_calculator(z_score):
    if z_score < -3.9:
        percentile = 0
    elif z_score > 3.9:
        percentile = 100
    else:
        percentile = z_score_table_data[str(round(z_score, 1))]
        percentile = round(float(percentile) * 100, 1)
    return percentile

def find_LMS_whole(
    weight,
    height,
    gender,
    age_months,
    hc=0,
):
    age_key = str(age_months)
    bmi = weight / ((height / 100) ** 2)
    bmi = round(bmi, 2)

    if age_key in weight_data[gender]:
        LW, MW, SW = weight_data[gender][age_key]
        z_score_w = calculate_z_score(weight, LW, MW, SW)
        
    if age_key in length_data[gender]:
        LHe, MHe, SHe = length_data[gender][age_key]
        z_score_he = calculate_z_score(height, LHe, MHe, SHe)

        if age_months>=24:
            LB, MB, SB = bmi_data[gender][age_key]
            z_score_b = calculate_z_score(bmi, LB, MB, SB)
            average_z_score_b = z_score_b
            percentile_b = percentile_calculator(average_z_score_b)
        else:
            average_z_score_b = 0
            percentile_b = 50

        average_z_score_w = z_score_w
        average_z_score_he = z_score_he

        if int(hc) and hc!=0 and age_months<=36:            
            LHc, MHc, SHc = head_circumference_data[gender][age_key]
            z_score_hc = calculate_z_score(hc, LHc, MHc, SHc)
            average_z_score_hc = z_score_hc
            percentile_hc = percentile_calculator(average_z_score_hc)

        else:
            average_z_score_hc = 0
            percentile_hc = 50

    else:
        lower_age = str(age_months - 0.5)
        upper_age = str(age_months + 0.5)

        try:
            LW_lower, MW_lower, SW_lower = weight_data[gender][lower_age]
            LW_upper, MW_upper, SW_upper = weight_data[gender][upper_age]
            
            LHe_lower, MHe_lower, SHe_lower = length_data[gender][lower_age]
            LHe_upper, MHe_upper, SHe_upper = length_data[gender][upper_age]
            if age_months>=24:
                LB_lower, MB_lower, SB_lower = bmi_data[gender][lower_age]
                LB_upper, MB_upper, SB_upper = bmi_data[gender][upper_age]
        
            if int(hc) and hc!=0 and age_months<=36:            
                LHc_lower, MHc_lower, SHc_lower = head_circumference_data[gender][lower_age]
                LHc_upper, MHc_upper, SHc_upper = head_circumference_data[gender][upper_age]
            
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

        if age_months>=24:
            z_score_lower_b = calculate_z_score(bmi, LB_lower, MB_lower, SB_lower)
            z_score_upper_b = calculate_z_score(bmi, LB_upper, MB_upper, SB_upper)
            average_z_score_b = round(((z_score_lower_b + z_score_upper_b) / 2), 2)
            percentile_b = percentile_calculator(average_z_score_b)
        else:
            average_z_score_b = 0
            percentile_b = 50

        if int(hc) and hc!=0 and age_months<=36:            
            z_score_lower_hc = calculate_z_score(hc, LHc_lower, MHc_lower, SHc_lower)
            z_score_upper_hc = calculate_z_score(hc, LHc_upper, MHc_upper, SHc_upper)
            average_z_score_hc = round(((z_score_lower_hc + z_score_upper_hc) / 2), 2)
            percentile_hc = percentile_calculator(average_z_score_hc)
        else:
            average_z_score_hc = 0
            percentile_hc = 50


    percentile_w = percentile_calculator(average_z_score_w)
    percentile_he = percentile_calculator(average_z_score_he)

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
            },
        "hc": {
            "value": hc,
            "z_score": round(average_z_score_hc, 2),
            "percentile": percentile_hc
            }
        }
    )
