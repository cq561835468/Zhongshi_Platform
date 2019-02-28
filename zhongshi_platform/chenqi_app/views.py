# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import StreamingHttpResponse
from chenqi_app import models
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q
from pyexcel_io import get_data
from forms import pro_info_begin,pro_info_stop,pro_info_end,pro_info_new
import xlrd
import os
import json
import datetime
import sys
from operator import  itemgetter
from excel_bug_get import excel_bug,excel_write

'''json时间方法重写'''
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

'''BUG表操作'''
class bugs_do_it():
    def __init__(self):
        self.bugs_sort = models.BugSort()
    def All_bug_sort(self,pro_num):
        Data_Bug = models.BugSort.objects.filter(id=pro_num).values_list('bug_sort1','bug_sort2','bug_sort3','bug_sort4','bug_sort5','bug_sort6','bug_sort7')
        return Data_Bug

    def All_bug_new(self,pro_num,bug_sort1=None,bug_sort2=None,bug_sort3=None,bug_sort4=None,bug_sort5=None,bug_sort6=None,bug_sort7=None):
        self.bugs_sort.bug_sort1 = bug_sort1
        self.bugs_sort.bug_sort2 = bug_sort2
        self.bugs_sort.bug_sort3 = bug_sort3
        self.bugs_sort.bug_sort4 = bug_sort4
        self.bugs_sort.bug_sort5 = bug_sort5
        self.bugs_sort.bug_sort6 = bug_sort6
        self.bugs_sort.bug_sort7 = bug_sort7
        self.bugs_sort.Pro_zs_one = models.Pro.objects.get(Pro_numbers=pro_num)
        self.bugs_sort.save()

    def All_bug_updata(self,bug_sort1,bug_sort2,bug_sort3,bug_sort4,bug_sort5,bug_sort6,bug_sort7,ID):
        models.BugSort.objects.filter(id=ID).update(bug_sort1=bug_sort1,bug_sort2=bug_sort2,bug_sort3=bug_sort3,
                                                    bug_sort4=bug_sort4,bug_sort5=bug_sort5,bug_sort6=bug_sort6,
                                                    bug_sort7=bug_sort7)

'''time表操作'''
class active_do_it():
    def __init__(self,Active_name=None,Active_version_num=None,Active_begin=None,
                 Active_end=None,Active_Use=None,Active_zs_one=None):
        self.Active_name = Active_name
        self.Active_version_num = Active_version_num
        self.Active_begin = Active_begin
        self.Active_end = Active_end
        self.Active_Use = Active_Use
        self.Active_zs_one = Active_zs_one
        self.times_db = models.Times()
    def begin_pro(self):
        self.times_db.Time_active = self.Active_name
        self.times_db.Time_version_num = self.Active_version_num
        self.times_db.Time_begin = self.Active_begin
        self.times_db.Pro_zs_one = models.Pro.objects.get(Pro_numbers=self.Active_zs_one)
        self.times_db.save()
    def stop_pro(self):
        models.Times.objects.filter(Time_end=None).update(Time_use=self.Active_Use)
        models.Times.objects.filter(Time_end=None).update(Time_end=self.Active_end)

