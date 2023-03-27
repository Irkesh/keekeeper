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
    comment = forms.CharField(label='Note', max_length=256)
    
class PasswordEditForm(forms.ModelForm):
    class Meta:
        model = PasItem
        fields = ['password_id', 'username', 'password', 'url', 'comment']
        labels = {
            'password_id': 'Title',
            'username': 'Username',
            'password': 'Password',
            'url': 'Url',
            'comment': 'Note',
        }
        widgets = {
            'password_id': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['itemcategory',]