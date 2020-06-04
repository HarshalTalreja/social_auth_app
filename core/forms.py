from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('phone', 'name')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('phone', 'name')

class UpdatePhoneNoForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['phone', 'name']