'''pro表操作'''
class pro_do_it():
    def __init__(self,Pro_state=None,Pro_name=None,Pro_ps=None,Pro_DI=None,Pro_People_pr=None,
                 Pro_zs=None,Pro_nedre_bug=None,Pro_leave_bug=None,Pro_nedfol_bug=None,Pro_zs_end=None,
                 Pro_safe_end=None,Pro_Update_Time_be=None,Pro_Update_Time_ed=None,Pro_Over_Time=None,
                 Pro_Over_Time_be=None,Pro_Over_Time_ed=None,Pro_num_post=None,Pro_Search_post=None,
                 Pro_Fatal_open=None,Pro_Fatal_close=None,Pro_Serious_open=None,Pro_Serious_close=None,
                 Pro_Common_open=None,Pro_Common_close=None,Pro_Lower_open=None,Pro_Lower_close=None,
                 Pro_Suggest_open=None,Pro_Suggest_close=None,Pro_Sort=None,Pro_lines_name=None,
                 Pro_Update_Time=None,Pro_lines=None):
        self.Pro_state = Pro_state
        self.Pro_name = Pro_name
        self.Pro_ps = Pro_ps
        self.Pro_Sort = Pro_Sort
        self.Pro_Update_Time = Pro_Update_Time
        self.Pro_lines_name = Pro_lines_name
        self.Pro_DI = Pro_DI
        self.Pro_People_pr = Pro_People_pr
        self.Pro_zs = Pro_zs
        self.Pro_nedre_bug = Pro_nedre_bug
        self.Pro_leave_bug = Pro_leave_bug
        self.Pro_nedfol_bug = Pro_nedfol_bug
        self.Pro_zs_end = Pro_zs_end
        self.Pro_safe_end = Pro_safe_end
        self.Pro_Update_Time_be = Pro_Update_Time_be
        self.Pro_Update_Time_ed = Pro_Update_Time_ed
        self.Pro_Over_Time = Pro_Over_Time
        self.Pro_Over_Time_be = Pro_Over_Time_be
        self.Pro_Over_Time_ed = Pro_Over_Time_ed
        self.Pro_num_post = Pro_num_post
        self.Pro_Search_post = Pro_Search_post
        self.Pro_lines = Pro_lines
        #-------------------
        self.Pro_Fatal_open = Pro_Fatal_open
        self.Pro_Fatal_close = Pro_Fatal_close
        self.Pro_Serious_open = Pro_Serious_open
        self.Pro_Serious_close = Pro_Serious_close
        self.Pro_Common_open = Pro_Common_open
        self.Pro_Common_close = Pro_Common_close
        self.Pro_Lower_open = Pro_Lower_open
        self.Pro_Lower_close = Pro_Lower_close
        self.Pro_Suggest_open = Pro_Suggest_open
        self.Pro_Suggest_close = Pro_Suggest_close
        self.pro_db = models.Pro()

    '''新建项目'''
    def new_pro(self):
        nowTime = datetime.datetime.now()
        nownumber = models.Pro.objects.all().order_by('-Pro_numbers').values_list('Pro_numbers')
        if nownumber:
            num = nownumber[0][0] + 1
        else:
            num = 1
        self.pro_db.Pro_numbers = num
        self.pro_db.Pro_state = self.Pro_state
        self.pro_db.Pro_name = self.Pro_name
        self.pro_db.Pro_Sort = self.Pro_Sort
        self.pro_db.Pro_lines_name = self.Pro_lines_name
        self.pro_db.Pro_ps = u'未通过'
        self.pro_db.Pro_DI = 0
        self.pro_db.Pro_People_pr = self.Pro_People_pr
        self.pro_db.Pro_Update_Time = nowTime
        self.pro_db.Pro_Over_Time = None
        self.pro_db.save()
        bugs_do_it().All_bug_new(pro_num=num) #调用新建bug关联表

    '''关联项目状态'''
    def update_state(self):
        models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).update(Pro_state=self.Pro_state)

    '''更新缺陷具体值'''
    def update_bug_value(self):
        models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).update(Pro_Fatal_open=self.Pro_Fatal_open,
                                                                        Pro_Fatal_close=self.Pro_Fatal_close,
                                                                        Pro_Serious_open=self.Pro_Serious_open,
                                                                        Pro_Serious_close=self.Pro_Serious_close,
                                                                        Pro_Common_open=self.Pro_Common_open,
                                                                        Pro_Common_close=self.Pro_Common_close,
                                                                        Pro_Lower_open=self.Pro_Lower_open,
                                                                        Pro_Lower_close=self.Pro_Lower_close,
                                                                        Pro_Suggest_open=self.Pro_Suggest_open,
                                                                        Pro_Suggest_close=self.Pro_Suggest_close)

    '''关闭项目更新的数据'''
    def end_pro(self):
        models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).update(Pro_state=self.Pro_state)
        models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).update(Pro_ps=self.Pro_ps)
        models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).update(Pro_Over_Time=self.Pro_Over_Time)

    '''查询所有数据:详情页'''
    def select_detail_info(self):
        Pro_data = models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).values_list('Pro_numbers','Pro_state','Pro_name','Pro_Sort','Pro_lines_name','Pro_ps',
                                   'Pro_DI','Pro_Fatal_open','Pro_Fatal_close','Pro_Serious_open','Pro_Serious_close',
                                   'Pro_Common_open','Pro_Common_close','Pro_Lower_open','Pro_Lower_close','Pro_Suggest_open',
                                    'Pro_Suggest_close','Pro_People_pr','Pro_lines','Pro_zs','Pro_nedre_bug',
                                    'Pro_leave_bug','Pro_nedfol_bug','Pro_zs_end','Pro_safe_end','Pro_Update_Time',
                                    'Pro_Over_Time','Pro_People_pr_old')
        return Pro_data

    '''查询版本信息'''
    def select_all_data_fk(self):
        Pro_data = models.Pro.objects.get(Pro_numbers=self.Pro_num_post)
        pd = Pro_data.times_set.all().values_list('Time_active','Time_version_num','Time_begin','Time_end','Time_use','Pro_zs_one')
        return pd

    '''查询所有数据'''
    def select_index(self):
        Pro_data = models.Pro.objects.all().values_list('Pro_numbers','Pro_state','Pro_name','Pro_Fatal_open','Pro_Fatal_close',
                                                        'Pro_Serious_open','Pro_Serious_close','Pro_Common_open','Pro_Common_close',
                                                        'Pro_Lower_open','Pro_Lower_close','Pro_Suggest_open','Pro_Suggest_close',
                                                        'Pro_People_pr','Pro_Update_Time','Pro_Over_Time')
        return Pro_data

    '''查询状态:主页'''
    def select_index_filter_Pro_state(self):
        if self.Pro_Search_post:
            Pro_data = models.Pro.objects.filter(Pro_state = self.Pro_Search_post).values_list('Pro_numbers', 'Pro_state', 'Pro_name', 'Pro_Fatal_open',
                                                                                                'Pro_Fatal_close','Pro_Serious_open', 'Pro_Serious_close',
                                                                                                'Pro_Common_open','Pro_Common_close','Pro_Lower_open',
                                                                                                'Pro_Lower_close', 'Pro_Suggest_open','Pro_Suggest_close',
                                                                                                'Pro_People_pr', 'Pro_Update_Time', 'Pro_Over_Time')
            return Pro_data
        return self.select_index()

    '''查询功能:项目名模糊查询'''
    def select_index_filter_Pro_name(self):
        if self.Pro_Search_post:
            Pro_data = models.Pro.objects.filter(Q(Pro_name__icontains = self.Pro_Search_post)).values_list('Pro_numbers', 'Pro_state', 'Pro_name', 'Pro_Fatal_open',
                                                                                                'Pro_Fatal_close','Pro_Serious_open', 'Pro_Serious_close',
                                                                                                'Pro_Common_open','Pro_Common_close','Pro_Lower_open',
                                                                                                'Pro_Lower_close', 'Pro_Suggest_open','Pro_Suggest_close',
                                                                                                'Pro_People_pr', 'Pro_Update_Time', 'Pro_Over_Time')
            return Pro_data
        return self.select_index()

    '''查询功能:负责人模糊查询'''
    def select_index_filter_Pro_People_pr(self):
        if self.Pro_Search_post:
            Pro_data = models.Pro.objects.filter(Q(Pro_People_pr__icontains = self.Pro_Search_post)).values_list('Pro_numbers', 'Pro_state', 'Pro_name', 'Pro_Fatal_open',
                                                                                                'Pro_Fatal_close','Pro_Serious_open', 'Pro_Serious_close',
                                                                                                'Pro_Common_open','Pro_Common_close','Pro_Lower_open',
                                                                                                'Pro_Lower_close', 'Pro_Suggest_open','Pro_Suggest_close',
                                                                                                'Pro_People_pr', 'Pro_Update_Time', 'Pro_Over_Time')
            return Pro_data
        return self.select_index()

    '''查询功能:时间模糊查询'''
    def select_index_filter_time_end(self):
        if not self.Pro_Over_Time_be:  #起始为假
            if not self.Pro_Over_Time_ed:  #结束为假
                return self.select_index()
            else:  #结束为真
                Pro_data = models.Pro.objects.filter(Pro_Over_Time__lte=self.Pro_Over_Time_ed).values_list('Pro_numbers','Pro_state',
                                                                                                           'Pro_name','Pro_Fatal_open',
                                                                                                           'Pro_Fatal_close','Pro_Serious_open',
                                                                                                           'Pro_Serious_close','Pro_Common_open',
                                                                                                           'Pro_Common_close','Pro_Lower_open',
                                                                                                           'Pro_Lower_close','Pro_Suggest_open',
                                                                                                           'Pro_Suggest_close','Pro_People_pr',
                                                                                                           'Pro_Update_Time','Pro_Over_Time')
                return Pro_data
        else: #起始为真
            if not self.Pro_Over_Time_ed: #结束为假
                Pro_data = models.Pro.objects.filter(Pro_Over_Time__gte=self.Pro_Over_Time_be).values_list('Pro_numbers','Pro_state',
                                                                                                        'Pro_name','Pro_Fatal_open',
                                                                                                        'Pro_Fatal_close','Pro_Serious_open',
                                                                                                        'Pro_Serious_close','Pro_Common_open',
                                                                                                        'Pro_Common_close','Pro_Lower_open',
                                                                                                        'Pro_Lower_close','Pro_Suggest_open',
                                                                                                        'Pro_Suggest_close','Pro_People_pr',
                                                                                                        'Pro_Update_Time', 'Pro_Over_Time')
                return Pro_data
            else:
                Pro_data = models.Pro.objects.filter(Pro_Over_Time__gte=self.Pro_Over_Time_be,
                                                     Pro_Over_Time__lte=self.Pro_Over_Time_ed).values_list('Pro_numbers','Pro_state',
                                                                                                        'Pro_name','Pro_Fatal_open',
                                                                                                        'Pro_Fatal_close','Pro_Serious_open',
                                                                                                        'Pro_Serious_close','Pro_Common_open',
                                                                                                        'Pro_Common_close','Pro_Lower_open',
                                                                                                        'Pro_Lower_close','Pro_Suggest_open',
                                                                                                        'Pro_Suggest_close','Pro_People_pr',
                                                                                                        'Pro_Update_Time', 'Pro_Over_Time')
                return Pro_data

    '''更新DI值'''
    def Update_DI(self):
        Pro_data = models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).update(Pro_DI=self.Pro_DI)
        return Pro_data

    '''bug类型获取'''
    def Select_Id_For_All_bug_sort(self):
        Prodata = models.Pro.objects.get(Pro_numbers=self.Pro_num_post)
        Pro_datas = Prodata.bugsort
        # print Pro_datas
        return Pro_datas

    '''更新项目人员'''
    def Updata_Pepole_lines(self):
        Prodata = models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).update(Pro_lines=self.Pro_lines)
        return Prodata

    '''更新项目负责人'''
    def Updata_Pepole_main(self):
        new_people = models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).values_list('Pro_People_pr')
        old_people = models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).values_list('Pro_People_pr_old')
        new_peoples = '' if not new_people[0][0] else new_people[0][0]
        old_peoples = '' if not old_people[0][0] else old_people[0][0]
        Prodata2 = models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).update(Pro_People_pr_old=old_peoples+new_peoples+' ')
        Prodata = models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).update(Pro_People_pr=self.Pro_People_pr)
        return Prodata

    '''更新项目中式人员'''
    def Updata_Pepole_zs(self):
        Prodata = models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).update(Pro_zs=self.Pro_zs)
        return Prodata

    '''更新未解决的主要问题'''
    def Updata_PNB(self):
        Prodata = models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).update(Pro_nedre_bug=self.Pro_nedre_bug)
        return Prodata

    '''更新遗留的主要问题'''
    def Updata_PLB(self):
        Prodata = models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).update(Pro_leave_bug=self.Pro_leave_bug)
        return Prodata

    '''更新需要产线跟踪的问题'''
    def Updata_PFB(self):
        Prodata = models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).update(Pro_nedfol_bug=self.Pro_nedfol_bug)
        return Prodata

    '''更新测试结论'''
    def Updata_ZE(self):
        Prodata = models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).update(Pro_zs_end=self.Pro_zs_end)
        return Prodata

    '''更新安全结论'''
    def Updata_SE(self):
        Prodata = models.Pro.objects.filter(Pro_numbers=self.Pro_num_post).update(Pro_safe_end=self.Pro_safe_end)
        return Prodata


