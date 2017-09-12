# coding=utf-8
from main_codes import db
from data_init import init_databse
# from main_codes.extensions import db
import os


modles_code_path = 'data/all_models'
if not os.path.exists(modles_code_path):
    os.mkdir(modles_code_path)

for file in os.listdir(modles_code_path):
    code = open(os.path.join(modles_code_path, file), 'r').read()
    try:
        exec(code)
    except Exception,e:
        print 'filename-----------', file
        print e

# 创建对应文件夹下面所有的表
db.create_all()