# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-08 05:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chenqi_app', '0005_bugsort'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bugsort',
            name='Pro_zs_one',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='chenqi_app.Pro', verbose_name='\u5173\u8054\u9879\u76ee'),
        ),
        migrations.AlterField(
            model_name='bugsort',
            name='bug_sort1',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u786c\u4ef6\u95ee\u9898'),
        ),
        migrations.AlterField(
            model_name='bugsort',
            name='bug_sort2',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u5ba2\u6237\u7aef\u95ee\u9898'),
        ),
        migrations.AlterField(
            model_name='bugsort',
            name='bug_sort3',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u4e1a\u52a1\u529f\u80fd\u95ee\u9898'),
        ),
        migrations.AlterField(
            model_name='bugsort',
            name='bug_sort4',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u5b89\u5168\u6027\u95ee\u9898'),
        ),
        migrations.AlterField(
            model_name='bugsort',
            name='bug_sort5',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u6613\u7528\u6027\u95ee\u9898'),
        ),
        migrations.AlterField(
            model_name='bugsort',
            name='bug_sort6',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u4e92\u8054\u4e92\u901a\u95ee\u9898'),
        ),
    ]
