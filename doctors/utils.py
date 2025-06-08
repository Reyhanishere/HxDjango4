import json #, math

# from django.http import JsonResponse
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
