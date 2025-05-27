import jdatetime
from datetime import date

from django import forms
from .models import Patient
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class IDCheckForm(forms.Form):
    autocomplete=True
    def set_autocomplete(boolean):
        if boolean==False:
            return 'off'
        else:
            return 'on'
        
    personal_id = forms.CharField(max_length=10, 
                                  min_length=6, 
                                  label="ID Number",
                                  widget=forms.TextInput(attrs={'dir': 'ltr', 
                                                                'autocomplete':set_autocomplete(autocomplete)}),
                                                                )
    def clean_personal_id(self):
        personal_id = self.cleaned_data['personal_id']
        if personal_id[0].isdigit():
            if len(personal_id)!=10:
                raise forms.ValidationError("کد ملی باید ده رقم باشد.")
            if not personal_id.isdigit():
                raise forms.ValidationError("کد ملی باید صرفا حاوی عدد باشد.")
            # so the id is local
            indices_sum=0
            for index, digit in enumerate(personal_id[:-1]):
                indices_sum += int(digit) * (10 - index)
            sum_mod=indices_sum % 11
            last_digit = int(personal_id[-1])
            if not ((sum_mod > 1 and sum_mod == 11 - last_digit) or 
                (sum_mod < 2 and sum_mod == last_digit)):
                raise forms.ValidationError("کد ملی وارد شده معتبر نیست.")
            return personal_id
        else:
            if not personal_id[1:].isdigit():
                raise forms.ValidationError("کد گذرنامه معتبر نیست.")
            return personal_id
            


    def save(self, commit=True):
            instance = super().save(commit=False)
            instance.personal_id = self.cleaned_data['personal_id']
            if commit:
                instance.save()
            return instance


class NewPatientForm(forms.ModelForm):
    name = forms.CharField(label="نام و نام خانوادگی",
                                  widget=forms.TextInput(attrs={'dir': 'rtl', 'autocomplete':'off'}))
    jalali_birth_date = forms.CharField(label="تاریخ تولد", help_text='مثلا 1404/05/04',widget=forms.TextInput(attrs={'dir': 'ltr', 
                                                                'autocomplete':'off'}),
                                                                )
    class Meta:
        model = Patient
        fields = ["name", "gender", "jalali_birth_date"]

    def clean_jalali_birth_date(self):
        jalali_str = self.cleaned_data['jalali_birth_date']
        try:
            # Split and convert
            year, month, day = map(int, jalali_str.split('/'))
            if not (1 <= month <= 12):
                raise forms.ValidationError("ماه وارد شده معتبر نیست.")
            elif not(1 <= day <= 31):
                raise forms.ValidationError("روز وارد شده معتبر نیست.")

            j_date = jdatetime.date(year, month, day)
            g_date = j_date.togregorian()

            # Validation: future date check
            if g_date > date.today():
                raise forms.ValidationError("تاریخ تولد نمی‌تواند در آینده باشد.")
            if year < 1381:
                raise forms.ValidationError("سال وارد شده پشتیبانی نمی‌شود.")
            return g_date
        
        except ValueError:
            raise forms.ValidationError("تاریخ وارد شده معتبر نیست.")


    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.birth_date = self.cleaned_data['jalali_birth_date']  # already converted to Gregorian
        if commit:
            instance.save()
        return instance
