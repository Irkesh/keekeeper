from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ('organisation', )


class PasswordForm(forms.Form):
    #create_password = forms.CharField(label='Add Password', max_length=100)
    password_id =forms.CharField(label='Title', max_length=256)  #title - how user decide to call it
    username = forms.CharField(label='Username', max_length=256)     #username to store
    password = forms.CharField(label='Password', max_length=256)     #password to store
    url = forms.CharField(label='Url', max_length=256)
    #own = models.CharField(max_length=2, default="Me")
    comment = forms.CharField(label='Note', max_length=256)
    