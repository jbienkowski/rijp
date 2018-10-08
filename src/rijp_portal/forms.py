from django.contrib.auth.models import User
from .models import Profile, RijpProject, RijpTestTemplate
from django import forms


RIJP_MODEL_BASE_FIELDS = (
    'name',
    'description',
    'priority',
    'is_archived',
    )

RIJP_MODEL_BASE_LABELS = {
    'name': 'Name',
    'description': 'Description',
    'priority': 'Priority',
    'is_archived': 'Is archived',
    }


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
        fields = RIJP_MODEL_BASE_FIELDS
        labels = RIJP_MODEL_BASE_LABELS


class ProjectTestTemplateNewForm(forms.Form):
    template_name = forms.CharField(max_length=20)
    class Meta:
        fields = (
            'template_name',
        )
        labels = {
            'template_name': 'Test template name',
        }

class ProjectTestTemplateForm(forms.ModelForm):
    class Meta:
        model = RijpTestTemplate
        fields = RIJP_MODEL_BASE_FIELDS
        labels = RIJP_MODEL_BASE_LABELS