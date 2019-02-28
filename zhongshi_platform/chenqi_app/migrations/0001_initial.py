# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-30 11:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pro',
            fields=[
                ('Pro_numbers', models.IntegerField(primary_key=True, serialize=False, verbose_name='\u9879\u76eeID')),
                ('Pro_state', models.CharField(choices=[('\u672a\u5f00\u59cb', '\u672a\u5f00\u59cb'), ('\u8fdb\u884c\u4e2d', '\u8fdb\u884c\u4e2d'), ('\u6682\u505c\u4e2d', '\u6682\u505c\u4e2d'), ('\u5df2\u7ed3\u9879', '\u5df2\u7ed3\u9879')], max_length=30, verbose_name='\u72b6\u6001')),
                ('Pro_name', models.CharField(max_length=30, verbose_name='\u9879\u76ee\u540d\u79f0')),
                ('Pro_ps', models.CharField(choices=[('\u901a\u8fc7', '\u901a\u8fc7'), ('\u672a\u901a\u8fc7', '\u672a\u901a\u8fc7')], max_length=30, verbose_name='\u901a\u8fc7\u72b6\u6001')),
                ('Pro_DI', models.IntegerField(verbose_name='\u9879\u76eeDI\u503c')),
                ('Pro_Fatal_open', models.IntegerField(blank=True, null=True, verbose_name='\u81f4\u547d\u672a\u5173\u95ed')),
                ('Pro_Fatal_close', models.IntegerField(blank=True, null=True, verbose_name='\u81f4\u547d\u5173\u95ed')),
                ('Pro_Serious_open', models.IntegerField(blank=True, null=True, verbose_name='\u4e25\u91cd\u672a\u5173\u95ed')),
                ('Pro_Serious_close', models.IntegerField(blank=True, null=True, verbose_name='\u4e25\u91cd\u5173\u95ed')),
                ('Pro_Common_open', models.IntegerField(blank=True, null=True, verbose_name='\u666e\u901a\u672a\u5173\u95ed')),
                ('Pro_Common_close', models.IntegerField(blank=True, null=True, verbose_name='\u666e\u901a\u5173\u95ed')),
                ('Pro_Lower_open', models.IntegerField(blank=True, null=True, verbose_name='\u8f83\u4f4e\u672a\u5173\u95ed')),
                ('Pro_Lower_close', models.IntegerField(blank=True, null=True, verbose_name='\u8f83\u4f4e\u5173\u95ed')),
                ('Pro_Suggest_open', models.IntegerField(blank=True, null=True, verbose_name='\u5efa\u8bae\u672a\u5173\u95ed')),
                ('Pro_Suggest_close', models.IntegerField(blank=True, null=True, verbose_name='\u5efa\u8bae\u5173\u95ed')),
                ('Pro_People_pr', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u8d1f\u8d23\u4eba')),
                ('Pro_lines', models.TextField(blank=True, max_length=30, null=True, verbose_name='\u4ea7\u7ebf\u4eba\u5458')),
                ('Pro_zs', models.TextField(blank=True, max_length=30, null=True, verbose_name='\u4e2d\u8bd5\u4eba\u5458')),
                ('Pro_nedre_bug', models.TextField(blank=True, max_length=30, null=True, verbose_name='\u672a\u89e3\u51b3\u7684\u4e3b\u8981\u95ee\u9898')),
                ('Pro_leave_bug', models.TextField(blank=True, max_length=30, null=True, verbose_name='\u9057\u7559\u7684\u4e3b\u8981\u95ee\u9898')),
                ('Pro_nedfol_bug', models.TextField(blank=True, max_length=30, null=True, verbose_name='\u9700\u8981\u4ea7\u7ebf\u8ddf\u8e2a\u7684\u95ee\u9898')),
                ('Pro_zs_end', models.TextField(blank=True, max_length=30, null=True, verbose_name='\u6d4b\u8bd5\u7ed3\u8bba')),
                ('Pro_safe_end', models.TextField(blank=True, max_length=30, null=True, verbose_name='\u5b89\u5168\u7ed3\u8bba')),
                ('Pro_Update_Time', models.DateField(null=True, verbose_name='\u9879\u76ee\u521b\u5efa\u65f6\u95f4')),
                ('Pro_Over_Time', models.DateField(blank=True, null=True, verbose_name='\u9879\u76ee\u7ed3\u9879\u65f6\u95f4')),
                ('Pro_Sort', models.CharField(choices=[('\u4e2d\u8bd5\u9879\u76ee', '\u4e2d\u8bd5\u9879\u76ee'), ('\u4e13\u9879', '\u4e13\u9879')], max_length=30, verbose_name='\u9879\u76ee\u7c7b\u578b')),
                ('Pro_lines_name', models.CharField(choices=[('\u4e2d\u8bd5\u9879\u76ee', '\u4e2d\u8bd5\u9879\u76ee'), ('\u4e13\u9879', '\u4e13\u9879')], max_length=30, verbose_name='\u4ea7\u54c1\u7ebf')),
            ],
            options={
                'ordering': ['-Pro_Update_Time'],
            },
        ),
        migrations.CreateModel(
            name='Times',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Time_active', models.CharField(max_length=30, null=True, verbose_name='\u6d4b\u8bd5\u6d3b\u52a8')),
                ('Time_version_num', models.CharField(max_length=30, null=True, verbose_name='\u7248\u672c\u53f7')),
                ('Time_begin', models.DateField(null=True, verbose_name='\u5f00\u59cb\u65e5\u671f')),
                ('Time_end', models.DateField(blank=True, null=True, verbose_name='\u7ed3\u675f\u65e5\u671f')),
                ('Time_use', models.IntegerField(blank=True, null=True, verbose_name='\u5b9e\u9645\u8017\u65f6')),
                ('Pro_zs_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chenqi_app.Pro')),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tool_Id', models.IntegerField(verbose_name='\u6587\u7ae0ID\u53f7')),
                ('Title', models.CharField(max_length=30, null=True, verbose_name='\u6807\u9898')),
                ('Context', models.TextField(verbose_name='\u6587\u7ae0\u5185\u5bb9')),
                ('Content_people', models.CharField(max_length=30, null=True, verbose_name='\u5f00\u53d1\u8005')),
                ('Download1', models.CharField(max_length=30, null=True, verbose_name='\u9644\u4ef61\u540d\u79f0')),
                ('Download_href1', models.FileField(upload_to='chenqi_app/static/share/file', verbose_name='\u9644\u4ef61\u4e0b\u8f7d\u5730\u5740')),
                ('Download2', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u9644\u4ef62\u540d\u79f0')),
                ('Download_href2', models.FileField(blank=True, null=True, upload_to='chenqi_app/static/share/file', verbose_name='\u9644\u4ef62\u4e0b\u8f7d\u5730\u5740')),
                ('Content_Pic', models.ImageField(upload_to='chenqi_app/static/share/pic', verbose_name='\u6587\u7ae0\u56fe')),
                ('Pic_min', models.ImageField(upload_to='chenqi_app/static/share/pic', verbose_name='\u9884\u89c8\u56fe')),
                ('Eff', models.IntegerField(default=1, null=True, verbose_name='\u6709\u6548\u503c')),
                ('Time', models.DateField(null=True, verbose_name='\u53d1\u5e03\u65e5\u671f')),
            ],
        ),
    ]
