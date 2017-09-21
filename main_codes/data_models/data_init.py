# coding=utf-8

def init_databse(self, columns, data):
    '''
    对应数据库模型类的初始化，值为每个行表中的所有值
    :param self:
    :param columns:
    :param data:
    :return:
    '''
    # 存储一下处理后的值
    values = []
    for index in range(len(columns)):
        # 将缺省值做null处理
        if str(data[index]).strip(' '):
            value = data[index]
        else:
            value = ''
        setattr(self, columns[index], value)
        values.append(value)

    '''
    # debug: 找到未能完整导入的数据表
    keyword = '引进英国BEAMECH公司液体二氧化碳发泡工艺技术'

    if keyword in data:
        data_str = ''

        for e in data:
            data_str += str(e) + ','
        print data_str

        for index in range(len(values)):
            print columns[index], '--', values[index]
    '''



