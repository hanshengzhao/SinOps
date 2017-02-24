#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz

# about how to use pymongo http://api.mongodb.com/python/current/tutorial.html
from pymongo import MongoClient
from pymongo import ReturnDocument
import uuid
from bson.objectid import ObjectId

client = MongoClient('192.168.104.137', 27017)
db = client['Ops']


# print db.collection_names()
# collection = db['vm_instance']
#
# data = {'age':18}
# collection.insert_one(data)





# 创建资产表信息，里面包括 表名称  表字段
def create_or_update_Assest(name, display_name, field_list):
    # 定义关系
    collection = db['Assest']
    data = {
        'name': name,
        'display_name': display_name,
        'field_list': field_list,
    }
    collection.find_one_and_update({'name': name}, {'$set': data}, upsert=True, return_document=ReturnDocument.AFTER)


# 删除一个资产表
def delete_Assest(table_id):
    collection = db['Assest']
    table = collection.find_one({'_id': ObjectId(table_id)})
    table_name = table['name']
    ret = collection.delete_one({'_id': ObjectId(table_id)})
    table_collection = db[table_name]
    table_collection.drop()
    return ret


# 更新一条field
def update_one_field(field_id, field_dic, table_name, field_old):
    collection = db['Assest']
    data = field_dic
    if field_id == "":
        # 新增
        data['field_id'] = uuid.uuid4()
        collection.update({'name': table_name}, {'$push': {"field_list": data}})
    else:
        # 更新一条,更新前获取 新旧字段
        ret = collection.update({'field_list.field_id': field_id}, {'$set': {"field_list.$": data}})
        table_collection = db[table_name]
        update_dic = {}
        for k in data:
            if k == 'field_id': break
            if data[k] != field_old[k]:
                update_dic[field_old[k]] = data[k]
        print update_dic
        if update_dic != {}:
            new_ret = table_collection.update({}, {"$rename": update_dic}, upsert=False, multi=True)
            print new_ret
        return ret['updatedExisting']
        # 更新一个之后要去修改其他字段


table_collection = db['person']


# print {old_name:name,old_display_name:display_name,old_show:show}

# 更新一条数据表信息
def update_one_data(data_id, field_dic, table_name):
    collection = db[table_name]
    ret = collection.update({'_id': ObjectId(data_id)}, {"$set": field_dic})
    return ret['updatedExisting']


# 删除一条数据表信息
def delete_one_data(data_id, table_name):
    collection = db[table_name]
    ret = collection.delete_one({'_id': ObjectId(data_id)})
    return 'true'


# 插入一条数据表信息
def insert_one_data(field_dic, table_name):
    collection = db[table_name]
    ret = collection.insert_one(field_dic)
    return ret


# update_one_field('5f421664-d4a6-4a31-81a6-b72d3623d563', { "field_id" : "5f421664-d4a6-4a31-81a6-b72d3623d563", "field_show" : True, "field_name" : "network_name", "field_display" : "网络名称" })




# 获取所有资产表信息
def get_all_Assest_info():
    collection = db['Assest']
    all_assest = collection.find()
    return all_assest


def get_Assest_info(table_name):
    collection = db["Assest"]
    assest = collection.find_one({'name': table_name})
    return assest


def get_table_info(table_name, field_name_list):
    collection = db[table_name]
    infos = collection.find(projection=field_name_list)
    return infos


# for i in get_table_info('host'):
#     print i

# print get_Assest_info('network')
# 插入一条数据
def insert_data(collection_name, data):
    collection = db[collection_name]
    collection.insert_one(data)

# # 定义数据
# field_list = [
#     {
#         'field_name': 'name',
#         'field_display': '网络名称',
#     },
#     {
#         'field_name': 'gateway',
#         'field_display': '网关',
#     },
#     {
#         'field_name': 'net',
#         'field_display': '网段',
#     }
# ]
#
# create_or_update_Assest('network1','网络1',field_list)

# create_or_update_Assest('instance','name','id','ip','passwd','image_id')
# create_or_update_Assest('network','name','id','net')