'''BUG处理类类'''
class Tool_arrw():
    def __init__(self,dict=None):
        self.dict = dict

    def bug_calc(self):
        '''统计bug数量'''
        dicts = {}
        for bug_info in ['Pro_Fatal_open','Pro_Fatal_close','Pro_Serious_open','Pro_Serious_close','Pro_Common_open',
                          'Pro_Common_close','Pro_Lower_open','Pro_Lower_close','Pro_Suggest_open','Pro_Suggest_close']:
            self.dict[bug_info] = 0 if self.dict[bug_info] == "--" else self.dict[bug_info]
        #bug数量计算
        dicts["Pro_Fatal_Bug"] = self.dict['Pro_Fatal_open'] + self.dict['Pro_Fatal_close']
        dicts["Pro_Serious_Bug"] = self.dict['Pro_Serious_open'] + self.dict['Pro_Serious_close']
        dicts["Pro_Common_Bug"] = self.dict['Pro_Common_open'] + self.dict['Pro_Common_close']
        dicts["Pro_Lower_Bug"] = self.dict['Pro_Lower_open'] + self.dict['Pro_Lower_close']
        dicts["Pro_Suggest_Bug"] = self.dict['Pro_Suggest_open'] + self.dict['Pro_Suggest_close']
        dicts["Pro_All_Bug"] = dicts["Pro_Fatal_Bug"] + dicts["Pro_Serious_Bug"] + dicts["Pro_Common_Bug"] + \
                               dicts["Pro_Lower_Bug"] + dicts["Pro_Suggest_Bug"]
        return dicts

    def look_to_zero(self,arrw):
        for index,value in enumerate(arrw):
            arrw[index] = 0 if value == '--' else value
        return arrw

    """给与两个关闭未关闭数组返回总数组"""
    def get_all_buglist(self,arrw1,arrw2):
        list = []
        list_all = [['致命','严重','普通','较低','建议'],
                    [],
                    [],
                    []]
        arrw1 = self.look_to_zero(arrw1)
        arrw2 = self.look_to_zero(arrw2)
        for index,value in enumerate(arrw1):
            list.append(arrw1[index]+arrw2[index])
        list_all[1] = list
        list_all[2] = arrw1
        list_all[3] = arrw2
        epl = excel_bug().Pro_Zero_list(list_all)
        return epl

    '''自动统计DI值，入参{open_bug:[],close:[]}'''
    def bug_DI_cacl(self,arrws):
        All_Di_li = 0
        arrw = [10,3,1,0.1,0.1]
        for index,value in enumerate(arrws['Open_Bug']):
            All_Di_li += arrw[index] * arrws['Open_Bug'][index]
        return All_Di_li

    '''分割返回字符串的数据整成数组'''
    def list_spilt(self,a):
        return str(a).split(',')

    '''获取bug类型返回类型名和对应值'''
    def bug_sort(self,num):
        return_list = []
        list_bug=[]
        arrw_list = [u"硬件", u"客户端", u"业务功能", u"安全性", u"易用性",u"互联互通",u"其他产品问题"]
        Bug_list_id = pro_do_it(Pro_num_post=num).Select_Id_For_All_bug_sort() #取出项目对应类型
        all_bug = self.list_spilt(Bug_list_id)[1:]    #第一位是ID，不要
        for index,value in enumerate(arrw_list):
            dict_tmp = {}
            dict_tmp['value']=all_bug[index]
            dict_tmp['name'] = value
            list_bug.append(dict_tmp)
        return_list.append(arrw_list)
        return_list.append(list_bug)
        return return_list

