# coding=utf-8
from collections import OrderedDict

from pyexcel_xls import get_data
from pyexcel_xls import save_data
import os

# 这个方法返回的是一个按逐行存取的二位数组，相当于xlrd方法的升级版（基于xlrd包）
def read_xls_file(filename):
    xls_data = get_data(filename)
    print "Get data type:", type(xls_data)
    for sheet_n in xls_data.keys():
        print sheet_n, ":", xls_data[sheet_n]


if __name__ == '__main__':
    xls_name = unicode('成果科.xlsx', 'utf-8')
    print type(xls_name)
    filename = os.path.join('../../data/source_data/' , xls_name)
    read_xls_file(filename)
