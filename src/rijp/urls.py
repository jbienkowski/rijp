from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from accounts import views as accounts_views
from rijp_portal import views as rijp_views

CACHE_TIME_SHORT = int(getattr(settings, "CACHE_TIME_SHORT", 0))
CACHE_TIME_MEDIUM = int(getattr(settings, "CACHE_TIME_MEDIUM", 0))
CACHE_TIME_LONG = int(getattr(settings, "CACHE_TIME_LONG", 0))
URL_BASE = getattr(settings, "URL_BASE", "")

urlpatterns = [
    path(
        '',
        rijp_views.IndexListView.as_view(),
        name='index'
    ),
    #     re_path(
    #     r'^{}user/(?P<username>\w+)/$'.format(URL_BASE),
    #     book_view.UserDetailsListView.as_view(),
    #     name='user_details'
    # ),
    path(
        '{}dashboard/'.format(URL_BASE),
        rijp_views.DashboardListView.as_view(),
        name='dashboard'
    ),
    path(
        '{}archive/'.format(URL_BASE),
        rijp_views.ArchiveListView.as_view(),
        name='archive'
    ),
    re_path(
        r'^{}restore/(?P<object_pk>\w+)/$'.format(URL_BASE),
        rijp_views.object_restore,
        name='object_restore'
    ),
    path(
        '{}projects/'.format(URL_BASE),
        rijp_views.ProjectsListView.as_view(),
        name='projects'
    ),
    re_path(
        r'^{}projects/(?P<project_pk>\w+)/$'.format(URL_BASE),
        rijp_views.ProjectDetailsListView.as_view(),
        name='project_details'
    ),
    path(
        '{}new-project/'.format(URL_BASE),
        rijp_views.project_new,
        name='project_new'
    ),
    re_path(
        r'^{}projects/(?P<project_pk>\w+)/edit/$'.format(URL_BASE),
        rijp_views.project_edit,
        name='project_edit'
    ),
    re_path(
        r'^{}projects/(?P<project_pk>\w+)/archive/$'.format(URL_BASE),
        rijp_views.project_archive,
        name='project_archive'
    ),
    re_path(
        r'^{}projects/(?P<project_pk>\w+)/new-test-template/$'.format(URL_BASE),
        rijp_views.project_test_template_new,
        name='project_test_template_new'
    ),
    re_path(
        r'^{}test-templates/(?P<template_pk>\w+)/$'.format(URL_BASE),
        rijp_views.ProjectTestTemplateDetailsListView.as_view(),
        name='project_test_template_details'
    ),
    re_path(
        r'^{}test-templates/(?P<template_pk>\w+)/edit/$'.format(URL_BASE),
        rijp_views.project_test_template_edit,
        name='project_test_template_edit'
    ),
    re_path(
        r'^{}test-templates/(?P<template_pk>\w+)/archive/$'.format(URL_BASE),
        rijp_views.project_test_template_archive,
        name='project_test_template_archive'
    ),
    re_path(
        r'^{}test-templates/(?P<template_pk>\w+)/new-test-case-template/$'.format(URL_BASE),
        rijp_views.project_test_case_template_new,
        name='project_test_case_template_new'
    ),
    re_path(
        r'^{}test-case-templates/(?P<test_case_template_pk>\w+)/$'.format(URL_BASE),
        rijp_views.ProjectTestCaseTemplateDetailsListView.as_view(),
        name='project_test_case_template_details'
    ),
    re_path(
        r'^{}test-case-templates/(?P<test_case_template_pk>\w+)/edit/$'.format(URL_BASE),
        rijp_views.project_test_case_template_edit,
        name='project_test_case_template_edit'
    ),
    re_path(
        r'^{}test-case-templates/(?P<test_case_template_pk>\w+)/archive/$'.format(URL_BASE),
        rijp_views.project_test_case_template_archive,
        name='project_test_case_template_archive'
    ),
    path(
        '{}tests/'.format(URL_BASE),
        rijp_views.TestsListView.as_view(),
        name='tests'
    ),
    path(
        '{}signup/'.format(URL_BASE),
        accounts_views.signup,
        name='signup'
    ),
    path(
        '{}login/'.format(URL_BASE),
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),
    path(
        '{}logout/'.format(URL_BASE),
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        '{}admin/'.format(URL_BASE),
        admin.site.urls
    ),
    re_path(
        r'^{}settings/account/$'.format(URL_BASE),
        rijp_views.update_profile,
        name='my_account'
    ),
    path(
        '{}reset/'.format(URL_BASE),
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'
    ),
    path(
        '{}reset/done/'.format(URL_BASE),
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    re_path(
        r'^' + URL_BASE + r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        '{}reset/complete/'.format(URL_BASE),
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path(
        '{}settings/password/'.format(URL_BASE),
        auth_views.PasswordChangeView.as_view(
            template_name='password_change.html'
        ),
        name='password_change'
    ),
    path(
        '{}settings/password/done/'.format(URL_BASE),
        auth_views.PasswordChangeDoneView.as_view(
            template_name='password_change_done.html'
        ),
        name='password_change_done'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add custom handlers for the HTTP error codes
# handler404 = 'book.views.custom_404'
# handler500 = 'book.views.custom_500'