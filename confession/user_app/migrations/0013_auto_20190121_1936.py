# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-21 19:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0012_auto_20190121_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='u_name',
            field=models.CharField(default='默认用户', max_length=30, verbose_name='用户昵称'),
        ),
    ]
