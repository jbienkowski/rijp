from django.shortcuts import \
    get_object_or_404, redirect, render, render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.db import transaction

from .models import \
    RijpProject, RijpTestTemplate, RijpTestCaseTemplate

from .forms import \
    UserForm, ProfileForm, ProjectForm, \
    ProjectTestTemplateNewForm, ProjectTestTemplateForm, \
    ProjectTestCaseTemplateForm


def handle_object_edit_request(request, object, form, url_next):
    if request.method == 'POST':
        f = form(request.POST, instance=object)
        if f.is_valid():
            f.save()
            return redirect(url_next)
        else:
            return render(
                request,
                'object_edit.html',
                {
                    'form': f,
                    'ctx': object,
                    'url_next': url_next,
                }
            )
    else:
        f = form(instance=object)
        return render(
            request,
            'object_edit.html',
            {
                'form': f,
                'ctx': object,
                'url_next': url_next,
            }
        )


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
def project_new(request):
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
def project_edit(request, project_pk):
    obj = get_object_or_404(
        RijpProject,
        pk=project_pk
    )
    url_next = reverse(
        'project_details',
        args=[project_pk]
    )
    return handle_object_edit_request(
        request, obj, ProjectForm, url_next
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProjectTestCaseTemplateForm
        return context

    def post(self, request, *args, **kwargs):
        tt = RijpTestCaseTemplate()
        tt.name = self.request.POST.get('name')
        tt.description = self.request.POST.get('description')
        tt.prerequisites = self.request.POST.get('prerequisites')
        tt.procedure = self.request.POST.get('procedure')
        tt.data = self.request.POST.get('data')
        tt.expected_result = self.request.POST.get('expected_result')
        tt.status = self.request.POST.get('status')
        tt.remarks = self.request.POST.get('remarks')
        tt.test_environment = self.request.POST.get('test_environment')
        tt.test_template = RijpTestTemplate.objects.get(
            pk=self.kwargs.get('template_pk')
        )
        tt.save()
        return redirect(
            'project_test_template_details',
            self.kwargs.get('project_pk'),
            self.kwargs.get('template_pk')
        )


@login_required
def project_test_template_new(request, project_pk):
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
def project_test_template_edit(request, project_pk, template_pk):
    obj = get_object_or_404(
        RijpTestTemplate,
        pk=template_pk
    )
    url_next = reverse(
        'project_test_template_details',
        args=[project_pk, template_pk]
    )
    return handle_object_edit_request(
        request, obj, ProjectTestTemplateForm, url_next
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
