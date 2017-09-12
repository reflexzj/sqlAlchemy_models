# coding=utf-8
import xlrd
import os
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')


def give_sheet(path, xls_name, c_path, c_xls, excle_name, step):
    data = xlrd.open_workbook(os.path.join(path, xls_name))


    # 读取所有的sheet表，给定对应的columns映射关系
    all_columns = get_columns(c_path, c_xls, excle_name, step)

    # 读取所有sheets中的内容
    all_datas = {}
    sheet_names = []

    for index in range(len(data.sheets())):
        table = data.sheets()[index]
        sheet_name = table.name
        sheet_names.append(sheet_name)
        nrows = table.nrows

        datas = read_sheet(table, 1, nrows)
        all_datas.update({sheet_name:datas})

    return  all_datas, all_columns, sheet_names

def read_sheet(table, begin, end):
    '''
    根据指定的序号，读取excle中的数据，行列存放到二维数组中
    :param table:
    :param begin:
    :param end:
    :param columns: 表格对应的栏目（属性）
    :return:
    '''

    all_datas = []

    for i in range(begin, end):
        data = table.row_values(i)

        row_data = []
        for cell in data:
            content = cell
            row_data.append(content)

        all_datas.append(row_data)

    return all_datas

def get_columns(path, xls_name, excle_name, step):
    '''
    将每个sheet名字，表格中的栏目以及对应的映射英文名从excle文件中获取到
    :param path:
    :param xls_name:
    :param step:
    :return:
    '''
    data = xlrd.open_workbook(os.path.join(path, xls_name))
    table = data.sheets()[0]
    nrows = table.nrows

    # 存储每个sheet对应的columns,
    # 获取sheet名，栏目名以及两者对应的数据库表中的英文映射名
    sheets = {}

    for index in range(1, nrows, step):

        org_colums = []
        ref_colums = []

        names = table.row_values(index)[0].split('.')
        sheet_name = names[1]
        table_name = excle_name + '_' + re.findall(r'\d+', names[0])[0]
        print sheet_name ,'(' ,table_name , ')'
        page_path = 'data/sums'
        fp = open(os.path.join(page_path, 'page_table.txt'), 'a')
        fp.write(sheet_name+ ',' + table_name + '\n')

        # 表头属性同步到数据库中时，要注意词前后的空格
        for column in table.row_values(index + 1):
            if column:
                org_colums.append(column.strip())

        for column in table.row_values(index + 2):
            if column:
                ref_colums.append(column.strip())

        # 生成对应的模型代码
        model_template = 'class '+table_name+'(db.Model):\n\n'
        for index in range(len(ref_colums)):
            try:
                val = ref_colums[index].strip()
            except Exception,e:
                print 'models code error: ', table_name
                print e

            if index == 0:
                model_template += '\t'+ val + '= db.Column(db.INTEGER, primary_key=True)\n'
            else:
                model_template += '\t'+ val + '= db.Column(db.TEXT)\n'

        model_template += "\n\tdef __repr__(self):\n" \
                          "\t\treturn 'info:{}'.format(self.id)\n" \
                          "\n\tdef __init__(self, columns, data):\n" \
                          "\t\tinit_databse(self, columns, data)\n"

        path = 'data/all_models'
        if not os.path.exists(path):
            os.mkdir(path)
        model_code = open(os.path.join(path, table_name+'.txt'), 'w')
        model_code.write(model_template)

        sheets.update({sheet_name: [org_colums, ref_colums, table_name]})

    return sheets






