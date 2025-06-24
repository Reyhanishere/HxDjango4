import jdatetime
from datetime import date
from dateutil.relativedelta import relativedelta

from django import forms
from .models import Patient
from .templatetags.tags import *


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
    def __init__(self, *args, **kwargs):
        self.is_default_girl = kwargs.pop('is_default_girl', None)
        self.is_date_reverse = kwargs.pop('is_date_reverse', None)
        super().__init__(*args, **kwargs)
        if self.is_default_girl:
            self.fields['gender'].initial='دختر'
        if self.is_date_reverse:
            self.fields['jalali_birth_date'].help_text = 'مثلا 4/5/1404'

    name = forms.CharField(label="نام و نام خانوادگی",
                                  widget=forms.TextInput(attrs={'dir': 'rtl', 'autocomplete':'off'}))
    
    jalali_birth_date = forms.CharField(label="تاریخ تولد", help_text='مثلا 1404/5/4',widget=forms.TextInput(attrs={'dir': 'ltr', 
                                                                'autocomplete':'off'}),
                                                                )
    class Meta:
        model = Patient
        fields = ["name", "gender", "jalali_birth_date"]


    def clean_jalali_birth_date(self):
        jalali_str = self.cleaned_data['jalali_birth_date']
        try:
            # Split and convert
            if self.is_date_reverse:
                day, month, year = map(int, jalali_str.split('/'))
            else:
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
            if g_date < date.today() - relativedelta(months=240):
                raise forms.ValidationError("سن نمی‌تواند بیشتر از ۲۰ سال باشد.")
            # if g_date < date(date.today().year - 20, date.today().month, date.today().day):                
            #     raise forms.ValidationError("سن نمی‌تواند بیشتر از ۲۰ سال باشد.")
            return g_date
        
        except ValueError:
            raise forms.ValidationError("تاریخ وارد شده معتبر نیست.")


    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.birth_date = self.cleaned_data['jalali_birth_date']  # already converted to Gregorian
        if commit:
            instance.save()
        return instance
    

class ZScoreForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.birth_date = kwargs.pop('birth_date', None)
        super().__init__(*args, **kwargs)

    weight = forms.FloatField(label="وزن", 
                              widget=forms.TextInput(attrs={'dir': 'ltr', 'autocomplete':'off',}))
    height = forms.FloatField(label="قد", 
                              widget=forms.TextInput(attrs={'dir': 'ltr', 'autocomplete':'off',}))
    hc = forms.FloatField(label="دور سر", required=False, 
                          widget=forms.TextInput(attrs={'dir': 'ltr', 'autocomplete':'off',}))
    jalali_record_date = forms.CharField(label="تاریخ ویزیت", required=False, help_text="مثلاً 1404/05/04", 
                                         widget=forms.TextInput(attrs={'dir': 'ltr', 'autocomplete':'off'}))
    
    def clean_jalali_record_date(self):
        data = self.cleaned_data.get('jalali_record_date')
        if not data:
            return date.today()
        try:
            year, month, day = map(int, data.split('/'))
            j_date = jdatetime.date(year, month, day)
            g_date = j_date.togregorian()
            if g_date > date.today():
                raise forms.ValidationError("تاریخ نمی‌تواند در آینده باشد.")
            if self.birth_date and g_date < self.birth_date:
                raise forms.ValidationError("تاریخ قبل از تولد بیمار است.")
            return g_date
        except:
            raise forms.ValidationError("تاریخ وارد شده معتبر نیست.")
        
class PatientUpdateForm(forms.ModelForm):
    name = forms.CharField(label="نام و نام خانوادگی",
                                  widget=forms.TextInput(attrs={'dir': 'rtl', 'autocomplete':'off'}))
    jalali_birth_date = forms.CharField(label="تاریخ تولد", widget=forms.TextInput(attrs={'dir': 'ltr', 
                                                                'autocomplete':'off',}),
                                                                )
    class Meta:
        model = Patient
        fields = ["name", "gender", "jalali_birth_date"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Access the model instance's field
        if self.instance and self.instance.pk:
            self.fields['jalali_birth_date'].widget.attrs.update({
                'value': j_date(self.instance.birth_date, "digit, long")
            })

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
            if g_date < date.today() - relativedelta(months=240):
                raise forms.ValidationError("سن نمی‌تواند بیشتر از ۲۰ سال باشد.")
            # if g_date < date(date.today().year - 20, date.today().month, date.today().day):                
            #     raise forms.ValidationError("سن نمی‌تواند بیشتر از ۲۰ سال باشد.")
            return g_date
        
        except ValueError:
            raise forms.ValidationError("تاریخ وارد شده معتبر نیست.")
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.birth_date = self.cleaned_data['jalali_birth_date']  # already converted to Gregorian
        if commit:
            instance.save()
        return instance
