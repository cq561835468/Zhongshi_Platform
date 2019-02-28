# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models



class Tool(models.Model):
    Tool_Id = models.IntegerField(verbose_name='文章ID号')
    Title = models.CharField(max_length=30,null=True,verbose_name='标题')
    #Context = models.CharField(max_length=300,null=True)
    Context = models.TextField(verbose_name='文章内容')
    Content_people = models.CharField(max_length=30,null=True,verbose_name='开发者')
    Download1 = models.CharField(max_length=30,null=True,verbose_name='附件1名称')
    #Download_href1 = models.CharField(max_length=30,null=True)
    Download_href1 = models.FileField(upload_to='chenqi_app/static/share/file',verbose_name='附件1下载地址')
    Download2 = models.CharField(max_length=30,null=True,blank=True,verbose_name='附件2名称')
    #Download_href2 = models.CharField(max_length=30,null=True,blank=True)
    Download_href2 = models.FileField(null=True,blank=True,upload_to='chenqi_app/static/share/file',verbose_name='附件2下载地址')
    #Content_Pic = models.CharField(max_length=100, null=True)
    Content_Pic = models.ImageField(upload_to='chenqi_app/static/share/pic',verbose_name='文章图')
    Pic_min = models.ImageField(upload_to='chenqi_app/static/share/pic',verbose_name='预览图')
    Eff = models.IntegerField(null=True,verbose_name='有效值',default=1)
    Time = models.DateField(null=True,verbose_name='发布日期')

class Pro(models.Model):
    Pro_numbers = models.IntegerField(verbose_name='项目ID',primary_key=True)
    Pro_state_value = (
        (u'未开始', u'未开始'),
        (u'进行中', u'进行中'),
        (u'暂停中', u'暂停中'),
        (u'已结项', u'已结项'),
    )
    Pro_pass_state = (
        (u'通过', u'通过'),
        (u'未通过', u'未通过'),
    )
    Pro_Sort_choic = (
        (u'中试项目', u'中试项目'),
        (u'专项', u'专项'),
    )
    Pro_state = models.CharField(max_length=30, verbose_name='状态', choices=Pro_state_value)
    Pro_name = models.CharField(max_length=30, verbose_name='项目名称')
    Pro_Sort = models.CharField(max_length=30, verbose_name='项目类型', choices=Pro_Sort_choic)
    Pro_lines_name = models.CharField(max_length=30, verbose_name='产品线')
    Pro_ps = models.CharField(max_length=30, verbose_name='通过状态', choices=Pro_pass_state)
    Pro_DI = models.FloatField(verbose_name='项目DI值')
    Pro_Fatal_open = models.IntegerField(null=True,blank=True,verbose_name='致命未关闭')
    Pro_Fatal_close = models.IntegerField(null=True,blank=True,verbose_name='致命关闭')
    Pro_Serious_open = models.IntegerField(null=True,blank=True,verbose_name='严重未关闭')
    Pro_Serious_close = models.IntegerField(null=True,blank=True,verbose_name='严重关闭')
    Pro_Common_open = models.IntegerField(null=True,blank=True,verbose_name='普通未关闭')
    Pro_Common_close = models.IntegerField(null=True,blank=True,verbose_name='普通关闭')
    Pro_Lower_open = models.IntegerField(null=True,blank=True,verbose_name='较低未关闭')
    Pro_Lower_close = models.IntegerField(null=True,blank=True,verbose_name='较低关闭')
    Pro_Suggest_open = models.IntegerField(null=True,blank=True,verbose_name='建议未关闭')
    Pro_Suggest_close = models.IntegerField(null=True,blank=True,verbose_name='建议关闭')
    Pro_People_pr = models.CharField(max_length=30,null=True,blank=True,verbose_name='负责人')
    Pro_lines = models.TextField(max_length=1000,null=True,blank=True,verbose_name='产线人员')
    Pro_zs = models.TextField(max_length=1000, null=True,blank=True, verbose_name='中试参与人员')
    Pro_nedre_bug = models.TextField(max_length=1000, null=True,blank=True,verbose_name='未解决的主要问题')
    Pro_leave_bug = models.TextField(max_length=1000, null=True,blank=True, verbose_name='遗留的主要问题')
    Pro_nedfol_bug = models.TextField(max_length=1000, null=True,blank=True, verbose_name='需要产线跟踪的问题')
    Pro_zs_end = models.TextField(max_length=1000, null=True,blank=True, verbose_name='测试结论')
    Pro_safe_end = models.TextField(max_length=1000, null=True,blank=True, verbose_name='安全结论')
    # Pro_Testver = models.IntegerField(null=True,verbose_name='版本数')
    Pro_Update_Time = models.DateField(null=True, verbose_name='项目创建时间')
    Pro_Over_Time = models.DateField(null=True,blank=True,verbose_name='项目结项时间')
    Pro_People_pr_old = models.CharField(max_length=300,null=True,blank=True,verbose_name='负责人_老的')


    # def __str__(self):
    #     return self.Pro_numbers

    class Meta:
        ordering = ['-Pro_Update_Time']



class Times(models.Model):
    Time_active = models.CharField(max_length=30,null=True, verbose_name='测试活动')
    Time_version_num = models.CharField(max_length=30,null=True, verbose_name='版本号')
    Time_begin = models.DateField(null=True,verbose_name='开始日期')
    Time_end = models.DateField(null=True,blank=True,verbose_name='结束日期')
    Time_use = models.IntegerField(null=True,blank=True,verbose_name='实际耗时')
    Pro_zs_one = models.ForeignKey(Pro)

    def __unicode__(self):
        return str(self.id)

class BugSort(models.Model):
    bug_sort1 = models.IntegerField(null=True, blank=True, verbose_name='硬件问题')
    bug_sort2 = models.IntegerField(null=True, blank=True, verbose_name='客户端问题')
    bug_sort3 = models.IntegerField(null=True, blank=True, verbose_name='业务功能问题')
    bug_sort4 = models.IntegerField(null=True, blank=True, verbose_name='安全性问题')
    bug_sort5 = models.IntegerField(null=True, blank=True, verbose_name='易用性问题')
    bug_sort6 = models.IntegerField(null=True, blank=True, verbose_name='互联互通问题')
    bug_sort7 = models.IntegerField(null=True, blank=True, verbose_name='其他产品问题')
    Pro_zs_one = models.OneToOneField(Pro, on_delete=models.CASCADE,verbose_name='关联项目')

    def __unicode__(self):
        a = []
        a.append(str(self.id))
        a.append(str(self.bug_sort1))
        #return str(self.id)
        return "%s,%s,%s,%s,%s,%s,%s,%s" % (str(self.id),str(self.bug_sort1),str(self.bug_sort2),str(self.bug_sort3),
                                         str(self.bug_sort4),str(self.bug_sort5),str(self.bug_sort6),
                                         str(self.bug_sort7))
