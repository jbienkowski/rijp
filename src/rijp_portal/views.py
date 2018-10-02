from django.shortcuts import \
    get_object_or_404, redirect, render, render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.db import transaction

from .models import \
    Project

from .forms import \
    UserForm, ProfileForm, ProjectForm


@method_decorator(login_required, name='dispatch')
class IndexListView(ListView):
    model = None
    context_object_name = 'ctx'
    template_name = 'index.html'

    def get_queryset(self):
        return None


@method_decorator(login_required, name='dispatch')
class ProjectsListView(ListView):
    model = Project
    context_object_name = 'ctx'
    template_name = 'projects.html'

    def get_queryset(self):
        queryset = Project.objects.all()
        return queryset


@method_decorator(login_required, name='dispatch')
class DashboardListView(ListView):
    model = None
    template_name = 'dashboard.html'

    def get_queryset(self):
        return None


@method_decorator(login_required, name='dispatch')
class TestsListView(ListView):
    model = None
    template_name = 'tests.html'

    def get_queryset(self):
        return None


def new_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project_form.save()
            return redirect('projects')
        else:
            return render(request, 'new_project.html', {
                'project_form': project_form
            })
    else:
        project_form = ProjectForm()
        return render(request, 'new_project.html', {
            'project_form': project_form
        })


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('my_account')
        else:
            return render(request, 'my_account.html', {
                'user_form': user_form, 'profile_form': profile_form
                })
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'my_account.html', {
            'user_profile': request.user.profile,
            'user_form': user_form,
            'profile_form': profile_form
            })