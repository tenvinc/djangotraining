# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-02-04 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_adminuser_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='year_of_study',
            field=models.CharField(blank=True, choices=[('Year 2', 'Year 2 (Sophomore)'), ('Year 4', 'Year 4 (Senior)'), ('Year 3', 'Year 3 (Junior)'), ('Year 1', 'Year 1 (Freshman)')], max_length=6),
        ),
    ]
