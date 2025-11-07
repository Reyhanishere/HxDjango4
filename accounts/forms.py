from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=100)
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("first_name","last_name","email","field","university","degree",)
    

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        # if user.student_profile.verified:
        #     pass
        # else:
        fields=['first_name', 'last_name', 'degree', 'university','fn_fa','ln_fa','en_name']
        
    first_name=forms.CharField(label='نام به انگلیسی')
    last_name=forms.CharField(label='نام خانوادگی به انگلیسی')

    en_name = forms.BooleanField(
        label='نام من را به انگلیسی نشان بده.',
        required=False
    )
    fn_fa = forms.CharField(
        label='نام به فارسی',
        required=False
    )
    ln_fa = forms.CharField(
        label='نام خانوادگی به فارسی',
        required=False
    )
    university = forms.ChoiceField(
        choices=CustomUser.UNIS,
        label='دانشگاه',
        required=False
    )
    degree = forms.ChoiceField(
        choices=CustomUser.DEGREES,
        label='مقطع',
        required=False,
        help_text="مقطع فعلی شما (اگر دانشجوی پزشکی نیستید، خالی بگذارید)"
    )
    password=forms.HiddenInput()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        hidden_fields=['fn_fa','ln_fa']

        # Check if the user has a student profile, doesn't let the user to change their Persian name.
        try: 
            if self.user.student_profile.verified == True:
                for f in hidden_fields:
                    self.fields[f].widget = forms.HiddenInput()
        except:
            pass

    def clean(self):
        cleaned_data = super().clean()
        en_name = cleaned_data.get('en_name')
        fn_fa = cleaned_data.get('fn_fa')
        ln_fa = cleaned_data.get('ln_fa')

        if en_name is False and (not fn_fa or not ln_fa):
            raise forms.ValidationError("برای اینکه نام فارسی شما را نمایش دهیم، باید نام خود را به فارسی وارد کنید.")

        return cleaned_data

class StudentProfileCreateForm(forms.ModelForm):
    contact_info = forms.CharField(widget=forms.TextInput(attrs={'dir':'ltr', 'maxlength':'11'}), required=True)
    semester_of_entrance = forms.IntegerField(widget=forms.NumberInput(attrs={'dir':'ltr', 'maxlength':'5'}), required=True)
    student_id = forms.IntegerField(widget=forms.NumberInput(attrs={'dir':'ltr'}), required=True)

    class Meta:
        model = StudentProfile
        exclude = ("verified_date", "verified", "completed", "user")
        labels = {
                'working_university': ('دانشگاه'),
                'contact_info': ('شماره تماس'),
                'semester_of_entrance': ('ورودی'),
                'student_id': ('شماره دانشجویی'),        
        }
        help_texts={
                'semester_of_entrance': ('برای نمونه اگر ورودی مهر 1404 هستید، به صورت 14041 و اگر ورودی بهمن 1399 هستید، 13992 وارد کنید.'),
         }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super().clean()

        # Check if the user has Farsi name or not:
        if not self.user.has_fa_name():
            raise forms.ValidationError(
                "ابتدا در  صفحۀ «ویرایش اطلاعات من» نام فارسی خود را ثبت کنید."
                )
        
        # Check Semester of Entrance format:
        if len(str(cleaned_data.get('semester_of_entrance'))) != 5:
            raise forms.ValidationError({"semester_of_entrance": "انتظار داریم یک عدد پنج رقمی وارد کنید."})
        else:
            year = int(str(cleaned_data.get('semester_of_entrance'))[:4])
            semester = str(cleaned_data.get('semester_of_entrance'))[4]

        if year < 1390 or year > 1404:
            raise forms.ValidationError(
                {"semester_of_entrance":"سال ورودی باید از 1390 تا به امروز باشد."}
                )
        elif semester not in ['1', '2']:
            raise forms.ValidationError(
                {"semester_of_entrance":"برای ورودی بهمن، عدد دو و برای ورودی مهر، عدد یک را وارد کنید."}
                )
        phone_number = str(cleaned_data.get('contact_info'))
        if len(phone_number) != 11:
            raise forms.ValidationError(
                {"contact_info":"شماره تماس، یک عدد یازده رقمی است."}
                )
        elif phone_number[:2] != "09": # Iran phone numbers
            raise forms.ValidationError(
                {"contact_info":"شماره تماس، در ایران به صورت 09** *** **** است.."}
            )
        elif not phone_number.isnumeric():
            raise forms.ValidationError(
                {"contact_info":"من جایی را نمی‌شناسم که کاراکتری غیر از عدد در شماره تماسش داشته باشد."}
            )

        return cleaned_data
