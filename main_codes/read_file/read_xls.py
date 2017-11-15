# coding=utf-8
import xlrd
import os
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')


def give_sheet(path, xls_name, c_path, c_xls, excle_name, step, page_table, sheets_dict, model_mappings):
    data = xlrd.open_workbook(os.path.join(path, xls_name))


    # 读取所有的sheet表，给定对应的columns映射关系
    all_columns = get_columns(c_path, c_xls, excle_name, step, page_table, sheets_dict, model_mappings)

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


def get_columns(path, xls_name, excle_name, step, page_table, sheets_dict, model_mappings):
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

    # 记录每个excel文件中的所有sheets,存储对应的dict中
    sheets_dict.write(excle_name + ' = {')

    # 存储excles文件中每个sheet对应的columns,获取sheet名，栏目名。
    sheets = {}

    for index in range(1, nrows, step):

        org_colums = []
        ref_colums = []

        names = table.row_values(index)[0].split('.')
        sheet_name = names[1]
        table_name = excle_name + '_' + re.findall(r'\d+', names[0])[0]
        print sheet_name ,'(' ,table_name , ')'

        # 所有sheet的中英文名对照表存储在sums文件夹中
        page_table.write(sheet_name+ ',' + table_name + '\n')

        # 分别存储所有columns的中英文名，表头属性同步到数据库中时，要注意词前后的空格
        for column in table.row_values(index + 1):
            if column:
                org_colums.append(column.strip())

        for column in table.row_values(index + 2):
            if column:
                ref_colums.append(column.strip())

        sheets_dict.write("'"+ sheet_name + "':" + "'" + table_name + "', ")


        # 生成对应的模型的sqlachemy代码（每个对应一个TXT文件），存储在all_modles文件夹中
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
        model_template += "\n\tdef __repr__(self):\n" + "\t\treturn 'info:{}'.format(self.id)\n"
        model_template += "\n\tdef __init__(self, columns, data):\n" + "\t\tinit_databse(self, columns, data)\n"

        path = 'data/all_models'
        if not os.path.exists(path):
            os.mkdir(path)
        model_code = open(os.path.join(path, table_name + '.txt'), 'w')
        model_code.write(model_template)

        # 生成对应elasticsearch的索引文件代码， 存储在sums文件夹中
        model_mapping = '\t\t"'+ table_name + '": {\n\t\t\t"properties": {\n'
        for index in range(len(ref_colums)):
            try:
                val = ref_colums[index].strip()
            except Exception,e:
                print e
            model_mapping += '\t\t\t\t"'+ val + '":\t{ "type": "text" },\n'
        model_mapping += '\t\t\t}\n\t\t},\n'

        model_mappings.write(model_mapping)

        # sheets保存：sheet中文名：[中文表头， 英文表头， 数据库表名]
        sheets.update({sheet_name: [org_colums, ref_colums, table_name]})

    sheets_dict.write('}\n')

    return sheets


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


