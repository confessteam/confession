# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-25 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0016_auto_20190121_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='confess',
            name='contentType',
            field=models.IntegerField(default=1, verbose_name='内容类型（1:表白、2：失物招领、3：二手商品、4：其他）'),
        ),
        migrations.AlterField(
            model_name='confess',
            name='release_time',
            field=models.CharField(default='1548398761', max_length=256, verbose_name='发布时间'),
        ),
    ]
