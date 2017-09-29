# coding=utf-8
from main_codes import app
from main_codes.data_models.create_databases import *
from main_codes.data_models.show_columns import *

# 6大科室
reflect_table = {'专利科':'patent', '农社科':'farm_socity', '合作交流科':'cop_ex',
                 '法规科':'law', '成果科':'result', '高新科':'high_new_tec', '总结':'sums'}


# reflect_table = {'总结':'sums'}

# 定义路径和起始参数
source_data_path = 'data/source_data/'
columns_data_path = 'data/columns/'
sums_data_path = 'data/sums/'


# 生成所有excle表中的文件
create_all_tables(reflect_table, source_data_path, columns_data_path, sums_data_path)

# 获取所有的数据库映射表关系
colums_table = show_columns(sums_data_path, file = 'all_tables.txt')

# 基本增、删、改、查工作测试

table_name = 'law_1'
colums = colums_table[table_name][1].strip().split(',')

# （1）query
query_table(table_name, '显示器', colums)

# （2）update
# newdata = ['1', '2007', '', '省人才', '', '', '', '', '', '高裕弟', '党员', '有机发光显示器产业化',
#           '昆山维信诺科技有限公司', '高新区', '创新', '100', '100', '100', '13801304086', '刘益\n宋琼琦',
#           '13621549956\n57269016\n13962656013', 'songqq@visionox.com', '']
#
# update_data(table_name, 1, newdata, colums)

# （3）delete
# delet_data(table_name, 1)

# app.run(debug=True)