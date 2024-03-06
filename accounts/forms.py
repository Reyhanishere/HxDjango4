from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=100)
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("first_name","last_name","email","university","degree",)
    

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields= ("university","degree",)
    