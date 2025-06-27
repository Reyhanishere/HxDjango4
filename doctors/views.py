from datetime import date, timedelta
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse

from .models import *
from .forms import *
from .utils import *
from .templatetags.tags import *
from accounts.models import *

def check_or_create_patient(request):
    doctor = get_object_or_404(Doctor, user=request.user)

    if request.method == 'POST':
        id_form = IDCheckForm(request.POST)
        if id_form.is_valid():
            personal_id = id_form.cleaned_data['personal_id']
            try:
                patient = Patient.objects.get(personal_id=personal_id)
                return redirect('zscore', personal_id=patient.personal_id)
            except Patient.DoesNotExist:
                request.session['pending_personal_id'] = personal_id
                return redirect('new_patient_info')
    else:
        id_form = IDCheckForm()
    return render(request, 'doctors/check_id.html', {'doctor': doctor,'form': id_form})

def create_patient(request):
    personal_id = request.session.get('pending_personal_id')
    doctor = get_object_or_404(Doctor, user=request.user)
    if not personal_id:
        return redirect('corc_patient')

    if request.method == 'POST':
        form = NewPatientForm(request.POST, is_default_girl=doctor.is_girl, is_date_reverse=doctor.is_date_reverse)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.personal_id = personal_id
            patient.created_by = doctor
            patient.save()
            del request.session['pending_personal_id']
            return redirect('zscore', personal_id=patient.personal_id)
    else:
        form = NewPatientForm(is_default_girl=doctor.is_girl, is_date_reverse=doctor.is_date_reverse)
    return render(request, 'doctors/new_patient.html', {'doctor':doctor,'form': form, 'personal_id': personal_id})


@login_required
def patient_record_view(request, personal_id):
    doctor = get_object_or_404(Doctor, user=request.user)
    patient = get_object_or_404(Patient, personal_id=personal_id)
    patient_age = calculate_age_extended(patient.birth_date)
    # Filter records for this doctor and this patient
    records = Record.objects.filter(doctor=doctor, patient=patient).order_by('-record_date')
    
    # Set is_wl
    is_wl = set_is_wl(records.first())

    # Get all Z-scores
    z_scores_list = list(records[:doctor.z_score_count])
    z_scores_list.reverse()
    all_zscores = {
        'weight_z': [record.weight_z for record in z_scores_list],
        'height_z': [record.height_z for record in z_scores_list],
        'bmi_z': [record.bmi_z for record in z_scores_list],
        'hc_z': [record.hc_z for record in z_scores_list] if patient.get_age_months() <= 36 else [],
        'wl_z': [record.wl_z for record in z_scores_list] if is_wl else [],

        'labels': [j_date(record.record_date, 'digit, long') for record in z_scores_list]
    }

    # Last 5 records (latest to earliest) for Table
    recent_records = records[:doctor.table_rows_count]
    recent_data = set_recent_data(records=recent_records, age=patient.get_age_months(), is_wl=is_wl)

    # Last n visits for mini charts
    last_records = list(records[:doctor.mini_charts_data_count])
    last_records.reverse()
    last_visits = {
        'weight': [record.weight for record in last_records],
        'height': [record.height for record in last_records],
        'hc': [record.hc for record in last_records],
        'wl_p50': [record.wl_p50 for record in last_records],

        'labels': [j_date(record.record_date, 'digit, long') for record in last_records]
    }
    if patient.get_age_months() >= 24:
        last_visits['bmi'] = [record.bmi for record in last_records]
    
    recoms = Recommendation.objects.filter(doctor=doctor, patient=patient).order_by('-add_date')[:5]

    alt_chart_records = Record.objects.filter(patient=patient).order_by('-record_date')[:doctor.z_score_count]
    gender = '1' if patient.gender == 'پسر' else '2'
    alternative_chart = create_alt_chart(alt_chart_records, gender, wps_data)

    context = {
        'doctor': doctor,
        'patient': patient,
        'patient_age': patient_age,
        'recent_records': recent_data,
        'recoms': recoms,
        'is_wl': is_wl,
    }
    context['all_zscores'] = json.dumps(all_zscores)
    context['last_visits'] = json.dumps(last_visits)
    context['alt_chart'] = json.dumps(alternative_chart)

    return render(request, 'doctors/patient_records.html', context)

