# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-26 18:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belt_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='joined_users',
            field=models.ManyToManyField(related_name='joined_trips', to='belt_app.User'),
        ),
        migrations.AddField(
            model_name='trip',
            name='planner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='planned_trips', to='belt_app.User'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='endDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='trip',
            name='startDate',
            field=models.DateField(),
        ),
    ]