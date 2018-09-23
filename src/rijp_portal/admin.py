from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change profile details', {
                'fields': [
                    'projects',
                    'about',
                    'location',
                    'agency',
                    'department',
                    'telephone',
                    'skype',
                    'birth_date',
                ]
            }
        ),
    ]

    list_display = (
        '__str__',
        'user',
        'about',
        'location',
        'birth_date',
    )

admin.site.register(Profile, ProfileAdmin)
