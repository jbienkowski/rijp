from django.contrib import admin
from .models import *

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

admin.site.register(RijpModelBase)
admin.site.register(Profile)
admin.site.register(RijpProject)
admin.site.register(RijpTestTemplate)
admin.site.register(RijpTestInstance)
admin.site.register(AccessDefinition)