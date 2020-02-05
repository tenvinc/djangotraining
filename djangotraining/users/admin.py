# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import AdminUser, Student

# Register your models here.
admin.register(AdminUser)
admin.register(Student)