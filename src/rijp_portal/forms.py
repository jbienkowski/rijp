from django.contrib.auth.models import User
from .models import Profile, RijpProject
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'name',
            )
        labels = {
            'name': 'User name',
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = RijpProject
        fields = (
            'name',
        )
        labels = {
            'name': 'Project name',
        }