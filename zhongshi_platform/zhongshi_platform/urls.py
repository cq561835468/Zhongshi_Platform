#coding=utf-8
"""zhongshi_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from chenqi_app import views as cq_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^bug_up_pie/(.+)/$', cq_views.bug_up_pie, name='bug_up_pie'),   #饼图接口
    url(r'^bug_up/(.+)/$', cq_views.bug_up,name='bug_up'),                #柱状图接口
    url(r'^project/download/(.+)/$', cq_views.download_list, name='download_list'),   #项目数据下载接口
    url(r'^tool/tool_main/(.+)/$',cq_views.Tool_main,name='tool_main'),
    url(r'^tool/', cq_views.tool,name='tool'),
    url(r'^project_main/', cq_views.manage, name='manage'),
    url(r'^project/(.+)/$', cq_views.info, name='manage_info'),
    url(r'^index/', cq_views.index,name='index'),
    url(r'^sit_keda/', cq_views.sit,name='sit'),
    url(r'^context/(.+)/$', cq_views.context,name='context'),
    url(r'^project_new/', cq_views.manage_new_pro,name='projectnew'),
    #url(r'^download/(.+)/$', cq_views.download_file,name='download'),
    url(r'^download/(.+)/$', cq_views.download_file,name='download'),
    #url(r'^background/tool_add/$', cq_views.tool_add,name='tool_add'),
    #url(r'^background/data_test/$', cq_views.insert_table,name='data_test'),
    url(r'^$',cq_views.zhongshi,name='zhongshi'),
]
