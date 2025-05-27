import requests
from decimal import Decimal, ROUND_HALF_UP
from datetime import date, timedelta
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import *
from .forms import *
from accounts.models import *

def check_or_create_patient(request):
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
    return render(request, 'doctors/check_id.html', {'form': id_form})

def create_patient(request):
    personal_id = request.session.get('pending_personal_id')
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
    return render(request, 'doctors/new_patient.html', {'form': form, 'personal_id': personal_id})



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


@login_required
def calculate_zscore(request, personal_id):
    patient = get_object_or_404(Patient, personal_id=personal_id)
    previous = Record.objects.filter(patient=patient).order_by('-record_add_date').first()
    result = None
    if request.method == 'POST':
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        # hc = request.POST.get('hc')

        # Calculate age in months with 0.5 precision
        today = date.today()
        days = (today - patient.birth_date).days
        age_months = Decimal(days / 30.4375).quantize(Decimal('0.5'), rounding=ROUND_HALF_UP)
        
        if patient.gender =='پسر':
            gender = '1'
        else: 
            gender='2'
        # Send request to the external API
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
            doctor = get_object_or_404(Doctor, user=request.user)
            response.raise_for_status()
            result = response.json()
            Record.objects.create(
                doctor=doctor,
                patient=patient,
                gender=gender,
                age_months = age_months,
                weight=weight,
                height=height,
                # hc=hc,
                # Extract values from the response
                weight_z=result["weight"]["z_score"],
                weight_p=result["weight"]["percentile"],
                height_z=result["height"]["z_score"],
                height_p=result["height"]["percentile"],
                bmi=result["bmi"]["value"],
                bmi_z=result["bmi"]["z_score"],
                bmi_p=result["bmi"]["percentile"]
            )
        
        except requests.RequestException as e:
            result = {'error': str(e)}

    return render(request, 'doctors/zscore.html', {
        'patient': patient,
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
    records = Record.objects.filter(doctor=doctor, patient=patient).order_by('-record_add_date')
    records_reverse=Record.objects.filter(doctor=doctor, patient=patient).order_by('record_add_date')


    # Get all Z-scores
    all_zscores = {
        'weight_z': [record.weight_z for record in records_reverse],
        'height_z': [record.height_z for record in records_reverse],
        'bmi_z': [record.bmi_z for record in records_reverse],
        'labels': [j_date(record.record_add_date, 'digit, long') for record in records_reverse]
    }

    # Last 3 records (latest to earliest)
    recent_records = records[:5]
    recent_data = [{
        'date': j_date(r.record_add_date, 'name, long'),
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
        'labels': [j_date(record.record_add_date, 'digit, long') for record in records_reverse[:10]]
    }
    

    context = {
        'doctor': doctor,
        'patient': patient,
        'patient_age': patient_age,
        # 'all_zscores': all_zscores,
        # 'all_dates': all_dates_jalali,
        'recent_records': recent_data,
        # 'last_visits': last_visits,
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
    records = Record.objects.filter(doctor=doctor, patient=patient).order_by('-record_add_date')
    records_reverse=Record.objects.filter(doctor=doctor, patient=patient).order_by('record_add_date')


    # Get all Z-scores
    all_zscores = {
        'weight_z': [record.weight_z for record in records_reverse],
        'height_z': [record.height_z for record in records_reverse],
        'bmi_z': [record.bmi_z for record in records_reverse],
        'labels': [j_date(record.record_add_date, 'digit, long') for record in records_reverse]
    }

    # Last 3 records (latest to earliest)
    recent_records = records[:5]
    recent_data = [{
        'date': j_date(r.record_add_date, 'name, long'),
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
        'labels': [j_date(record.record_add_date, 'digit, long') for record in records_reverse[:10]]
    }
    

    context = {
        'doctor': doctor,
        'patient': patient,
        'patient_age': patient_age,
        # 'all_zscores': all_zscores,
        # 'all_dates': all_dates_jalali,
        'recent_records': recent_data,
        # 'last_visits': last_visits,
    }
    context['all_zscores'] = json.dumps(all_zscores)
    context['last_visits'] = json.dumps(last_visits)

    return render(request, 'doctors/patient_records_print.html', context)
