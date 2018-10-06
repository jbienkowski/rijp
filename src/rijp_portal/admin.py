from django.contrib import admin
from .models import *


class RijpModelBaseAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change model base details', {
                'fields': [
                    'name',
                    'description',
                    'is_archived',
                ]
            }
        ),
    ]

    list_display = (
        '__str__',
        'name',
        'description',
        'is_archived',
    )


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change profile details', {
                'fields': [
                    'name',
                ]
            }
        ),
    ]

    list_display = (
        '__str__',
        'user',
        'name',
    )

admin.site.register(RijpModelBase, RijpModelBaseAdmin)
admin.site.register(Profile)
admin.site.register(RijpProject)
admin.site.register(RijpTestTemplate)
admin.site.register(RijpTestCaseTemplate)
admin.site.register(RijpTestInstance)
admin.site.register(RijpTestCaseInstance)
admin.site.register(AccessDefinition)