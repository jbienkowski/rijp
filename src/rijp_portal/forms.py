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
            'description',
            'priority',
            'is_archived',
        )
        labels = {
            'name': 'Project name',
            'description': 'Description',
            'priority': 'Priority',
            'is_archived': 'Is archived',
        }


class ProjectTestTemplateNewForm(forms.Form):
    template_name = forms.CharField(max_length=20)
    class Meta:
        fields = (
            'template_name',
        )
        labels = {
            'template_name': 'Test template name',
        }