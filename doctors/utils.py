from datetime import date, timedelta
import json, math
import os

from django.http import JsonResponse

from .templatetags.tags import *

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

def load_wl_data():
    json_file_path = os.path.join(
        os.path.dirname(__file__), "../static/data/wfl_LMSP50_45-103.json"
    )
    with open(json_file_path, "r") as file:
        return json.load(file)


wl_data = load_wl_data()

#### ------------------ ####

def load_wps_data():
    json_file_path = os.path.join(
        os.path.dirname(__file__), "../static/data/weight_Ps_24-240.json"
    )
    with open(json_file_path, "r") as file:
        return json.load(file)


wps_data = load_wps_data()

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

def to_five(value):
    value *= 10
    value=round(value)
    while value % 5 != 0:
        value += 1
    return value / 10

def calculate_age_extended(birth_date):
    today = date.today()
    
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day
    
    # Adjust for negative months/days
    if days < 0:
        months -= 1
        # Get last day of previous month
        last_month = today.replace(day=1) - timedelta(days=1)
        days += last_month.day
    
    if months < 0:
        years -= 1
        months += 12

    if years==0:
        year_text=''
    else:
        year_text='{} سال و '.format(years)

    if months==0:
        month_text=''
    else:
        month_text='{} ماه و '.format(months)
    if days==0:
        day_text=''
    else:
        day_text='{} روز'.format(days)
    return year_text + month_text + day_text


def set_is_wl(last_record):
    is_wl=True
    last_height = last_record.height
    if last_height > 103.5 or last_height < 45:
        is_wl = False
    return is_wl

def set_recent_data(records, age, is_wl):
    final_list = []
    for r in records:
        data_temp_dict = {}
        data_temp_dict['date'] = j_date(r.record_date, 'name, long')
        data_temp_dict['weight'] = r.weight
        data_temp_dict['weight_z'] = r.weight_z
        data_temp_dict['weight_p'] = r.weight_p

        data_temp_dict['height'] = r.height
        data_temp_dict['height_z'] = r.height_z
        data_temp_dict['height_p'] = r.height_p

        data_temp_dict['hc'] = r.hc
        data_temp_dict['hc_z'] = r.hc_z
        data_temp_dict['hc_p'] = r.hc_p
        
        if age > 24:
            data_temp_dict['bmi'] = r.bmi
            data_temp_dict['bmi_z'] = r.bmi_z
            data_temp_dict['bmi_p'] = r.bmi_p

        if is_wl:
            data_temp_dict['wl_p50'] = r.wl_p50
            data_temp_dict['wl_z'] = r.wl_z
            data_temp_dict['wl_p'] = r.wl_p

        final_list.append(data_temp_dict)
    return final_list

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
    length = to_five(height) #####################

    if length >= 45 and length < 104: ######
        if str(length) in wl_data[gender]:
            LWL, MWL, SWL, P50WL = wl_data[gender][str(length)]
            z_score_wl = calculate_z_score(weight, LWL, MWL, SWL)
            average_z_score_wl = z_score_wl
            percentile_wl = percentile_calculator(average_z_score_wl)

        else:
            lower_length = length - 0.5
            upper_length = length + 0.5
            if str(lower_length) in wl_data[gender] and str(upper_length) in wl_data[gender]:
                LWL_lower, MWL_lower, SWL_lower, P50WL_lower = wl_data[gender][str(lower_length)]
                LWL_upper, MWL_upper, SWL_upper, P50WL_upper = wl_data[gender][str(upper_length)]
                z_score_lower_wl = calculate_z_score(weight, LWL_lower, MWL_lower, SWL_lower)
                z_score_upper_wl = calculate_z_score(weight, LWL_upper, MWL_upper, SWL_upper)
                P50WL = round(((P50WL_lower + P50WL_upper) / 2), 2)
                average_z_score_wl = round(((z_score_lower_wl + z_score_upper_wl) / 2), 2)
                percentile_wl = percentile_calculator(average_z_score_wl)
            else:
                P50WL = None
                average_z_score_wl = None
                percentile_wl = None
    else:
        P50WL = None
        average_z_score_wl = None
        percentile_wl = None
    
    if age_key in weight_data[gender]:
        LW, MW, SW = weight_data[gender][age_key]
        z_score_w = calculate_z_score(weight, LW, MW, SW)
        
        
        if age_key in length_data[gender]:
            LHe, MHe, SHe = length_data[gender][age_key]
            z_score_he = calculate_z_score(height, LHe, MHe, SHe)

            average_z_score_w = z_score_w
            average_z_score_he = z_score_he

        if age_months>=24:
            LB, MB, SB = bmi_data[gender][age_key]
            z_score_b = calculate_z_score(bmi, LB, MB, SB)
            average_z_score_b = z_score_b
            percentile_b = percentile_calculator(average_z_score_b)
        else:
            average_z_score_b = 0
            percentile_b = 50

        if hc and hc!=0 and age_months<=36:            
            LHc, MHc, SHc = head_circumference_data[gender][age_key]
            z_score_hc = calculate_z_score(hc, LHc, MHc, SHc)
            average_z_score_hc = z_score_hc
            percentile_hc = percentile_calculator(average_z_score_hc)

        else:
            if hc==None:
                hc = 0
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
        
            if hc and hc!=0 and age_months<=36:            
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

        if hc and hc!=0 and age_months<=36:            
            z_score_lower_hc = calculate_z_score(hc, LHc_lower, MHc_lower, SHc_lower)
            z_score_upper_hc = calculate_z_score(hc, LHc_upper, MHc_upper, SHc_upper)
            average_z_score_hc = round(((z_score_lower_hc + z_score_upper_hc) / 2), 2)
            percentile_hc = percentile_calculator(average_z_score_hc)
        else:
            if hc==None: ################
                hc = 0
            average_z_score_hc = 0
            percentile_hc = 50


    percentile_w = percentile_calculator(average_z_score_w)
    percentile_he = percentile_calculator(average_z_score_he)

    response = {
        "Weight": {
            "value": weight,
            "z_score": round(average_z_score_w, 2),
            "percentile": percentile_w
            },
        "Height": {
            "value": height,
            "z_score": round(average_z_score_he, 2),
            "percentile": percentile_he
            },
        "BMI": {
            "value": bmi,
            "z_score": round(average_z_score_b, 2),
            "percentile": percentile_b
            },
        }
    if P50WL:
        response["Weight for Length"] = {
            "value": round(P50WL,2),
            "z_score": round(average_z_score_wl, 2)if average_z_score_wl else None,
            "percentile": percentile_wl
            }
    if hc and hc!=0 and age_months<=36:
        response["Head Circumference"] = {
            "value": hc,
            "z_score": round(average_z_score_hc, 2),
            "percentile": percentile_hc
            }
        
    return JsonResponse(response)
    
