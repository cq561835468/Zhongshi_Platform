# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-30 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chenqi_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pro',
            name='Pro_lines_name',
            field=models.CharField(max_length=30, verbose_name='\u4ea7\u54c1\u7ebf'),
        ),
    ]
