from django.contrib.auth.models import User
from .models import Profile, Project
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'name',
            )

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'name',
        )