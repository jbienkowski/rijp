# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from enum import Enum

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

STRING_LENGTH_SHORT = 256
STRING_LENGTH_MEDIUM = 1024
STRING_LENGTH_LONG = 16384


class RijpModelBase(models.Model):
    PRIORITY_CHOICES = (
        (0, 'Ultra low'),
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Immediate'),
    )
    created = models.DateTimeField(
        default=timezone.now
    )
    modified = models.DateField(
        default=timezone.now
    )
    is_archived = models.BooleanField(
        default=False
    )
    name = models.CharField(
        max_length = STRING_LENGTH_SHORT
    )
    description = models.CharField(
        max_length = STRING_LENGTH_MEDIUM,
        blank = True
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=2
    )

    def get_priority(self):
        return '{} priority'.format(self.PRIORITY_CHOICES[self.priority][1])

    def get_priority_bulma_class(self):
        return {
            0: 'is-white',
            1: 'is-info',
            2: 'is-warning',
            3: 'is-danger',
            4: 'is-black',
        }.get(self.priority)


class RijpProject(RijpModelBase):
    pass


class RijpTestCaseBase(RijpModelBase):
    STATUS_CHOICES = (
        (0, 'Not executed'),
        (1, 'Pass'),
        (2, 'Fail'),
        (3, 'Blocked'),
    )
    prerequisites = models.TextField(
        max_length = STRING_LENGTH_MEDIUM,
        blank = True
    )
    procedure = models.TextField(
        max_length = STRING_LENGTH_MEDIUM,
        blank = True
    )
    data = models.TextField(
        max_length = STRING_LENGTH_MEDIUM,
        blank = True
    )
    expected_result = models.TextField(
        max_length = STRING_LENGTH_MEDIUM,
        blank = True
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0
    )
    remarks = models.TextField(
        max_length = STRING_LENGTH_MEDIUM,
        blank = True
    )
    test_environment = models.TextField(
        max_length = STRING_LENGTH_MEDIUM,
        blank = True
    )

    def get_status(self):
        return 'Test {}'.format(self.STATUS_CHOICES[self.status][1].lower())

    def get_status_bulma_class(self):
        return {
            0: 'is-white',
            1: 'is-success',
            2: 'is-danger',
            3: 'is-warning',
        }.get(self.status)


class RijpTestTemplate(RijpModelBase):
    project = models.ForeignKey(
        RijpProject,
        related_name='test_templates',
        on_delete=models.CASCADE
    )
    

class RijpTestCaseTemplate(RijpTestCaseBase):
    test_template = models.ForeignKey(
        RijpTestTemplate,
        related_name='test_case_templates',
        on_delete=models.CASCADE
    )


class RijpTestInstance(RijpModelBase):
    test_template = models.ForeignKey(
        RijpTestTemplate,
        related_name='test_instances',
        on_delete=models.CASCADE
    )


class RijpTestCaseInstance(RijpTestCaseBase):
    test_instance = models.ForeignKey(
        RijpTestInstance,
        related_name='test_case_instances',
        on_delete=models.CASCADE
    )
    execution_timestamp = models.DateTimeField()
    actual_result = models.CharField(
        max_length = STRING_LENGTH_MEDIUM
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