'''工具页面路径处理'''
def del_app_path(path):
    path_t = path[path.index('/'):]
    return path_t

'''主页面'''
def index(request):
    '''主页'''
    return render(request,'chenqi_app/index.html')

'''返回项目编号:num对应的time表数据['Time_active','Time_version_num','Time_begin','Time_end','Time_use']'''
def Get_pro_to_time(num):
    p_num = models.Pro.objects.get(Pro_numbers=num)
    Time_Id = p_num.times_set.all()
    arrw = []
    for indexx, tid in enumerate(Time_Id):
        dict = {}
        Time_data = models.Times.objects.filter(id=tid.id).values_list('Time_active',
                                                                       'Time_version_num',
                                                                       'Time_begin',
                                                                       'Time_end',
                                                                       'Time_use',)
        for index, value in enumerate(['Time_active','Time_version_num','Time_begin',
                                       'Time_end','Time_use']):
            if not Time_data[0][index]:
                dict[value] = '--'
                continue
            dict[value] = Time_data[0][index]
        arrw.append(dict)
    return arrw

'''工时转换为具体天数'''
def time_to_day(data):
    time_all = 0
    for dic_one in data:
        if dic_one['Time_use'] == "--":
            dic_one['Time_use'] = "--"
            continue
        time_all += dic_one['Time_use']
    day = time_all / 8
    day += 1 if time_all % 8 > 0 else 0
    time_alls = "%d小时 共%s天" % (time_all, day)
    return time_alls

'''管理主页数据转换'''
def manage_index_data(i,dict):
    # print "i is %s" % i
    # print "dict is %s" % dict
    #print i[0]
    Time_use = 0
    arrw_version = []
    #工时计算
    for indexx, tid in enumerate(Get_pro_to_time(i[0])):
        Time_use += 0 if tid['Time_use'] == '--' else tid['Time_use']
        arrw_version.append(tid['Time_version_num'])  #统计版本数量用
    dict["Pro_Update_Time"] = dict["Pro_Update_Time"].strftime("%Y-%m-%d") if not dict["Pro_Update_Time"] == '--' else dict["Pro_Update_Time"]
    dict["Pro_Over_Time"] = dict["Pro_Over_Time"].strftime("%Y-%m-%d") if not dict["Pro_Over_Time"] == '--'else dict["Pro_Over_Time"]
    # dict["Time_begin"] = dict["Pro_Update_Time"] = dict["Pro_Update_Time"].strftime("%Y-%m-%d")
    # dict["Time_end"] = dict["Pro_Over_Time"] = dict["Pro_Over_Time"].strftime("%Y-%m-%d")
    #版本数计算
    dict["vernum"] = len({}.fromkeys(arrw_version).keys())
    #工时
    dict["timeall"] = Time_use
    #各等级缺陷计算
    retu_cacl = Tool_arrw(dict).bug_calc()
    for i in ['Pro_Fatal_Bug','Pro_Serious_Bug','Pro_Common_Bug','Pro_Lower_Bug','Pro_Suggest_Bug',"Pro_All_Bug"]:
        dict[i] = retu_cacl[i]
    return dict

'''将数据库数据转换为对应字典'''
def data_to_dict(data,dict_arrw):
    dict = {}
    for index,value in enumerate(dict_arrw):
        if data[index] == None or data[index] == '':
            dict[value] = '--'
            continue
        dict[value] = data[index]
    return dict

'''工具主页类'''
class manage_info():
    def __init__(self,Pro_datas=None,renturn_data=None,Search_data=None):
        self.Pro_data = Pro_datas
        self.renturn_data = renturn_data
        self.Search_data = Search_data
    '''分割项目主页数据'''
    def main_post_html(self):
        data = []
        for i in self.Pro_data:
            dict = data_to_dict(i,['Pro_numbers', 'Pro_state', 'Pro_name', 'Pro_Fatal_open',
                                   'Pro_Fatal_close','Pro_Serious_open', 'Pro_Serious_close',
                                   'Pro_Common_open','Pro_Common_close','Pro_Lower_open',
                                   'Pro_Lower_close', 'Pro_Suggest_open','Pro_Suggest_close',
                                   'Pro_People_pr', 'Pro_Update_Time', 'Pro_Over_Time']) #dict分解字典none为--
            # print dict
            if i[1] == u'未开始':
                dict = manage_index_data(i, dict)
                for ii in ['Pro_end_time','Pro_Fatal_Bug','Pro_Serious_Bug','Pro_Common_Bug',
                           'Pro_Lower_Bug','Pro_Suggest_Bug','Pro_All_Bug','Time_begin','Time_end','timeall','vernum']:
                    dict[ii] = '--'

            elif i[1] == u'进行中':
                dict = manage_index_data(i,dict)
            elif i[1] == u'暂停中':
                dict = manage_index_data(i, dict)
            elif i[1] == u'已结项':
                dict = manage_index_data(i, dict)
            data.append(dict)

        return data

    def main_filter(self):
        list = []
        manage_post = manage_info(self.renturn_data).main_post_html()  # 分割项目数据
        self.Search_data = '全部' if not self.Search_data else self.Search_data  # 判断是否为空
        list.append(manage_post)
        list.append(self.Search_data)
        return list

    '''分割下载数据'''
    def Download_Data_Change(self,arrw):
        dict = data_to_dict(arrw, ['Pro_numbers','Pro_state','Pro_name','Pro_Sort','Pro_lines_name','Pro_ps',
                                   'Pro_DI','Pro_Fatal_open','Pro_Fatal_close','Pro_Serious_open','Pro_Serious_close',
                                   'Pro_Common_open','Pro_Common_close','Pro_Lower_open','Pro_Lower_close','Pro_Suggest_open',
                                    'Pro_Suggest_close','Pro_People_pr','Pro_lines','Pro_zs','Pro_nedre_bug',
                                    'Pro_leave_bug','Pro_nedfol_bug','Pro_zs_end','Pro_safe_end','Pro_Update_Time',
                                    'Pro_Over_Time'])  # dict分解字典none为--
        re_nid = manage_index_data(arrw,dict)
        for ss in ["Pro_Fatal_open","Pro_Fatal_close",'Pro_Serious_open','Pro_Serious_close','Pro_Common_open','Pro_Common_close',
                  'Pro_Lower_open','Pro_Lower_close','Pro_Suggest_open','Pro_Suggest_close']:
            re_nid.pop(ss)
        return dict

