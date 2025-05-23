from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import Patient
from .forms import IDCheckForm, NewPatientForm

from .forms import *

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


import requests
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict
from datetime import date
import json

from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required

from .models import *
from accounts.models import *

# @login_required
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
        age_months=round(float(age_months),0)

        
        if patient.gender =='پسر':
            gender = '1'
        else: 
            gender='2'
        # Send request to the external API
        try:
            response = requests.get(
                "https://mdpt.ir/calculus/calculi/pedi_all_zscores/",
                params={
                    'gender': gender,
                    'age_months': age_months,
                    'weight': weight,
                    'height': height,
                }
            )
            doctor = get_object_or_404(Doctor, user__username='Ehsan')
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
                weight_z=result['weight']['z_score'],
                weight_p=result['weight']['percentile'],
                height_z=result['height']['z_score'],
                height_p=result['height']['percentile'],
                bmi=result['bmi']['value'],
                bmi_z=result['bmi']['z_score'],
                bmi_p=result['bmi']['percentile']
            )
        
        except requests.RequestException as e:
            result = {'error': str(e)}

    return render(request, 'doctors/zscore.html', {
        'patient': patient,
        'result': result,
        'previous': previous,
    })




# You said you have a Jalali converter, so we assume: to_jalali(date)
from .templatetags.tags import *  # hypothetical utility function

# @login_required
def patient_record_view(request, personal_id):
    doctor = get_object_or_404(Doctor, user__username='Ehsan')
    patient = get_object_or_404(Patient, personal_id=personal_id)

    # Filter records for this doctor and this patient
    records = Record.objects.filter(doctor=doctor, patient=patient).order_by('-record_add_date')
    records_reverse=Record.objects.filter(doctor=doctor, patient=patient).order_by('record_add_date')

    # Convert all records' dates to Jalali
    # all_dates_jalali = [to_jalali(str(record.record_add_date.strftime("%Y %m %d"))) for record in records]

    # Get all Z-scores
    all_zscores = {
        'weight_z': [record.weight_z for record in records_reverse],
        'height_z': [record.height_z for record in records_reverse],
        'bmi_z': [record.bmi_z for record in records_reverse],
        'labels': [to_jalali(str(record.record_add_date.strftime("%Y %m %d"))) for record in records_reverse]
    }

    # Last 3 records (latest to earliest)
    recent_records = records[:3]
    recent_data = [{
        'date': to_jalali(r.record_add_date.strftime("%Y %m %d")),
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
        'weight': [record.weight for record in records_reverse[:5]],
        'height': [record.height for record in records_reverse[:5]],
        'bmi': [record.bmi for record in records_reverse[:5]],
        'labels': [to_jalali(str(record.record_add_date.strftime("%Y %m %d"))) for record in records_reverse[:5]]
    }
    

    context = {
        'doctor': doctor,
        'patient': patient,
        # 'all_zscores': all_zscores,
        # 'all_dates': all_dates_jalali,
        'recent_records': recent_data,
        # 'last_visits': last_visits,
    }
    context['all_zscores'] = json.dumps(all_zscores)
    context['last_visits'] = json.dumps(last_visits)

    return render(request, 'doctors/patient_records.html', context)
