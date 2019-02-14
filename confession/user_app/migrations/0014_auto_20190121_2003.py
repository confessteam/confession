# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-21 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0013_auto_20190121_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(auto_now=True, verbose_name='出生年月日'),
        ),
        migrations.AddField(
            model_name='user',
            name='signature',
            field=models.CharField(default='我就是我，不一样的烟火', max_length=64, verbose_name='个性签名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='action_time',
            field=models.TimeField(auto_now=True, verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(default='太原市', max_length=64, verbose_name='学校所在市'),
        ),
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.TimeField(auto_now_add=True, verbose_name='用户创建时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='icon',
            field=models.CharField(max_length=256, verbose_name='用户头像'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='123456', max_length=256, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=11, unique=True, verbose_name='手机号'),
        ),
        migrations.AlterField(
            model_name='user',
            name='province',
            field=models.CharField(default='山西省', max_length=64, verbose_name='学校所在省'),
        ),
        migrations.AlterField(
            model_name='user',
            name='school',
            field=models.CharField(default='山西大学', max_length=256, verbose_name='学校名称'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('男性', '男性'), ('女性', '女性'), ('保密', '保密')], default='男性', max_length=4, verbose_name='性别'),
        ),
    ]