'''项目类'''
class pro_tool():
    def __init__(self,pro_name=None):
        self.pro_name = pro_name

    '''详情页中统计开启和关闭的缺陷'''
    def info_detail(self):
        list_open = []
        list_close = []
        All_data = pro_do_it(Pro_num_post=self.pro_name).select_detail_info()
        dict_pro = data_to_dict(All_data[0],['Pro_numbers','Pro_state','Pro_name','Pro_Sort','Pro_lines_name','Pro_ps',
                                   'Pro_DI','Pro_Fatal_open','Pro_Fatal_close','Pro_Serious_open','Pro_Serious_close',
                                   'Pro_Common_open','Pro_Common_close','Pro_Lower_open','Pro_Lower_close','Pro_Suggest_open',
                                    'Pro_Suggest_close','Pro_People_pr','Pro_lines','Pro_zs','Pro_nedre_bug',
                                    'Pro_leave_bug','Pro_nedfol_bug','Pro_zs_end','Pro_safe_end','Pro_Update_Time',
                                    'Pro_Over_Time','Pro_People_pr_old'])
        for i in ['Pro_Fatal_open','Pro_Serious_open','Pro_Common_open','Pro_Lower_open','Pro_Suggest_open']:
            list_open.append(dict_pro[i])
            dict_pro.pop(i)
        dict_pro['list_open'] = list_open
        for ii in ['Pro_Fatal_close','Pro_Serious_close','Pro_Common_close','Pro_Lower_close','Pro_Suggest_close']:
            list_close.append(dict_pro[ii])
            dict_pro.pop(ii)
        dict_pro['list_close'] = list_close
        return dict_pro

    def count_list_pro(self,arrw):
        list_arrw = []
        for i in arrw:
            list_arrw.append(str(i['Pro_numbers']))
        list_arrw = '|'.join(list_arrw)
        return list_arrw

    '''缺陷统计'''
    def time_calc_ajax(self,arrw):
        for i in range(3,8):
            arrw[i] = arrw[i] + arrw[i+1]
            del arrw[i+1]
        sum = arrw[3]+arrw[4]+arrw[5]+arrw[6]+arrw[7]
        arrw.insert(8,sum)
        return arrw

    '''none转0'''
    def none_to_zero(self,arrw):
        for index,value in enumerate(arrw):
            arrw[index] = 0 if value == None or value == '' else value
        return arrw

    '''0转--'''
    def zero_look(self,arrw):
        for index,value in enumerate(arrw):
            if index in (3,4,5,6,7,8):
                continue
            arrw[index] = '--' if value == 0 else value
        return arrw

    '''数据库数组转为通常数组'''
    def arrw_data_to_arrw(self,arrw):
        list_r = []
        for i in arrw:
            list_r.append(list(i))
        return list_r

    '''序号添加'''
    def sord_number_add(self,arrw):
        for index,value in enumerate(arrw):
            value.append(index+1)
        return arrw

    '''处理数据库返回的数据用于解决ajax问题'''
    def ajax_data_pro(self,arrw):
        list_return = []
        list_r = self.arrw_data_to_arrw(arrw)
        for pro in list_r:
            arrw_version = []
            Time_use = 0
            pro_zero = self.none_to_zero(pro)
            pro_zeros = self.time_calc_ajax(pro_zero)
            '''统计工时和版本号'''
            for indexx, tid in enumerate(Get_pro_to_time(pro[0])):
                Time_use += 0 if tid['Time_use'] == '--' else tid['Time_use']
                arrw_version.append(tid['Time_version_num'])  # 统计版本数量用
            version_len = len({}.fromkeys(arrw_version).keys())  #版本数
            pro_zeros.append(Time_use)
            pro_zeros.append(version_len)
            pro_zeros = self.zero_look(pro_zeros)
            if pro_zeros[1] == u"未开始":
                for i in range(3,9):
                    pro_zeros[i] = '--'
                for i in range(11, 14):
                    pro_zeros[i] = '--'
            list_return.append(pro_zeros)
        list_return = sorted(list_return,key=itemgetter(0),reverse=True)
        list_return_n = self.sord_number_add(list_return)
        return list_return_n

    '''计算当前页和最后页面'''
    def last_cur_page(self,arrw):
        lists =[]
        page = 0
        if len(arrw)%15 > 0:
            page = len(arrw)/15 +1
        else:
            page = len(arrw)/15
        for s in range(1,page+1):
            lists.append(s)
        return lists

'''工具页面'''
@csrf_protect
def tool(request):
    if request.method == "GET":
        search_name='全部'
        data =[]
        All_data = models.Tool.objects.filter(Eff=1).order_by('-Tool_Id').values_list('Title','Context',
                                                                                      'Content_people','Pic_min',
                                                                                      'Download_href1','Tool_Id','Time')
        for i in All_data:
            dict = {}
            dict['tool_name']=i[0]
            dict['content_text']=i[1]
            dict['content_people']=i[2]
            dict['content_ico'] = del_app_path(i[3])
            dict['download'] = del_app_path(i[4])
            dict['ID'] = i[5]
            dict['Time'] = i[6]
            data.append(dict)
        return render(request,'chenqi_app/tool2.html',{'data': data,'search_name':search_name})
    elif request.method == "POST":
        search = request.POST.get("search")
        if not search:
            search=''
            search_name='全部'
        else:
            search_name = search
        data =[]
        All_data = models.Tool.objects.filter(Q(Title__icontains=search)).order_by('-Tool_Id').values_list('Title',
                                                                                                            'Context',
                                                                                                            'Content_people',
                                                                                                            'Pic_min',
                                                                                                            'Download_href1',
                                                                                                            'Tool_Id',
                                                                                                            'Time')

        for i in All_data:
            dict = data_to_dict(All_data[0],['tool_name', 'content_text', 'content_people', 'content_ico', 'download', 'ID','Time'])
            dict['tool_name']=i[0]
            dict['content_text']=i[1]
            dict['content_people']=i[2]
            dict['content_ico']=del_app_path(i[3])
            dict['download']=del_app_path(i[4])
            dict['ID'] = i[5]
            dict['Time'] = i[6]
            data.append(dict)
        return render(request,'chenqi_app/tool2.html',{'data': data,'search_name':search_name})

'''上传文件'''
def upload_file(file,title):
    '''上传文件调用函数'''
    if file == None:
        return 0
    folder = os.path.join(r"chenqi_app\static\share"+"\\", title)
    file_path = os.path.join(r"chenqi_app\static\share"+"\\", title,file.name)
    if not os.path.exists(folder):
        os.makedirs(folder)
    f = open(file_path, mode="wb")
    for i in file.chunks():
        f.write(i)
    f.close()
    return file_path

