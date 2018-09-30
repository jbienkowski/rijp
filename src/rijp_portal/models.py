# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from enum import Enum

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
        null = True,
        blank = True
    )
    deleted = models.DateField(
        null = True,
        blank = True
    )
    name = models.CharField(
        max_length = STRING_LENGTH_SHORT
    )


class Project(RijpModelBase):
    pass


class TestTemplate(RijpModelBase):
    proj = models.ForeignKey(
        Project,
        related_name='test_templates',
        on_delete=models.CASCADE
    )


class TestInstance(RijpModelBase):
    test_template = models.ForeignKey(
        TestTemplate,
        related_name='test_instances',
        on_delete=models.CASCADE
    )


class Profile(RijpModelBase):
    user = models.OneToOneField(
        User,
        related_name = 'profile',
        on_delete = models.CASCADE
    )

    def __str__(self):
        return 'Profile of: {0}'.format(self.user)


class RoleDefinition(models.Model):
    pass


class AccessDefinition(models.Model):
    ACCESS_CHOICES = (
        (0, 'Read only'),
        (1, 'Read and write'),
        (9, 'Owner'),
    )

    model = models.ForeignKey(
        RijpModelBase,
        related_name='access_definitions',
        on_delete=models.CASCADE
    )

    level = models.IntegerField(
        choices=ACCESS_CHOICES,
        default=0
    )
