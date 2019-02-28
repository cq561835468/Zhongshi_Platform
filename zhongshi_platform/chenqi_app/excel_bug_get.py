#coding=utf-8
import xlrd
import xlsxwriter
from datetime import datetime
import os
import copy


class excel_bug():
    def __init__(self):
        pass

    #调试用路径转换
    def del_app_path(self,path):
        path_t = path[path.index('\\') + 1:]
        return path_t

    '''bug中为0不返回，返回不以为0的'''
    def Pro_Zero_list(self,lists):
        list_return = copy.deepcopy(lists)
        for sa in list_return:del sa[:]
        Need_del = [i for i in range(len(lists[1])) if lists[1][i] != 0]
        for i in Need_del:
            for index,value in enumerate(lists):
                list_return[index].append(value[i])
        return list_return

    '''处理BUG类型,饼图用'''
    def Pro_Cake_list(self,path):
        seriout_num = [[u"硬件", u"客户端", u"业务功能", u"安全性", u"易用性",u"互联互通",u"其他产品问题"],
                       [0,0,0,0,0,0,0]]

        data = xlrd.open_workbook(path)
        table = data.sheets()[0]
        # 获取第一行识别需要的列
        row = table.row_values(0)
        # 总行数
        nrows = table.nrows
        # 类型列
        Index_Sort = row.index(u'缺陷类型')
        arrw_r = table.col_values(Index_Sort)[1:]
        arrw_r_s = set(arrw_r)
        for item in arrw_r_s:
            seriout_num[1][seriout_num[0].index(item)] = arrw_r.count(item)
        data.release_resources()
        del data
        return dict(zip(seriout_num[0],seriout_num[1]))

    '''返回缺陷是否关闭、严重等级,柱状图用'''
    def serious_level(self, path):
        # 致命，严重，普通，较低，建议
        Bug_Opcl_list = (u"关闭",)
        re_list = {}
        #总值 关闭 未关闭
        seriout_num = [[u"1-致命", u"2-严重", u"3-普通", u"4-较低", u"5-建议"],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]]
        data = xlrd.open_workbook(path)
        table = data.sheets()[0]
        # 获取第一行识别需要的列
        row = table.row_values(0)
        # 总行数
        nrows = table.nrows
        # 状态和缺陷所在列
        Index_Se = row.index(u'缺陷描述.严重性')
        Index_St =  row.index(u'状态')
        for i in range(1,nrows):
            row_value = table.row_values(i)
            if row_value[Index_Se] in seriout_num[0]:
                Bu_list_index = seriout_num[0].index(row_value[Index_Se])   #计算严重性所在列
                if row_value[Index_St] in Bug_Opcl_list: #如果在Bug_Opcl_list中则[1]+1否则[2]+1
                    seriout_num[2][Bu_list_index] += 1  # 在对应的数组中+1
                else:
                    seriout_num[3][Bu_list_index] += 1  # 在对应的数组中+1
                seriout_num[1][Bu_list_index] +=1   #在对应的数组中+1
        re_list["Close_Bug"] = seriout_num[2]
        re_list["Open_Bug"] = seriout_num[3]
        data.release_resources()
        del data
        return re_list

class excel_write():
    def __init__(self):
        pass

    '''时间位提前分列'''
    def fom_change(self,list_all):
        list_r = []
        list_r.append(list_all['Pro_numbers'])
        list_r.append(list_all['Pro_state'])
        list_r.append(list_all['Pro_name'])
        list_r.append(list_all['Pro_Sort'])
        list_r.append(list_all['Pro_lines_name'])
        list_r.append(list_all['Pro_ps'])
        list_r.append(list_all['Pro_DI'])
        list_all['Pro_Update_Time'] = 0 if list_all['Pro_Update_Time'] == '--'else list_all['Pro_Update_Time']
        list_r.append(list_all['Pro_Update_Time'])
        list_all['Pro_Over_Time'] = 0 if list_all['Pro_Over_Time'] == '--' else list_all['Pro_Over_Time']
        list_r.append(list_all['Pro_Over_Time'])
        list_r.append(list_all['timeall'])
        list_r.append(list_all['Pro_Fatal_Bug'])
        list_r.append(list_all['Pro_Serious_Bug'])
        list_r.append(list_all['Pro_Common_Bug'])
        list_r.append(list_all['Pro_Lower_Bug'])
        list_r.append(list_all['Pro_Suggest_Bug'])
        list_r.append(list_all['Pro_All_Bug'])
        list_r.append(list_all['vernum'])
        list_r.append(list_all['Pro_People_pr'])
        list_r.append(list_all['Pro_zs'])
        list_r.append(list_all['Pro_lines'])
        list_r.append(list_all['Pro_nedre_bug'])
        list_r.append(list_all['Pro_leave_bug'])
        list_r.append(list_all['Pro_nedfol_bug'])
        list_r.append(list_all['Pro_zs_end'])
        list_r.append(list_all['Pro_safe_end'])
        return list_r

    '''写入下载文件中'''
    def write_all_data(self,arrw):
        arrw_fom_change = arrw
        '''根据字典完成列表'''
        for index,value in enumerate(arrw_fom_change):
            sa = self.fom_change(value)
            arrw_fom_change[index] = sa
        '''写入excel中'''
        path = r"chenqi_app\static\share\tmp\download_Pro_data.xls"
        if os.path.exists(path):
            os.remove(path)
        f = open(path, 'w')
        f.close()
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet()
        #格式
        bold = workbook.add_format({'bold': 1})
        #表头

        headings = [u'项目编号',u'项目状态',u'项目名称',u'项目分类',u'产品线',u'发布建议',u'项目DI值',u'项目创建时间',u'项目结项时间',
                    u'工时总计',u'致命',u'严重',u'普通',u'较低',u'建议',u'全部',u'版本数',u'负责人',u'中试参与人员',u'产线人员',
                    u'未解决的主要问题',u'遗留的主要问题',u'需要产线跟踪的问题',u'测试结论',u'安全结论']
        #headings_time = [u'测试活动',u'版本号',u'开始日期',u'结束日期',u'实际耗时',u'项目编号']

        worksheet.write_row('A1', headings, bold)
        col_num = 2
        for value in arrw_fom_change:
            worksheet.write_row('A'+ str(col_num), value)
            col_num += 1


if __name__ =="__main__":
    eb = excel_bug()
    #path = eb.del_app_path(r"chenqi_app\static\share\tmp\test.xls")
    path = 'static\\share\\tmp\\4.16.xls'
    print '123123'