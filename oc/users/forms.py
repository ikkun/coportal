from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,TEAM_CHOICES


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    team=forms.ChoiceField(choices=TEAM_CHOICES)
    

    class Meta:
        model = User
        fields = ['username','team','email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['team']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']