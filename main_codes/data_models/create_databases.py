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


def create_tables(path, xls_name, c_path, c_xls, excle_name, step):
    '''
    创建一个excle文件中的所有的表，并把对应excel表中数据存入数据库中
    :param path:
    :param xls_name:
    :param c_path:
    :param c_xls:
    :param step:
    :return:
    '''


    all_datas, all_columns, sheet_names = give_sheet(path, xls_name, c_path, c_xls, excle_name, step)

    # 将所有sheet中数据存入对应数据库表中去
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

        # 将每个sheet的栏目信息存储起来，便于后期的引用
        sums_path = 'data/sums/'
        all = open(os.path.join(c_path, 'all_tables.txt'), 'a')
        try:
            all.write(table_name.replace('\n','') +'\n')
            all.write(','.join(org_columns).replace('\n','')+'\n')
            all.write(','.join(ref_columns).replace('\n','')+'\n')

        except Exception,e:
            print 'save tables errot: ', sheet_name
            print e

def create_all_tables(reflect_table, source_data_path, columns_data_path):
    '''
    读取所有的excle表格,生成对应的数据库表格，所有表导入完成后可以不再调用
    :param reflect_table:
    :return:
    '''
    # 表头映射表的步长（3行代表一张sheet）
    step = 3

    for key in reflect_table.keys():
        print '->' + key
        print 'start creating tables:'

        xls_name = unicode(key+'.xls', 'utf-8')
        if not os.path.exists(os.path.join(source_data_path, xls_name)):
            xls_name = unicode(key + '.xlsx', 'utf-8')
        c_xls = unicode(key+'.xlsx', 'utf-8')

        excle_name = reflect_table[key]

        create_tables(source_data_path, xls_name, columns_data_path, c_xls, excle_name, step)

        print 'finished.'


def show_columns(path, file):
    '''
    读取存储好的文件中所有栏目表
    :param path:
    :param file:
    :return: columsn_table字典，返回原始栏目名和对应的数据库中映射表名
    '''
    data = open(os.path.join(path, file), 'r').readlines()
    columns_table = {}
    for index in range(0, len(data), 3):
        try:
            table_name = data[index].strip('\n')
            org_columns = data[index+1].strip('\n')
            ref_columns = data[index+2].strip('\n')
            columns_table.update({table_name:[org_columns, ref_columns]})
        except Exception,e:
            # all_tables文件中的没有成功读取相应的table的信息
            print 'show_columns missing:', table_name
            print e

    return  columns_table