@login_required
def patient_record_print_view(request, personal_id):
    doctor = get_object_or_404(Doctor, user=request.user)
    patient = get_object_or_404(Patient, personal_id=personal_id)
    patient_age = calculate_age_extended(patient.birth_date)
    
    days = (date.today() - patient.birth_date).days
    age_months = to_five(round((days / 30.4375), 1))
    age_months = min(age_months, 240)
    # Filter records for this doctor and this patient
    records = Record.objects.filter(doctor=doctor, patient=patient).order_by('-record_date')

    # Set recommendations
    last_record = records.first()
    if last_record:
        considerations, recommendations = make_recom_and_considers(age_months=age_months, last_record=last_record)
    else: 
        considerations, recommendations = {}, {}
    
    # Set is_wl
    is_wl = set_is_wl(records.first())

    # Get all Z-scores
    z_scores_list = list(records[:doctor.z_score_count])
    z_scores_list.reverse()
    all_zscores = {
        'weight_z': [record.weight_z for record in z_scores_list],
        'height_z': [record.height_z for record in z_scores_list],
        'bmi_z': [record.bmi_z for record in z_scores_list],
        'hc_z': [record.hc_z for record in z_scores_list] if patient.get_age_months() <= 36 else [],
        'wl_z': [record.wl_z for record in z_scores_list] if is_wl else [],

        'labels': [j_date(record.record_date, 'digit, long') for record in z_scores_list]
    }

    # Last n records (latest to earliest) for Table
    recent_records = records[:5]
    recent_data = set_recent_data(records=recent_records, age=patient.get_age_months(), is_wl=is_wl)

    # Last n visits for mini charts
    last_records = list(records[:doctor.mini_charts_data_count])
    last_records.reverse()
    last_visits = {
        'weight': [record.weight for record in last_records],
        'height': [record.height for record in last_records],
        'hc': [record.hc for record in last_records],
        'wl_p50': [record.wl_p50 for record in last_records],

        'labels': [j_date(record.record_date, 'digit, short') for record in last_records]
    }
    if patient.get_age_months() >= 24:
        last_visits['bmi'] = [record.bmi for record in last_records]
    
    recoms = Recommendation.objects.filter(doctor=doctor, patient=patient)
    last_recom = recoms.last()
    today_recom = Recommendation.objects.filter(doctor=doctor, patient=patient, add_date=date.today()).last()
    
    if request.method == 'POST':
        recommendation_text = request.POST.get('recommendation_text')
        if recommendation_text:
            if today_recom:
                today_recom.text = recommendation_text
                today_recom.save()
            else: 
                Recommendation.objects.create(
                    doctor=doctor,
                    patient=patient,
                    text=recommendation_text,
                )
        else:
            pass
        # Redirect to prevent form resubmission on refresh
        return redirect('patient_records_print', personal_id=personal_id)
    
    alt_chart_records = Record.objects.filter(patient=patient).order_by('-record_date')[:doctor.z_score_count]
    gender = '1' if patient.gender == 'پسر' else '2'
    alternative_chart = create_alt_chart(alt_chart_records, gender, wps_data)
    
    context = {
        'doctor': doctor,
        'patient': patient,
        'patient_age': patient_age,
        'recent_records': recent_data,
        'last_recom':last_recom.text if last_recom else '',
        'considerations' : considerations,
        'recommendations' : recommendations,
        'is_wl': is_wl,

    }
    context['all_zscores'] = json.dumps(all_zscores)
    context['last_visits'] = json.dumps(last_visits)
    context['alt_chart'] = json.dumps(alternative_chart)
    
    return render(request, 'doctors/patient_records_print.html', context)

