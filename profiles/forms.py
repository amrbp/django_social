from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ProfileModelFrom(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio','avatar')


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name' ,'password1', 'password2']