'''欢迎页面'''
def zhongshi(request):

    return render(request,'chenqi_app/zhongshi.html')

'''下载文件'''
def download_file(request,the_file_name):
    filename = r'chenqi_app\static\share\\'+ the_file_name # 要下载的文件路径
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name[the_file_name.find('/')+1:])
    return response

'''下载函数'''
def readFile(filename, chunk_size=512):

    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

'''工具详情页'''
def Tool_main(request,id):
    All_data = models.Tool.objects.filter(Tool_Id=id).values_list('Title','Context',
                                                                  'Content_people','Download1',
                                                                  'Download_href1','Download2',
                                                                  'Download_href2','Content_Pic',
                                                                  'Time')

    for i in All_data:
        dict = {}
        dict2 = {}
        dict2[i[3]]=del_app_path(i[4])
        if i[5]:
            dict2[i[5]]=del_app_path(i[6])
        dict['tool_name'] = i[0]
        dict['content_text'] = i[1]
        dict['content_people'] = i[2]
        con_png = i[7].split('|')
        for num,value in enumerate(con_png):
            con_png[num] = del_app_path(value)
        dict['content_png'] = con_png
        dict['download']=dict2
        dict['Time'] = i[8]
    return render(request,'chenqi_app/Tool_main.html',{'data':dict})

'''座位页面'''
def sit(request):
    path = r'E:\svn\django_vue\Django\zhongshi_platform\chenqi_app\static\sit_keda\12月份最新座位图.xls'
    excel = {}
    xls = xlrd.open_workbook(path,formatting_info=True)
    data = get_data(path)
    for name_sheet in xls.sheet_names():
        excel_data = {}
        merge_arrw_all = []
        sh = xls.sheet_by_name(name_sheet)
        if not data[name_sheet][0]:
            for i in range(0,sh.ncols):
                data[name_sheet][0].append('')
        else:
            for i in range(0,sh.ncols-len(data[name_sheet][0])):
                data[name_sheet][0].append('')
        for crange in sh.merged_cells:
            merge_dist_add = {}
            rs, re, cs, ce = crange
            merge_dist_add['row'] = rs
            merge_dist_add['col'] = cs
            merge_dist_add['rowspan'] = re - rs
            merge_dist_add['colspan'] = ce - cs
            merge_arrw_all.append(merge_dist_add)
        excel_data[json.dumps(data[name_sheet])] = json.dumps(merge_arrw_all)
        excel[name_sheet] = excel_data
    return render(request,'chenqi_app/sit_keda.html',{"data":excel})

'''中试管理项目主页面'''
def manage(request):
    if request.method == 'GET':
        '''正常请求'''
        renturn_data = pro_do_it(Pro_Search_post='').select_index_filter_Pro_state()  # 数据库查询
        data = manage_info(renturn_data=renturn_data, Search_data='').main_filter()  # 分解数据
        pro_list = pro_tool().count_list_pro(data[0]) #下载列表数据
        list_rd = pro_tool().ajax_data_pro(renturn_data) #ajax数据
        page = pro_tool().last_cur_page(list_rd) #计算当前页和最后页
        form_beg = pro_info_new()  #新建项目
        return render(request, 'chenqi_app/manage_ajax.html',{"data":list_rd[0:15],"search_name":len(list_rd),
                                                              "Pro_list":pro_list,"page_list":page,"current_page":1,
                                                              "new_pro":form_beg})
    else:
        '''POST请求'''
        Search_State = request.POST.get('pro_state')
        Ju_value = request.POST.get('select')
        Pro_Name = request.POST.get('pro_name')
        Begin_Time_Manager = request.POST.get('begin_time_manager')
        End_Time_Manager = request.POST.get('end_time_manager')
        Begin_Time_Ver = request.POST.get('begin_time_ver')
        End_Time_Ver = request.POST.get('end_time_ver')
        Page_Go = request.POST.get('page_go')
        if Ju_value == u'状态':
            Search_State = '' if Search_State == u'全部' else Search_State
            renturn_data = pro_do_it(Pro_Search_post=Search_State).select_index_filter_Pro_state()  # 数据库查询
            list_rd = pro_tool().ajax_data_pro(renturn_data)
            data = manage_info(renturn_data = renturn_data).main_filter() #分解数据
            pro_list = pro_tool().count_list_pro(data[0]).replace('|','%7C') +'/'
            page = pro_tool().last_cur_page(list_rd)  # 计算当前页和最后页
            return HttpResponse(json.dumps({"data": list_rd[(int(Page_Go)-1)*15:int(Page_Go)*15],"search_name":len(list_rd),"Pro_list":pro_list,"page_list":page,"current_page":Page_Go},cls=DateEncoder))
        elif Ju_value == u'项目名称':
            renturn_data = pro_do_it(Pro_Search_post=Pro_Name).select_index_filter_Pro_name()  # 数据库查询
            list_rd = pro_tool().ajax_data_pro(renturn_data)
            data = manage_info(renturn_data = renturn_data).main_filter() #分解数据
            pro_list = pro_tool().count_list_pro(data[0])
            page = pro_tool().last_cur_page(list_rd)  # 计算当前页和最后页
            return HttpResponse(json.dumps(
                {"data": list_rd[(int(Page_Go) - 1) * 15:int(Page_Go) * 15], "search_name": len(list_rd),
                 "Pro_list": pro_list, "page_list": page, "current_page": Page_Go}, cls=DateEncoder))
        elif Ju_value == u'负责人':
            renturn_data = pro_do_it(Pro_Search_post=Pro_Name).select_index_filter_Pro_People_pr()  # 数据库查询
            list_rd = pro_tool().ajax_data_pro(renturn_data)
            data = manage_info(renturn_data = renturn_data).main_filter() #分解数据
            pro_list = pro_tool().count_list_pro(data[0])
            page = pro_tool().last_cur_page(list_rd)  # 计算当前页和最后页
            return HttpResponse(json.dumps(
                {"data": list_rd[(int(Page_Go) - 1) * 15:int(Page_Go) * 15], "search_name": len(list_rd),
                 "Pro_list": pro_list, "page_list": page, "current_page": Page_Go}, cls=DateEncoder))
        elif Ju_value == u'结项时间':
            print 'is me'
            renturn_data = pro_do_it(Pro_Over_Time_be=Begin_Time_Manager,Pro_Over_Time_ed=End_Time_Manager).select_index_filter_time_end()
            list_rd = pro_tool().ajax_data_pro(renturn_data)
            data = manage_info(renturn_data=renturn_data).main_filter()  # 分解数据
            pro_list = pro_tool().count_list_pro(data[0])
            page = pro_tool().last_cur_page(list_rd)  # 计算当前页和最后页
            return HttpResponse(json.dumps(
                {"data": list_rd[(int(Page_Go) - 1) * 15:int(Page_Go) * 15], "search_name": len(list_rd),
                 "Pro_list": pro_list, "page_list": page, "current_page": Page_Go}, cls=DateEncoder))
        elif Ju_value == u'版本数':
            Begin_Time_Ver = 0 if not Begin_Time_Ver else Begin_Time_Ver
            End_Time_Ver = 0 if not End_Time_Ver else End_Time_Ver
            renturn_data = pro_do_it(Pro_Search_post='').select_index_filter_Pro_state()  # 数据库查询
            list_rd = pro_tool().ajax_data_pro(renturn_data)
            data = manage_info(renturn_data=renturn_data, Search_data='').main_filter()  # 分解数据
            pro_list = pro_tool().count_list_pro(data[0])
            list = []
            for i in list_rd:
                i[-1] = '0' if i[-1] == '--' else i[-1]
                if int(i[-1]) < int(Begin_Time_Ver) or int(i[-1]) > int(End_Time_Ver):
                    continue
                list.append(i)
            page = pro_tool().last_cur_page(list)  # 计算当前页和最后页
            return HttpResponse(json.dumps(
                {"data": list[(int(Page_Go) - 1) * 15:int(Page_Go) * 15], "search_name": len(list),
                 "Pro_list": pro_list, "page_list": page, "current_page": Page_Go}, cls=DateEncoder))
        return HttpResponse("error")

