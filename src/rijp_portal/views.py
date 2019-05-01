from django.shortcuts import \
    get_object_or_404, redirect, render, render_to_response
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.db import transaction

from .models import \
    RijpModelBase, RijpProject, RijpTestTemplate, RijpTestCaseTemplate

from .forms import \
    RijpModelBaseForm, UserForm, ProfileForm, ProjectForm, \
    ProjectTestTemplateNewForm, ProjectTestTemplateForm, \
    ProjectTestCaseTemplateForm


def handle_object_edit_request(request, object, form, url_next, desc='edited'):
    if request.method == 'POST':
        f = form(request.POST, instance=object)
        print(f)
        if f.is_valid():
            f.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                '{} {}!'.format(object.name, desc)
            )
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


def handle_object_archive_request(request, object, url_next):
    if request.method == 'POST':
        f = RijpModelBaseForm(request.POST)
        print(f)
        if f.is_valid():
            object.is_archived = True
            object.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                '{} archived!'.format(object.name)
            )
            return redirect(url_next)
        else:
            return render(
                request,
                'object_archive.html',
                {
                    'form': f,
                    'ctx': object,
                    'url_next': url_next,
                }
            )
    else:
        f = RijpModelBaseForm()
        return render(
            request,
            'object_archive.html',
            {
                'form': f,
                'ctx': object,
                'url_next': url_next,
            }
        )


def handle_object_restore_request(request, object, url_next):
    if request.method == 'POST':
        f = RijpModelBaseForm(request.POST)
        print(f)
        if f.is_valid():
            object.is_archived = False
            object.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                '{} restored!'.format(object.name)
            )
            return redirect(url_next)
        else:
            return render(
                request,
                'object_restore.html',
                {
                    'form': f,
                    'ctx': object,
                    'url_next': url_next,
                }
            )
    else:
        f = RijpModelBaseForm()
        return render(
            request,
            'object_restore.html',
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


@login_required
def project_new(request):
    obj = RijpProject()
    url_next = reverse(
        'projects'
    )
    return handle_object_edit_request(
        request, obj, ProjectForm, url_next, 'created'
    )


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


@login_required
def project_archive(request, project_pk):
    obj = get_object_or_404(
        RijpProject,
        pk=project_pk
    )
    url_next = reverse(
        'projects'
    )
    return handle_object_archive_request(
        request, obj, url_next
    )


@login_required
def object_restore(request, object_pk):
    obj = get_object_or_404(
        RijpModelBase,
        pk=object_pk
    )
    url_next = reverse(
        'archive'
    )
    return handle_object_restore_request(
        request, obj, url_next
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


@login_required
def project_test_template_new(request, project_pk):
    obj = RijpTestTemplate()
    obj.name = request.POST.get('template_name')
    obj.project = RijpProject.objects.get(pk=project_pk)
    url_next = reverse(
        'project_details',
        args=[project_pk]
    )
    return handle_object_edit_request(
        request, obj, ProjectTestTemplateForm, url_next, 'created'
    )

@login_required
def project_test_template_edit(request, template_pk):
    obj = get_object_or_404(
        RijpTestTemplate,
        pk=template_pk
    )
    url_next = reverse(
        'project_details',
        args=[obj.project.pk]
    )
    return handle_object_edit_request(
        request, obj, ProjectTestTemplateForm, url_next
    )


@login_required
def project_test_template_archive(request, template_pk):
    obj = get_object_or_404(
        RijpTestTemplate,
        pk=template_pk
    )
    url_next = reverse(
        'project_details',
        args=[obj.project.pk]
    )
    return handle_object_archive_request(
        request, obj, url_next
    )


@method_decorator(login_required, name='dispatch')
class ProjectTestCaseTemplateDetailsListView(ListView):
    model = RijpTestCaseTemplate
    context_object_name = 'ctx'
    template_name = 'project_test_case_template_details.html'

    def get_queryset(self):
        queryset = get_object_or_404(
            RijpTestCaseTemplate,
            pk=self.kwargs.get('test_case_template_pk')
        )
        return queryset


@login_required
def project_test_case_template_new(request, template_pk):
    obj = RijpTestCaseTemplate()
    obj.name = request.POST.get('name')
    obj.description = request.POST.get('description')
    obj.prerequisites = request.POST.get('prerequisites')
    obj.procedure = request.POST.get('procedure')
    obj.data = request.POST.get('data')
    obj.expected_result = request.POST.get('expected_result')
    obj.status = 0
    obj.remarks = request.POST.get('remarks')
    obj.test_environment = request.POST.get('test_environment')
    obj.test_template = RijpTestTemplate.objects.get(
        pk=template_pk
    )
    url_next = reverse(
        'project_test_template_details',
        args=[template_pk]
    )
    return handle_object_edit_request(
        request, obj, ProjectTestCaseTemplateForm, url_next, 'created'
    )


@login_required
def project_test_case_template_edit(request, test_case_template_pk):
    obj = get_object_or_404(
        RijpTestCaseTemplate,
        pk=test_case_template_pk
    )
    url_next = reverse(
        'project_test_case_template_details',
        args=[test_case_template_pk]
    )
    return handle_object_edit_request(
        request, obj, ProjectTestCaseTemplateForm, url_next
    )


@login_required
def project_test_case_template_archive(request, test_case_template_pk):
    obj = get_object_or_404(
        RijpTestCaseTemplate,
        pk=test_case_template_pk
    )
    url_next = reverse(
        'project_test_template_details',
        args=[obj.test_template.pk]
    )
    return handle_object_archive_request(
        request, obj, url_next
    )


@method_decorator(login_required, name='dispatch')
class DashboardListView(ListView):
    model = None
    template_name = 'dashboard.html'

    def get_queryset(self):
        return None


@method_decorator(login_required, name='dispatch')
class ArchiveListView(ListView):
    model = RijpModelBase
    context_object_name = 'ctx'
    template_name = 'archive.html'

    def get_queryset(self):
        queryset = RijpModelBase.objects.filter(is_archived=True)
        return queryset


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
        profile_form = None #ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid(): #and profile_form.is_valid():
            user_form.save()
            # profile_form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'User details updated!'
            )
            return redirect('my_account')
        else:
            return render(request, 'my_account.html', {
                'user_form': user_form,
                'profile_form': profile_form
                })
    else:
        user_form = UserForm(instance=request.user)
        profile_form = None #ProfileForm(instance=request.user.profile)
        return render(request, 'my_account.html', {
            'user_profile': request.user.profile,
            'form': user_form,
            'profile_form': profile_form
            })
