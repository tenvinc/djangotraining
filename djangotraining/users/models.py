# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


# Special information specific to a student
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    CHOICES_FOR_YR = {
        ("Year 1", "Year 1 (Freshman)"),
        ("Year 2", "Year 2 (Sophomore)"),
        ("Year 3", "Year 3 (Junior)"),
        ("Year 4", "Year 4 (Senior)")
    }
    full_name = models.CharField(max_length=100, blank=True)
    year_of_study = models.CharField(max_length=6, choices=CHOICES_FOR_YR, blank=True)
    course = models.CharField(max_length=100, blank=True)
    weight = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    height = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return "Student : %s" % (self.full_name)


class AdminUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "Admin User: %s" % (self.user.username)
