# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from .models import Times,Pro
from django.forms import ModelForm
from django.contrib.admin import widgets

# class pro_info_begin(forms.Form):
#     user_id = forms.IntegerField()
#     user_name = forms.CharField(widget=forms.TextInput(attrs={"type":"date"}))
#     email = forms.EmailField()

'''开始项目表单'''
class pro_info_begin(forms.ModelForm):
    class Meta:
        model = Times
        fields = ("Time_active","Time_version_num","Time_begin")
        widgets = {'Time_begin': forms.TextInput(attrs={"type": "date"})}

'''停止项目表单'''
class pro_info_stop(forms.ModelForm):
    class Meta:
        model = Times
        fields = ("Time_end","Time_use")
        widgets = {'Time_end': forms.TextInput(attrs={"type": "date"})}

'''结束项目表单'''
class pro_info_end(forms.ModelForm):
    class Meta:
        model = Pro
        fields = ("Pro_Over_Time","Pro_ps")
        widgets = {'Pro_Over_Time': forms.TextInput(attrs={"type": "date"})}

'''新建项目表单'''
class pro_info_new(forms.ModelForm):
    class Meta:
        model = Pro
        fields = ("Pro_name","Pro_Sort","Pro_lines_name","Pro_People_pr")