'''新建项目接口'''
def manage_new_pro(request):
    form_pro = pro_info_new(request.POST)
    if form_pro.is_valid():
        id_Pro_Name = request.POST.get("Pro_name")
        id_Pro_Sort = request.POST.get("Pro_Sort")
        id_Pro_lines_name = request.POST.get("Pro_lines_name")
        id_Pro_People_pr = request.POST.get("Pro_People_pr")
        pro_do_it(Pro_state=u'未开始',Pro_name=id_Pro_Name,Pro_Sort=id_Pro_Sort,Pro_lines_name=id_Pro_lines_name,
                            Pro_People_pr=id_Pro_People_pr).new_pro()
        return HttpResponseRedirect("/project_main/")

'''中试项目详情页'''
@csrf_protect
def info(request,pro_name):
    if request.method == "GET":
        All_data = pro_tool(pro_name=pro_name).info_detail()
        if All_data['Pro_state'] == u"未开始":
            form_pro_begin = pro_info_begin()
            # data:版本工时主体 time_len:最后一列合并单元格行数 time_all:总工时 state:页面判断当前项目状态 forms:按钮弹窗内容
            # data_pro 项目相关所有信息内容
            # list_open list_name list_close 缺陷柱状图
            Post_Bug_data = Tool_arrw().get_all_buglist(All_data['list_open'], All_data['list_close']) #处理柱状表
            Bug_Sort_List = Tool_arrw().bug_sort(num=pro_name)
            return render(request, 'chenqi_app/manage_info.html',{"data": "", "time_len": "",
                                                                  "time_all": "","state":0,
                                                                  'forms_begin':form_pro_begin,
                                                                  "data_pro":All_data,
                                                                  "list_open":Post_Bug_data[3],
                                                                  "list_close": Post_Bug_data[2],
                                                                  "list_name":json.dumps(Post_Bug_data[0]),
                                                                  "pic_data1":json.dumps(Bug_Sort_List[0]),
                                                                  "pic_data2":json.dumps(Bug_Sort_List[1])})
        elif All_data['Pro_state'] == u"进行中":
            form_pro_stop = pro_info_stop()  #获取表格数据
            data = Get_pro_to_time(pro_name)#获取工时详情
            time_all = time_to_day(data)    #计算工时总计
            Post_Bug_data = Tool_arrw().get_all_buglist(All_data['list_open'], All_data['list_close'])
            Bug_Sort_List = Tool_arrw().bug_sort(num=pro_name)
            return render(request, 'chenqi_app/manage_info.html',{"data":data,"time_len":len(data),
                                                                  "time_all":time_all,"state":1,
                                                                  'forms_stop':form_pro_stop,
                                                                  "data_pro":All_data,
                                                                  "list_open":Post_Bug_data[3],
                                                                  "list_close": Post_Bug_data[2],
                                                                  "list_name":json.dumps(Post_Bug_data[0])})
        elif All_data['Pro_state'] == u"暂停中":
            form_pro_begin = pro_info_begin()
            form_pro_end = pro_info_end()
            data = Get_pro_to_time(pro_name)
            time_all = time_to_day(data)
            Post_Bug_data = Tool_arrw().get_all_buglist(All_data['list_open'], All_data['list_close'])
            Bug_Sort_List = Tool_arrw().bug_sort(num=pro_name)
            return render(request, 'chenqi_app/manage_info.html',{"data":data,"time_len":len(data),
                                                                  "time_all":time_all,"state":2,
                                                                  'forms_begin':form_pro_begin,'forms_end':form_pro_end,
                                                                  "data_pro":All_data,
                                                                  "list_open":Post_Bug_data[3],
                                                                  "list_close": Post_Bug_data[2],
                                                                  "list_name":json.dumps(Post_Bug_data[0]),
                                                                  "pic_data1":json.dumps(Bug_Sort_List[0]),
                                                                  "pic_data2":json.dumps(Bug_Sort_List[1])})
        elif All_data['Pro_state'] == u"已结项":
            form_pro = pro_info_end()
            data = Get_pro_to_time(pro_name)
            time_all = time_to_day(data)
            Post_Bug_data = Tool_arrw().get_all_buglist(All_data['list_open'], All_data['list_close'])
            Bug_Sort_List = Tool_arrw().bug_sort(num=pro_name)
            return render(request, 'chenqi_app/manage_info.html',{"data":data,"time_len":len(data),
                                                                  "time_all":time_all,"state":3,
                                                                  'forms':form_pro,"data_pro":All_data,
                                                                  "list_open":Post_Bug_data[3],
                                                                  "list_close": Post_Bug_data[2],
                                                                  "list_name":json.dumps(Post_Bug_data[0]),
                                                                  "pic_data1":json.dumps(Bug_Sort_List[0]),
                                                                  "pic_data2":json.dumps(Bug_Sort_List[1])})
    else:
        state_value = request.POST.get("stata_value")
        pro_num = request.POST.get("pro_num")
        if state_value == "begin":
            #开始按钮触发
            form_pro = pro_info_begin(request.POST)
            if form_pro.is_valid():
                Time_active = form_pro.cleaned_data['Time_active']
                Time_version_num = form_pro.cleaned_data['Time_version_num']
                Time_begin = form_pro.cleaned_data['Time_begin']
                active_do_it(Active_name=Time_active, Active_version_num=Time_version_num,
                             Active_begin=Time_begin, Active_zs_one=pro_num).begin_pro()
                pro_do_it(Pro_state=u'进行中', Pro_num_post=pro_num).update_state()
                return HttpResponseRedirect("/project/" + pro_num + "/")
        elif state_value == "stop":
            #停止按钮触发
            form_pro = pro_info_stop(request.POST)
            if form_pro.is_valid():
                #print "---pro_info_stop---"
                Time_end = form_pro.cleaned_data['Time_end']
                Time_use = form_pro.cleaned_data['Time_use']
                active_do_it(Active_end=Time_end,Active_Use=Time_use).stop_pro()
                pro_do_it(Pro_state=u'暂停中', Pro_num_post=pro_num).update_state()
                return HttpResponseRedirect("/project/" + pro_num + "/")
        elif state_value == "end":
            #结束按钮触发
            form_pro = pro_info_end(request.POST)
            if form_pro.is_valid():
                Time_end = form_pro.cleaned_data['Pro_Over_Time']
                Pass_state = form_pro.cleaned_data['Pro_ps']
                # all_bug = pro_do_it(Pro_num_post=pro_num).select_all_bug()[0]
                pro_do_it(Pro_state=u'已结项', Pro_num_post=pro_num,Pro_Over_Time=Time_end,Pro_ps=Pass_state).end_pro()
                return HttpResponseRedirect("/project/" + pro_num + "/")
        return HttpResponse("错误的post数据")

