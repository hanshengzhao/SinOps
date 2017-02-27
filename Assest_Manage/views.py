#! coding:utf-8
from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
# Create your views here.
from API import mongo_ops
from API import  utils
import uuid


# 获取所有资产表
def get_left_nav():
    table_list = mongo_ops.get_all_Assest_info()
    return table_list




def index(req):
    if req.method == "GET":
        page_title, page_subtitle, active_nav_li = '首页', '基本信息', 'index'
        table_list = get_left_nav()
        return render(req,'base.html',locals())

def create(req):
    if req.method == "GET":
        page_title, page_subtitle, active_nav_li,active_nav_sub_li = '资产表管理', '创建新资产表', 'assest','assest_create'
        table_list = get_left_nav()
        return render(req, 'Assest_Create.html', locals())
    else:
        table_name =  req.POST.get('table_name')
        table_display_name = req.POST.get('table_display_name')
        if table_display_name=="":table_display_name=table_name
        field_name_list = req.POST.getlist('field_name')
        field_display_name = req.POST.getlist('field_display_name')
        field_list = []
        if len(field_name_list)>0:
            for index,field_name in enumerate(field_name_list):
                field_dic = {
                    'field_name':field_name.strip(),
                    'field_display':field_display_name[index],
                    'field_show':True,
                    'field_id': str(uuid.uuid4())
                }
                field_list.append(field_dic)
        mongo_ops.create_or_update_Assest(table_name,table_display_name,field_list)
        return  HttpResponse('True')


# 列出所有的资产表
def assest_manage(req):
    if req.method == "GET":
        active_nav_li = 'assest'
        active_nav_sub_li = 'assest_manage'
        table_list = get_left_nav()
        if '?' in req.get_full_path():
            encode64_url = req.get_full_path().split('?')[1]
            args_str = utils.base64_url_decode(encode64_url)
            args_dic = utils.parser_url(args_str)
            page_title = '资产表修改'
            if args_dic.has_key('id') and args_dic.has_key('name') and args_dic.has_key('display_name'):
                table_name = args_dic['name'][0]
                table_id = args_dic['id'][0]
                table_display_name = args_dic['display_name'][0]
                page_subtitle = table_name
                type = 'assest'
                assest_info = mongo_ops.get_Assest_info(table_name)
            else:
                all_assest = mongo_ops.get_all_Assest_info()
                assest_list = []
                type = 'all_assest'
                for assest in all_assest:
                    assest_list.append(assest)
            return render(req, 'Assest_Manage.html', locals())
        else:
            page_title = '资产表管理'
            page_subtitle = '所有资产表'
            all_assest = mongo_ops.get_all_Assest_info()
            assest_list = []
            type = 'all_assest'
            for assest in all_assest:
                assest_list.append(assest)
            return render(req, 'Assest_Manage.html', locals())
    else:
        # post
        if "?" in req.get_full_path():
            encode64_url = req.get_full_path().split('?')[1]
            args_str = utils.base64_url_decode(encode64_url)
            args_dic = utils.parser_url(args_str)
            # 判断链接里是否有 id name display_name
            if args_dic.has_key('id')  and args_dic.has_key('name') and args_dic.has_key('display_name'):
                # 如果有并且action 有edit，那么就是要修改字段
                table_name = args_dic['name'][0]
                table_id = args_dic['id'][0]
                table_display_name = args_dic['display_name'][0]
                # if args_dic['action'][0]=='edit':
                if req.POST.get('action')=='save_field':
                    # 要修改字段
                    field_id = req.POST.get('field_id')
                    field_info = req.POST.get('field_info')
                    field_old = req.POST.get('field_old')
                    import json

                    field_info =  json.loads(field_info)
                    field_old = json.loads(field_old)
                    ret = mongo_ops.update_one_field(field_id,field_info,table_name,field_old)
                    if field_old == {}:# 如果是新增，那么就返回ID值。
                        return HttpResponse(ret)
                    return HttpResponse("true")
                elif req.POST.get('action') == "delete_field":
                    field_id = req.POST.get('field_id')
                    mongo_ops.delete_one_field(table_id,field_id)
                    return HttpResponse('true')


            else:
                if args_dic['action'][0] == 'delete':
                    table_id = args_dic['id'][0]
                    ret =  mongo_ops.delete_Assest(table_id)
                    return HttpResponse('true')
                else:
                    return HttpResponse('error')
        else:
            if req.POST.get('action') == "change_table":
                table_display_name = req.POST.get('table_display_name')
                table_id = req.POST.get('table_id')
                mongo_ops.rename_Assest(table_id,table_display_name)
                return HttpResponse('true')

def table(req,table_name):
    if req.method == "GET":
        page_title, page_subtitle, active_nav_li, active_nav_sub_li =u'%s表管理'%table_name, '详细信息', 'table', u'table_%s'%table_name
        table_list = get_left_nav()
        table_info = mongo_ops.get_Assest_info(table_name)
        table_field = table_info['field_list']
        field_name_list = []
        for index,field in enumerate(table_field):
            if field.has_key('field_name'):
                field_name_list.append(field['field_name'])
            else:
                # 删除没有field_name 的字段
                del  table_field[index]
        data = mongo_ops.get_table_info(table_name,field_name_list)

        return render(req,'Table_Info.html',locals())
    else:
        import json
        info =  json.loads(req.body)
        table_name =  info['table_name']
        action = info['action']
        if action == "edit":
            data_id = info['data_id']
            field_info = info['field_info']
            ret = mongo_ops.update_one_data(data_id,field_info,table_name)
        elif action == "delete":
            data_id = info['data_id']
            ret = mongo_ops.delete_one_data(data_id,table_name)
        elif action == "add":
            field_info = info['field_info']
            ret = mongo_ops.insert_one_data(field_info,table_name)
        else:
            ret = 'false'
        return HttpResponse(ret)

