# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-10 19:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0007_auto_20190110_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='confess',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='confess',
            name='release_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
