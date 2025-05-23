from django import forms
from .models import Patient
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class IDCheckForm(forms.Form):
    personal_id = forms.CharField(max_length=10, min_length=10, label="ID Number")

class NewPatientForm(forms.ModelForm):
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),)

    class Meta:
        model = Patient
        fields = ["name", "gender", "birth_date"]
