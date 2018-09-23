# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

STRING_LENGTH_SHORT = 256
STRING_LENGTH_MEDIUM = 1024
STRING_LENGTH_LONG = 16384


class RijpModelBase(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateField(
        null=True,
        blank=True
    )
    deleted = models.DateField(
        null=True,
        blank=True
    )


class Project(RijpModelBase):
    name = models.CharField(
        max_length=STRING_LENGTH_SHORT
    )
    test_templates = None
    test_instances = None


class TestTemplate(RijpModelBase):
    name = models.CharField(
        max_length=STRING_LENGTH_SHORT
    )


class TestInstance(RijpModelBase):
    name = models.CharField(
        max_length=STRING_LENGTH_SHORT
    )


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE
    )
    projects = models.ManyToManyField(
        Project,
        blank=True,
        related_name='projects'
    )
    about = models.CharField(
        max_length=STRING_LENGTH_MEDIUM,
        blank=True
    )
    location = models.CharField(
        max_length=STRING_LENGTH_MEDIUM,
        blank=True
    )
    agency = models.CharField(
        max_length=STRING_LENGTH_MEDIUM,
        blank=True
    )
    department = models.CharField(
        max_length=STRING_LENGTH_MEDIUM,
        blank=True
    )
    telephone = models.CharField(
        max_length=STRING_LENGTH_MEDIUM,
        blank=True
    )
    skype = models.CharField(
        max_length=STRING_LENGTH_MEDIUM,
        blank=True
    )
    birth_date = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return 'Profile of: {0}'.format(self.user)
