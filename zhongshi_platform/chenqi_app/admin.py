# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Tool,Pro,Times,BugSort


# Register your models here.

admin.site.site_header = '中试管理平台后台'
admin.site.site_title = '中试管理平台后台'

class Toollist(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = ('Title','Content_people','Context','Tool_Id','Eff')
    empty_value_display = ' -em- '
    list_editable = ['Content_people','Context','Eff']
    list_filter = ('Content_people','Eff')
    search_fields = ('Title','Content_people',)

class Pro_zs_list(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = ('Pro_numbers', 'Pro_state', 'Pro_name', 'Pro_People_pr','Pro_Update_Time','Pro_Over_Time')
    empty_value_display = ' -em- '

class Times_Version_list(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = ('Time_active', 'Time_version_num', 'Time_begin', 'Time_end','Time_use','Pro_zs_one')
    empty_value_display = ' -em- '

class BugSort_list(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = ('bug_sort1', 'bug_sort2', 'bug_sort3', 'bug_sort4','bug_sort5','bug_sort6','bug_sort7','Pro_zs_one')
    empty_value_display = ' -em- '

admin.site.register(Tool,Toollist)
admin.site.register(Pro,Pro_zs_list)
admin.site.register(Times,Times_Version_list)
admin.site.register(BugSort,BugSort_list)

# class img_up(admin.ModelAdmin):
#     list_display = ('id','img','single')
#     filter_horizontal = ('imgs',)
#
# admin.site.register(Imgs, img_up)