'''详情页内容修改'''
@csrf_protect
def context(request,pro_num):
    sort_name = request.POST.get("sort_name")
    print sort_name
    pre = request.POST.get("textarea")
    if sort_name == 'people_line':
        pro_do_it(Pro_num_post=pro_num,Pro_lines=pre).Updata_Pepole_lines()
    elif sort_name == 'people_zs_main':
        '''项目负责人'''
        pro_do_it(Pro_num_post=pro_num, Pro_People_pr=pre).Updata_Pepole_main()
    elif sort_name == 'people_zs':
        pro_do_it(Pro_num_post=pro_num, Pro_zs=pre).Updata_Pepole_zs()
    elif sort_name == 'PNB':
        pro_do_it(Pro_num_post=pro_num, Pro_nedre_bug=pre).Updata_PNB()
    elif sort_name == 'PLB':
        pro_do_it(Pro_num_post=pro_num, Pro_leave_bug=pre).Updata_PLB()
    elif sort_name == 'PFB':
        pro_do_it(Pro_num_post=pro_num, Pro_nedfol_bug=pre).Updata_PFB()
    elif sort_name == 'PZE':
        pro_do_it(Pro_num_post=pro_num, Pro_zs_end=pre).Updata_ZE()
    elif sort_name == 'PSE':
        pro_do_it(Pro_num_post=pro_num, Pro_safe_end=pre).Updata_SE()
    return HttpResponseRedirect("/project/" + pro_num + "/")

'''缺陷柱状图上传'''
@csrf_protect
def bug_up(request,pro_num):
    print "i am bug_up"
    if request.method == "POST":
        file = request.FILES.get('file_bug')
        if not file:
            return HttpResponseRedirect("/project/" + pro_num + "/")
        eb = excel_bug()
        title = 'tmp'
        excel_path = upload_file(file,title)
        list_re = eb.serious_level(excel_path)
        DI = Tool_arrw().bug_DI_cacl(list_re)
        pro_do_it(Pro_num_post=pro_num,Pro_DI=DI).Update_DI()
        pro_do_it(Pro_Fatal_open=list_re["Open_Bug"][0],Pro_Fatal_close=list_re["Close_Bug"][0],
                  Pro_Serious_open=list_re["Open_Bug"][1],Pro_Serious_close=list_re["Close_Bug"][1],
                  Pro_Common_open=list_re["Open_Bug"][2],Pro_Common_close=list_re["Close_Bug"][2],
                  Pro_Lower_open=list_re["Open_Bug"][3],Pro_Lower_close=list_re["Close_Bug"][3],
                  Pro_Suggest_open=list_re["Open_Bug"][4],Pro_Suggest_close=list_re["Close_Bug"][4],
                  Pro_num_post=pro_num).update_bug_value()
        if os.path.exists(excel_path):
            os.remove(excel_path)
            print "remove %s" % excel_path
        return HttpResponseRedirect("/project/" + pro_num + "/")

'''缺陷饼图文件上传+写入数据库'''
@csrf_protect
def bug_up_pie(request,pro_num):
    print "i am bug_up_pie"
    if request.method == "POST":
        file = request.FILES.get('file_bug_pic')
        if not file:
            return HttpResponseRedirect("/project/" + pro_num + "/")
        eb = excel_bug()
        title = 'tmp'
        try:
            excel_path = upload_file(file,title)
            list_re = eb.Pro_Cake_list(excel_path)
            SortId = pro_do_it(Pro_num_post=pro_num).Select_Id_For_All_bug_sort()
            SortIds = Tool_arrw().list_spilt(SortId)[0]
            bugs_do_it().All_bug_updata(bug_sort1=list_re[u'硬件'],bug_sort2=list_re[u'客户端'],bug_sort3=list_re[u'业务功能'],
                                      bug_sort4=list_re[u'安全性'],bug_sort5=list_re[u'易用性'],bug_sort6=list_re[u'互联互通'],
                                      bug_sort7=list_re[u'其他产品问题'],ID=SortIds)
            # u"硬件", u"客户端", u"业务功能", u"安全性", u"易用性",u"互联互通",u"其他产品问题"
            return HttpResponseRedirect("/project/" + pro_num + "/")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info();
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print (Exception,e,exc_tb.tb_lineno,fname)
            return HttpResponse(u"请检查文件中是否有缺陷类型列！")

'''下载项目列表'''
@csrf_protect
def download_list(request,list):
    if request.method == "POST":
        lists = list.split('|')
        lists_s = sorted([int(x) for x in lists],reverse=True)
        print lists_s
        list_pro = []
        for i in lists_s:
            Pro_data = pro_do_it(Pro_num_post=i).select_detail_info()
            dict_list = manage_info().Download_Data_Change(Pro_data[0])
            list_pro.append(dict_list)
        excel_write().write_all_data(list_pro)
        return HttpResponseRedirect("/download/tmp/download_Pro_data.xls")