@login_required
def patients_list_view(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    records = Record.objects.filter(doctor=doctor).order_by('-record_add_date')
    patients_list=list()
    patients_set=set()

    for r in records[:100]:
        # while len(patients_set) < 10:
        patients_set.add(r.patient.personal_id)
    for r in records[:100]:
        # while len(patients_list) < 10:
        if r.patient.personal_id in patients_set:
            patients_list.append(r.patient)
            patients_set.remove(r.patient.personal_id)

    context = {
        'doctor': doctor,
        'patients': patients_list,
    }

    return render(request, 'doctors/patients_list.html', context)

@login_required
def patient_update_view(request, personal_id):
    # Get the patient or return 404
    patient = get_object_or_404(Patient, personal_id=personal_id)
    
    # Check if the requesting user is a doctor
    doctor = Doctor.objects.filter(user=request.user)
    is_doctor = doctor.exists()
    doctor = get_object_or_404(Doctor, user=request.user)

    if not is_doctor:
        # You can return a permission denied response or redirect
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("Only doctors can edit patient information")
    
    if request.method == 'POST':
        form = PatientUpdateForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('zscore', personal_id=patient.personal_id)  # Redirect to patient detail view
    else:
        form = PatientUpdateForm(instance=patient)
    
    return render(request, 'doctors/update_patient.html', {
        'doctor': doctor,
        'form': form,
        'patient': patient,
    })


@login_required
def calculate_zscore(request, personal_id):
    patient = get_object_or_404(Patient, personal_id=personal_id)
    previous = Record.objects.filter(patient=patient).order_by('-record_date').first()
    doctor = get_object_or_404(Doctor, user=request.user)
    result = None

    form = ZScoreForm(request.POST or None, birth_date=patient.birth_date)

    if request.method == 'POST':
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            hc = form.cleaned_data.get('hc')
            record_date = form.cleaned_data['jalali_record_date']

            # Calculate age in months
            days = (record_date - patient.birth_date).days
            age_months = to_five(round((days / 30.4375), 1))
            age_months = min(age_months, 240)

            gender = '1' if patient.gender == 'پسر' else '2'

            # Validation
            if gender not in ['1', '2']:
                return JsonResponse({'error': 'جنسیت باید دختر یا پسر باشد.'}, status=400)
            if height < 30 or height > 250:
                return JsonResponse({'error': 'قد به درستی وارد نشده است. واحد قابل پذیرش، سانتی‌متر (cm) است.'}, status=400)
            if weight < 0.5 or weight > 300:
                return JsonResponse({'error': 'وزن به درستی وارد نشده است. واحد قابل پذیرش، کیلوگرم (kg) است.'}, status=400)
            if age_months % 0.5 != 0:
                return JsonResponse({'error': 'خطایی در سن کودک رخ داده است.'}, status=400)
            if age_months > 240.5:
                return JsonResponse({'error': 'سامانه تا سن بیست سالگی قابل استفاده است.'}, status=400)

            # Check for existing record
            existing_qs = Record.objects.filter(
                doctor=doctor, patient=patient, record_date=record_date
            )

            if existing_qs.exists() and not request.POST.get('force') and not request.POST.get('update'):
                return JsonResponse({
                    'status': 'exists',
                    'message': "در این تاریخ یک رکورد ثبت شده است.",
                })

            try:
                result_content = json.loads(find_LMS_whole(weight, height, gender, age_months, hc).content)

                # Update existing record
                if request.POST.get('update') and existing_qs.exists():
                    record = existing_qs.first()
                    record.weight = weight
                    record.height = height
                    record.hc = hc
                    
                    record.age_months = age_months
                    record.weight_z = result_content["Weight"]["z_score"]
                    record.weight_p = result_content["Weight"]["percentile"]

                    record.height_z = result_content["Height"]["z_score"]
                    record.height_p = result_content["Height"]["percentile"]
                    
                    if "Head Circumference" in result_content.keys():
                        record.hc_z = result_content["Head Circumference"]["z_score"]
                        record.hc_p = result_content["Head Circumference"]["percentile"]
                    
                    if "Weight for Length" in result_content.keys():
                        record.wl_p50 = result_content["Weight for Length"]["value"]
                        record.wl_z = result_content["Weight for Length"]["z_score"]
                        record.wl_p = result_content["Weight for Length"]["percentile"]

                    if result_content["BMI"]:
                        record.bmi = result_content["BMI"]["value"]
                        record.bmi_z = result_content["BMI"]["z_score"]
                        record.bmi_p = result_content["BMI"]["percentile"]

                    record.save()
                    return JsonResponse({'status': 'updated', 'result': result_content})
                
                # Create new record
                Record.objects.create(
                    doctor=doctor,
                    patient=patient,
                    gender=gender,
                    age_months=age_months,
                    record_date=record_date,
                    weight=weight,
                    height=height,
                    hc=hc,
                    weight_z=result_content["Weight"]["z_score"],
                    weight_p=result_content["Weight"]["percentile"],
                    height_z=result_content["Height"]["z_score"],
                    height_p=result_content["Height"]["percentile"],
                    hc_z = result_content["Head Circumference"]["z_score"] if "Head Circumference" in result_content.keys() else 0,
                    hc_p = result_content["Head Circumference"]["percentile"] if "Head Circumference" in result_content.keys() else 50,
                    wl_p50 = result_content["Weight for Length"]["value"] if "Weight for Length" in result_content.keys() else None,
                    wl_z = result_content["Weight for Length"]["z_score"] if "Weight for Length" in result_content.keys() else None,
                    wl_p = result_content["Weight for Length"]["percentile"] if "Weight for Length" in result_content.keys() else None,
                    bmi=result_content["BMI"]["value"],
                    bmi_z=result_content["BMI"]["z_score"],
                    bmi_p=result_content["BMI"]["percentile"]
                )
                return JsonResponse({'status': 'created', 'result': result_content})

            except Exception as e:
                return JsonResponse({'status': 'error', 'error': str(e)})
        else:
            errs = list(form.errors.values())

            return JsonResponse({'status': 'error', 'error': errs})
    else:
        initial_data = {}
        if previous:
            initial_data = {
                'weight': previous.weight if previous.weight else None,
                'height': previous.height if previous.height else None,
                'hc': previous.hc if previous.hc else None,
            }
        form = ZScoreForm(initial=initial_data)

    return render(request, 'doctors/zscore.html', {
        'patient': patient,
        'doctor': doctor,
        'form': form,
        'result': result,
        'previous': previous,
    })

import decimal
def drange(x, y, jump):
  while x < y:
    yield float(x)
    x += jump

def chart(request):
    patient = get_object_or_404(Patient, personal_id='0670893404')
    records = Record.objects.filter(patient=patient).order_by('-record_date')[:10]
    first_age = records[9].age_months
    if first_age%1 != 0.5:
        first_age -= 0.5
    last_age = Record.objects.filter(patient=patient).last().age_months
    if last_age%1 != 0.5:
        last_age += 0.5
    age_list = []
    
    # for i in list(drange(first_age-3, last_age+7, 10)):

    for i in range(int(10*(first_age-3)), int(10*(last_age+7)), 10):
        age_list.append(i/10)
    
    first_ind = age_list.index(first_age) - 3
    last_ind = age_list.index(last_age) + 7
    age_list = age_list[first_ind:last_ind]
    kid_data = []
    for i in age_list:
        for r in records:
            if r.age_months == i or r.age_months-0.5 == i:
                kid_data.append(r.weight)
                break        
        else:
            kid_data.append(10)
    # age = 50.5
    
    gender = '1'
    agemos = wps_data[gender]['agemos']
    # ind = agemos.index(age)
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
    # print(len(kid_data))
    # print(len(p3))
    # print(len(agemos))
    # print(len(p97))


    x = [24, 24.5, 25.5, 26.5, 27.5, 28.5, 29.5, 30.5, 31.5, 32.5, 33.5, 34.5, 35.5]
    result = {
        'kid_data':kid_data,
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
    p3 = [i for i in list(wps_data[gender].values())[0]]
    wps_data[gender]
    return render(request, 'doctors/chart.html', result)
