# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-21 16:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0011_auto_20190121_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='action_time',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
