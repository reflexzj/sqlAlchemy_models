# coding=utf-8
import os

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