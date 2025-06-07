import requests
from datetime import date, timedelta
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse

from .models import *
from .forms import *
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
        form = NewPatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.personal_id = personal_id
            patient.save()
            del request.session['pending_personal_id']
            return redirect('zscore', personal_id=patient.personal_id)
    else:
        form = NewPatientForm()
    return render(request, 'doctors/new_patient.html', {'doctor':doctor,'form': form, 'personal_id': personal_id})



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

def to_five(value):
    value *= 10
    value=round(value)
    while value % 5 != 0:
        value += 1
    return value / 10


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

            # Check for existing record
            existing_qs = Record.objects.filter(
                doctor=doctor, patient=patient, record_date=record_date
            )

            # Return a warning if exists and no override/update
            if existing_qs.exists() and not request.POST.get('force') and not request.POST.get('update'):
                return JsonResponse({
                    'status': 'exists',
                    'message': f"A record already exists for {record_date}.",
                })

            try:
                response = requests.get(
                    "https://medepartout.ir/calculus/calculi/pedi_all_zscores/",
                    params={
                        'gender': gender,
                        'age_months': age_months,
                        'weight': weight,
                        'height': height,
                    }
                )
                response.raise_for_status()
                result = response.json()

                # Update existing record
                if request.POST.get('update') and existing_qs.exists():
                    record = existing_qs.first()
                    record.weight = weight
                    record.height = height
                    record.hc = hc
                    record.age_months = age_months
                    record.weight_z = result["weight"]["z_score"]
                    record.weight_p = result["weight"]["percentile"]
                    record.height_z = result["height"]["z_score"]
                    record.height_p = result["height"]["percentile"]
                    record.bmi = result["bmi"]["value"]
                    record.bmi_z = result["bmi"]["z_score"]
                    record.bmi_p = result["bmi"]["percentile"]
                    record.save()
                    return JsonResponse({'status': 'updated', 'result': result })

                # Otherwise, create a new one
                Record.objects.create(
                    doctor=doctor,
                    patient=patient,
                    gender=gender,
                    age_months=age_months,
                    record_date=record_date,
                    weight=weight,
                    height=height,
                    # hc=hc,
                    weight_z=result["weight"]["z_score"],
                    weight_p=result["weight"]["percentile"],
                    height_z=result["height"]["z_score"],
                    height_p=result["height"]["percentile"],
                    bmi=result["bmi"]["value"],
                    bmi_z=result["bmi"]["z_score"],
                    bmi_p=result["bmi"]["percentile"]
                )
                return JsonResponse({'status': 'created', 'result': result })

            except requests.RequestException as e:
                return JsonResponse({'status': 'error', 'error': str(e)})

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


from .templatetags.tags import *

@login_required
def patient_record_view(request, personal_id):
    doctor = get_object_or_404(Doctor, user=request.user)
    patient = get_object_or_404(Patient, personal_id=personal_id)
    patient_age = calculate_age_extended(patient.birth_date)
    # Filter records for this doctor and this patient
    records = Record.objects.filter(doctor=doctor, patient=patient).order_by('-record_date')
    records_reverse=Record.objects.filter(doctor=doctor, patient=patient).order_by('record_date')


    # Get all Z-scores
    all_zscores = {
        'weight_z': [record.weight_z for record in records_reverse],
        'height_z': [record.height_z for record in records_reverse],
        'bmi_z': [record.bmi_z for record in records_reverse],
        'labels': [j_date(record.record_date, 'digit, long') for record in records_reverse]
    }

    # Last 3 records (latest to earliest)
    recent_records = records[:5]
    recent_data = [{
        'date': j_date(r.record_date, 'name, long'),
        'weight': r.weight,
        'height': r.height,
        'bmi': round(r.bmi,2),
        'weight_z': r.weight_z,
        'height_z': r.height_z,
        'bmi_z': r.bmi_z,
        'weight_p': r.weight_p,
        'height_p': r.height_p,
        'bmi_p': r.bmi_p
    } for r in recent_records]

    # Last 5 visits (date + one or more value fields)
    last_visits = {
        'weight': [record.weight for record in records_reverse[:10]],
        'height': [record.height for record in records_reverse[:10]],
        'bmi': [record.bmi for record in records_reverse[:10]],
        'labels': [j_date(record.record_date, 'digit, long') for record in records_reverse[:10]]
    }
    
    recoms = Recommendation.objects.filter(add_date = date.today(), doctor=doctor, patient=patient).order_by('-add_date')[:5]

    context = {
        'doctor': doctor,
        'patient': patient,
        'patient_age': patient_age,
        # 'all_zscores': all_zscores,
        # 'all_dates': all_dates_jalali,
        'recent_records': recent_data,
        # 'last_visits': last_visits,
        'recoms': recoms,
    }
    context['all_zscores'] = json.dumps(all_zscores)
    context['last_visits'] = json.dumps(last_visits)

    return render(request, 'doctors/patient_records.html', context)

@login_required
def patient_record_print_view(request, personal_id):
    doctor = get_object_or_404(Doctor, user=request.user)
    patient = get_object_or_404(Patient, personal_id=personal_id)
    patient_age = calculate_age_extended(patient.birth_date)
    # Filter records for this doctor and this patient
    records = Record.objects.filter(doctor=doctor, patient=patient).order_by('-record_date')
    records_reverse=Record.objects.filter(doctor=doctor, patient=patient).order_by('record_date')


    # Get all Z-scores
    all_zscores = {
        'weight_z': [record.weight_z for record in records_reverse],
        'height_z': [record.height_z for record in records_reverse],
        'bmi_z': [record.bmi_z for record in records_reverse],
        'labels': [j_date(record.record_date, 'digit, long') for record in records_reverse]
    }

    # Last 3 records (latest to earliest)
    recent_records = records[:5]
    recent_data = [{
        'date': j_date(r.record_date, 'name, long'),
        'weight': r.weight,
        'height': r.height,
        'bmi': round(r.bmi,2),
        'weight_z': r.weight_z,
        'height_z': r.height_z,
        'bmi_z': r.bmi_z,
        'weight_p': r.weight_p,
        'height_p': r.height_p,
        'bmi_p': r.bmi_p
    } for r in recent_records]

    # Last 5 visits (date + one or more value fields)
    last_visits = {
        'weight': [record.weight for record in records_reverse[:10]],
        'height': [record.height for record in records_reverse[:10]],
        'bmi': [record.bmi for record in records_reverse[:10]],
        'labels': [j_date(record.record_date, 'digit, long') for record in records_reverse[:10]]
    }
    
    recoms = Recommendation.objects.filter(add_date = date.today(), doctor=doctor, patient=patient)
    last_recom = recoms.first()
    
    if request.method == 'POST':
        # Get the recommendation text from the form
        recommendation_text = request.POST.get('recommendation_text')
        if recommendation_text:  # Make sure there's text

            if last_recom.exists():
                last_recom.text = recommendation_text
                last_recom.save()
            else: 
                Recommendation.objects.create(
                    doctor=doctor,
                    patient=patient,
                    text=recommendation_text,
                    # Add any other required fields here
                )
        else:
            pass
        # Redirect to prevent form resubmission on refresh
        return redirect('patient_records_print', personal_id=personal_id)
    
    context = {
        'doctor': doctor,
        'patient': patient,
        'patient_age': patient_age,
        # 'all_zscores': all_zscores,
        # 'all_dates': all_dates_jalali,
        'recent_records': recent_data,
        'last_recom':last_recom.text,
        # 'last_visits': last_visits,
    }
    context['all_zscores'] = json.dumps(all_zscores)
    context['last_visits'] = json.dumps(last_visits)
    
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
