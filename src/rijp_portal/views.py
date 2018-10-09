from django.shortcuts import \
    get_object_or_404, redirect, render, render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.db import transaction

from .models import \
    RijpProject, RijpTestTemplate

from .forms import \
    UserForm, ProfileForm, ProjectForm, \
    ProjectTestTemplateNewForm, ProjectTestTemplateForm


@method_decorator(login_required, name='dispatch')
class IndexListView(ListView):
    model = None
    context_object_name = 'ctx'
    template_name = 'index.html'

    def get_queryset(self):
        return None


@method_decorator(login_required, name='dispatch')
class ProjectsListView(ListView):
    model = RijpProject
    context_object_name = 'ctx'
    template_name = 'projects.html'

    def get_queryset(self):
        queryset = RijpProject.objects.filter(is_archived=False)
        return queryset


@method_decorator(login_required, name='dispatch')
class ProjectDetailsListView(ListView):
    model = RijpProject
    context_object_name = 'ctx'
    template_name = 'project_details.html'

    def get_queryset(self):
        queryset = get_object_or_404(
            RijpProject,
            pk=self.kwargs.get('project_pk')
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProjectTestTemplateNewForm
        return context

    def post(self, request, *args, **kwargs):
        tt = RijpTestTemplate()
        tt.name = self.request.POST.get('template_name')
        tt.project = RijpProject.objects.get(pk=self.kwargs.get('project_pk'))
        tt.save()
        return redirect(
            'project_details', self.kwargs.get('project_pk')
        )


@login_required
def project_edit(request, project_pk):
    obj = get_object_or_404(
        RijpProject,
        pk=project_pk
    )
    cancel_url = reverse(
        'project_details',
        args=[project_pk]
    )
    if request.method == 'POST':
        form = ProjectForm(
            request.POST,
            instance=obj
        )
        if form.is_valid():
            form.save()
            return redirect(
                'project_details',
                project_pk
            )
        else:
            return render(
                request,
                'object_edit.html',
                {
                    'form': form,
                    'ctx': obj,
                    'cancel_url': cancel_url,
                }
            )
    else:
        form = ProjectForm(instance=obj)
        return render(
            request,
            'object_edit.html',
            {
                'form': form,
                'ctx': obj,
                'cancel_url': cancel_url,
            }
        )


@method_decorator(login_required, name='dispatch')
class ProjectTestTemplateDetailsListView(ListView):
    model = RijpTestTemplate
    context_object_name = 'ctx'
    template_name = 'project_test_template_details.html'

    def get_queryset(self):
        queryset = get_object_or_404(
            RijpTestTemplate,
            pk=self.kwargs.get('template_pk')
        )
        return queryset


@login_required
def project_test_template_edit(request, project_pk, template_pk):
    obj = get_object_or_404(
        RijpTestTemplate,
        pk=template_pk
    )
    cancel_url = reverse(
        'project_test_template_details',
        args=[project_pk, template_pk]
    )
    if request.method == 'POST':
        form = ProjectTestTemplateForm(
            request.POST,
            instance=obj
        )
        if form.is_valid():
            form.save()
            return redirect(
                'project_test_template_details',
                project_pk,
                template_pk
            )
        else:
            return render(
                request,
                'object_edit.html',
                {
                    'form': form,
                    'ctx': obj,
                    'cancel_url': cancel_url
                }
            )
    else:
        form = ProjectTestTemplateForm(instance=obj)
        return render(
            request,
            'object_edit.html',
            {
                'form': form,
                'ctx': obj,
                'cancel_url': cancel_url
            }
        )


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

@login_required
def new_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project_form.save()
            return redirect('projects')
        else:
            return render(request, 'project_new.html', {
                'form': project_form
            })
    else:
        project_form = ProjectForm()
        return render(request, 'project_new.html', {
            'form': project_form
        })


@login_required
def new_project_test_template(request, project_pk):
    if request.method == 'POST':
        return render(
            request,
            'project_test_template_new.html'
        )
    else:
        ctx = get_object_or_404(
            RijpProject,
            pk=project_pk
        )
        return render(
            request,
            'project_test_template_new.html',
            {'ctx': ctx}
        )


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

# Templates
@login_required
def view_template(request):
    object = None
    cancel_url = reverse(
        'index'
    )
    if request.method == 'POST':
        form = None(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(
                request,
                'index.html',
                {
                    'form': form,
                    'ctx': object,
                    'cancel_url': cancel_url,
                }
            )
    else:
        form = None(instance=object)
        return render(
            request,
            'index.html',
            {
                'form': form,
                'ctx': object,
                'cancel_url': cancel_url,
            }
        )