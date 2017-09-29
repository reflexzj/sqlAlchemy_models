# coding=utf-8
from main_codes.read_file.read_xls import give_sheet
from models import *
from main_codes import db
from sqlalchemy import or_
import os

def insert(table_name, xls_data, columns):
    '''
    全表格查找，匹配表格中的所有栏目
    :param table_name:
    :param xls_data:
    :param columns:
    :return:
    '''
    for data in xls_data:
        content = None

        try:
            exec('content ='+ table_name + '(columns, data)')
            db.session.add(content)
        except Exception, e:
            # models没有成功初始化
            print 'table model init error: ', table_name, len(columns), len(data)
            print e

        try:
            db.session.commit()
        except Exception, e:
            # print 'ERROR:', e
            db.session.rollback()

def query_table(table_name, keyword, columns):
    '''
    对应表格的全文查询
    :param table_name:
    :param keyword:
    :param columns:
    :return:
    '''
    result = None
    conditions = []

    for column in columns:
        conditions.append(table_name+"."+column+".like('%'+keyword+'%')")
    conditions = ', '.join(conditions)

    exec('result = '+ table_name+'.query.filter(or_(' +conditions+ '))')
    return result

def delet_data(table_name, id):
    '''
    删除对应id行的数据
    :param table_name:
    :param id:
    :return:
    '''
    exec(table_name+ '.query.filter_by(id = id).delete()')
    db.session.commit()

def update_data(tale_name, id, new_data, columns):
    '''
    更新表中的某行数据, 以id（主键）为索引目标
    :param tale_name:
    :param id:
    :param new_data:
    :param columns:
    :return:
    '''
    values = []
    for index in range(len(columns)):
        # 如果new_Data[index]中包含换行符，会报错, 需要保持字符串为raw string（repr, eval）
        value = tale_name+ '.'+columns[index] + ':' + "'" +new_data[index]+ "'"
        values.append(value)
    values = '{' + ', '.join(values) + '}'
    print values

    exec( tale_name+'.query.filter_by(id = id).update(' + values + ')')
    db.session.commit()



def create_tables(path, xls_name, c_path, c_xls, excle_name, step, all_tables, page_table, sheets_dict, model_mappings):
    '''
    创建一个excle文件中的所有的表，并把对应excel表中数据存入数据库中
    :param path:
    :param xls_name:
    :param c_path:
    :param c_xls:
    :param step:
    :return:
    '''


    all_datas, all_columns, sheet_names = give_sheet(path, xls_name, c_path, c_xls, excle_name, step, page_table, sheets_dict, model_mappings)

    # 将所有sheet中数据存入对应数据库表中去
    # 将每个sheet的栏目信息存储起来，便于后期的引用

    for sheet_name in sheet_names:
        try:
            org_columns = all_columns[sheet_name][0]
            ref_columns = all_columns[sheet_name][1]
            table_name = all_columns[sheet_name][2]
        except Exception, e:
            # sheet_name与all_columns中不匹配
            print 'sheet names error: ', sheet_name
            # print ', '.join(sheet_names)
            print e
            continue

        insert(table_name, all_datas[sheet_name], ref_columns)


        try:
            all_tables.write(table_name.replace('\n','') +'\n')
            all_tables.write(','.join(org_columns).replace('\n','')+'\n')
            all_tables.write(','.join(ref_columns).replace('\n','')+'\n')

        except Exception,e:
            print 'save tables errot: ', sheet_name
            print e

def create_all_tables(reflect_table, source_data_path, columns_data_path, sums_data_path):
    '''
    读取所有的excle表格,生成对应的数据库表格，所有表导入完成后可以不再调用
    :param reflect_table:
    :return:
    '''
    # 表头映射表的步长（3行代表一张sheet）
    step = 3

    # sums_data
    all_tables = open(os.path.join(sums_data_path, 'all_tables.txt'), 'w')
    page_table = open(os.path.join(sums_data_path, 'page_table.txt'), 'w')
    model_mappings = open(os.path.join(sums_data_path, 'model_mappings.txt'), 'w')
    sheets_dict = open(os.path.join(sums_data_path, 'sheets_dict.txt'), 'w')

    model_mappings.write('model_mappings = {\n\t"mappings": {\n')

    for key in reflect_table.keys():
        print '->' + key
        print 'start creating tables:'

        xls_name = unicode(key+'.xls', 'utf-8')
        if not os.path.exists(os.path.join(source_data_path, xls_name)):
            xls_name = unicode(key + '.xlsx', 'utf-8')
        c_xls = unicode(key+'.xlsx', 'utf-8')

        excle_name = reflect_table[key]



        create_tables(source_data_path, xls_name, columns_data_path, c_xls, excle_name, step, all_tables, page_table, sheets_dict, model_mappings)

        print 'finished.'

    model_mappings.write('\t}\n}')



