from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=100)
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("first_name","last_name","email","field","university","degree",)
    

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields=['first_name', 'last_name', 'degree', 'university','fn_fa','ln_fa','en_name']
    first_name=forms.CharField(label='نام به انگلیسی')
    last_name=forms.CharField(label='نام خانوادگی به انگلیسی')
    # degree=forms.ChoiceField(label='ردۀ تحصیلی')

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

    def clean(self):
        cleaned_data = super().clean()
        en_name = cleaned_data.get('en_name')
        fn_fa = cleaned_data.get('fn_fa')
        ln_fa = cleaned_data.get('ln_fa')

        if en_name is False and (not fn_fa or not ln_fa):
            raise forms.ValidationError("برای اینکه نام فارسی شما را نمایش دهیم، باید نام خود را به فارسی وارد کنید.")

        return cleaned_data
    