# -------------------- #

def create_alt_chart (records, gender, wps_data,):
    reversible_records = list(records)
    reversible_records.reverse()
    last_rec = reversible_records[-1]
    first_rec = reversible_records[0]

    agemos = wps_data[gender]['agemos']

    first_age = first_rec.age_months
    last_age = last_rec.age_months
    if first_age % 1 != 0.5:
        first_age -= 0.5
    if last_age % 1 != 0.5:
        last_age -= 0.5
    
    first_ind = agemos.index(first_age) - 3
    if first_ind < 0:
        first_ind = 0

    last_ind = agemos.index(last_age) + 7
    if last_age > 233.5:
        last_ind=agemos.index(240)

    
    agemos = agemos[first_ind:last_ind]
    p3  = wps_data[gender]['P3'][first_ind:last_ind]
    p5  = wps_data[gender]['P5'][first_ind:last_ind]
    p10 = wps_data[gender]['P10'][first_ind:last_ind]
    p25 = wps_data[gender]['P25'][first_ind:last_ind]
    p50 = wps_data[gender]['P50'][first_ind:last_ind]
    p75 = wps_data[gender]['P75'][first_ind:last_ind]
    p90 = wps_data[gender]['P90'][first_ind:last_ind]
    p95 = wps_data[gender]['P95'][first_ind:last_ind]
    p97 = wps_data[gender]['P97'][first_ind:last_ind]

    ages = []
    for i in reversible_records:
        if i.age_months in wps_data[gender]['agemos']:
            ages.append(i.age_months)
        else:
            ages.append(i.age_months-.5)

    weights= []
    co = 0
    for i in agemos:
        if i in ages:
            weights.append(reversible_records[co].weight)
            co+=1
        else:
            weights.append('-')

    # print(agemos)
    # print(ages)
    # print(weights)

    result = {
        'kid_data':json.dumps(weights),
        'agemos' : agemos,
        'p3': p3,
        'p5': p5,
        'p10': p10,
        'p25': p25,
        'p50': p50,
        'p75': p75,
        'p90': p90,
        'p95': p95,
        'p97': p97,
    }
    return result
