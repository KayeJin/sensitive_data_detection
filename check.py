# -*- coding:utf-8 -*-

"""
@Author     :   Browser
@file       :   identity_mysql.py 
@time       :   2019/09/30
@software   :   PyCharm 
@description:   " "
"""
import pymysql
import re, sys
from pyhanlp import *

# http://www.360doc.com/content/21/0220/19/13664199_963059614.shtml
moblie_phone_pattern = re.compile(r'1[356789]\d{9}')
phone_pattern = re.compile(r'\d{3}-\d{8}|\d{4}-\d{7}')
id_pattern = re.compile(r'[1-9]\d{5}(?:18|19|(?:[23]\d))\d{2}(?:(?:0[1-9])|(?:10|11|12))(?:(?:[0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]')
email_pattern = re.compile(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)')
bank_card_pattern = re.compile(r'([1-9]{1}\d{15}|\d{18})')

CRFnewSegment = HanLP.newSegment("crf")  # 通过crf算法识别实体

def check_secret(pattern, value):
    return pattern.findall(value)

def check_chinese_address_and_name(value):
    seg_text = CRFnewSegment.seg(value)
    Address = r'(ns|nsf)'
    
    Person_Name = r'nr'
    
    dict = {}
    
    address_list = []
    name_list = []
    
    for i in seg_text:
        dict[str(i.word)] = [str(i.nature)]
    
    for key, value in dict.items():
        value = str(value)
        if re.search(Address, value):
            address_list.append(key)
        if re.search(Person_Name, value):
            name_list.append(key)
    return address_list, name_list


class DB(object):
    def __init__(self,ip,username,password):
        self.ip = ip
        self.username = username
        self.password = password
        self.db = pymysql.connect(self.ip,self.username,self.password)
        self.cursor = self.db.cursor()

    #  通过schemata获取所有数据库名称
    def get_database(self):
        self.cursor.execute("SELECT schema_name from information_schema.schemata ")
        database_list = self.cursor.fetchall()
        result = []
        for line in database_list:
            if line[0] not in ['information_schema','mysql','performance_schema','sys','loonflownew']:   #排除默认的数据库
                result.append(line[0])
        return result

    #  获取表名
    def get_table(self,database):
        self.cursor.execute("select table_name from information_schema.tables where table_schema= '%s' " % database)
        table_list = self.cursor.fetchall()
        result = []
        for line in table_list:
            result.append(line[0])
        return result

    #  获取字段名
    def get_column(self,database,table):
        self.cursor.execute("select column_name from information_schema.columns where table_schema='%s' and table_name='%s'" % (database,table))
        column_list = self.cursor.fetchall()
        result = []
        for line in column_list:
            result.append(line[0])
        return result

    #  获取字段内容
    def get_content(self,database,table,column):
        self.cursor.execute("select %s from %s.%s LIMIT 0,1" %(column,database,table))
        content = self.cursor.fetchall()
        if content:
            return content[0][0]

    def __del__(self):
        self.db.close()

if __name__ == '__main__':
        # # db = DB('192.168.189.154','root','Gepoint')
        # db = DB('rm-bp1i3518ykiqi60my8o.mysql.rds.aliyuncs.com','root','Epoint@123@)!(')
        # databases = db.get_database()  #  通过schemata获取所有数据库名称
        # for database in databases:
        #     tables = db.get_table(database) #  获取表名
        #     for table in tables:
        #         columns = db.get_column(database,table) #  获取字段名
        #         for column in columns:
        #             data = db.get_content(database,table,column) #  获取字段内容
        #             data_str = str(data)
        #             # 数据库名 表名  字段名  字段内容  “中风险”/“无风险”
        #             result = [database,table,column,data_str,check_secret(data_str)]
        #             result_str = str(result) + "\r\n"
        #             with open('message.txt','a+',encoding='UTF-8') as file:
        #                 file.write(result_str)

        # 正则表达式
        bc = check_secret(bank_card_pattern, '我的手机号是18590085340,身份证是110101199003072957,银行卡是6225806592337329,我的邮箱是aka@gmail.com')
        print('银行卡',bc)
        bc = check_secret(moblie_phone_pattern, '我的手机号是18590085340,身份证是110101199003072957,银行卡是6225806592337329,我的邮箱是aka@gmail.com')
        print('手机',bc)
        bc = check_secret(id_pattern, '我的手机号是18590085340,身份证是110101199003072957,银行卡是6225806592337329,我的邮箱是aka@gmail.com')
        print('身份证',bc)
        bc = check_secret(email_pattern, '我的手机号是18590085340,身份证是110101199003072957,银行卡是6225806592337329,我的邮箱是aka@gmail.com')
        print('邮箱',bc)

        # Hanlp 自然语言处理
        address_list,name_list = check_chinese_address_and_name('我家在北京市东城区东长安街, 我叫金翠花')
        print('地址', address_list)
        print('名字', name_list)