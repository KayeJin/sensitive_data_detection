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
import threading
from multiprocessing import Process, Pool #进程
from threading import Thread #线程
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pyhanlp import *
from math import ceil
import time 
import match
import yyyy
import db_class

#取整个数据库 def（）
def sensitive_word_recognize( database, table, columns, data, index, size): #data 数据，index 数据分片索引， size 进程数
    data_len = len(data)
    size = ceil(data_len/size)
    start = index * size
    end = (index + 1) * size if (index + 1) * size < data_len else data_len 
    tmp_data = data[start : end]
    result_str = ''
    for j in tmp_data: #行分组块
        k = 0
        for i in j :
            # 字段内容  “中风险”/“无风险”
            # result = [database, table,columns[k],str(i), match2.auto_check_secret(str(i)) ]
            result = [database, table,columns[k],str(i), match.auto_check_secret(str(i)) ]
            result_str += str(result) + '\r\n' #对每个字段标识
            k += 1
    return result_str
    
     
if __name__ == '__main__':
        
        process_num = int(input('线程数： '))
        #数据库
        db = db_class.DB('localhost','debian-sys-maint','TTOn7ubVfTJJ89Y8','user_test')
        #多线程------对数据块分线程
        databases = db.get_database()  #  通过schemata获取所有数据库名称
        start_time = time.time()
        for database in databases:
            tables = db.get_table(database) #  获取表名
            for table in tables:
                columns = db.get_column(database,table) #  获取字段名
                data = db.get_line(database, table) #按行取数据
                #读取数据库数据耗费的时间并不多，可能是因为只有一个表吧:D
                print(len(data))
                data[0:2]
                res = [] 
                # 线程
                result_str = []
                i = 0
                with ThreadPoolExecutor(max_workers=process_num) as t:
                    print('34134234234234')
                    res = t.submit(lambda cxp:sensitive_word_recognize(*cxp),(database, table,columns, data, 0, 1)).result()
                    print("-------------------------")
                    result_str.append(res)
        end_time = time.time()    
        print(end_time - start_time)    
        with open('message2.txt','a+',encoding='UTF-8') as file:
            for result in result_str :
                file.write(result)       
            file.write("耗时：{:.2f}秒".format(end_time-start_time))    


        # 正则表达式
        # bc = match2.check_secret(match2.bank_card_pattern, '我的手机号是18590085340,身份证是110101199003072957,银行卡是6225806592337329,我的邮箱是aka@gmail.com')
        # print('银行卡',bc)
        # bc = match2.check_secret(match2.moblie_phone_pattern, '我的手机号是18590085340,身份证是110101199003072957,银行卡是6225806592337329,我的邮箱是aka@gmail.com')
        # print('手机',bc)
        # bc = match2.check_secret(match2.id_pattern, '我的手机号是18590085340,身份证是110101199003072957,银行卡是6225806592337329,我的邮箱是aka@gmail.com')
        # print('身份证',bc)
        # bc = match2.check_secret(match2.email_pattern, '我的手机号是18590085340,身份证是110101199003072957,银行卡是6225806592337329,我的邮箱是aka@gmail.com')
        # print('邮箱',bc)

        # # Hanlp 自然语言处理
        # address_list,name_list = match2.check_chinese_address_and_name('我家在北京市东城区东长安街, 我叫金翠花, 我的手机号是18590085340, 身份证是110101199003072957, 银行卡是6225806592337329, 我的邮箱是aka@gmail.com')
        # print('地址', address_list)
        # print('名字', name_list)
        # print(match2.match('我家在北京市asljda@outlook.com东城区东长安街,gongzheng@qq.com 我叫金翠花, 我的手sdfsdfsd机号是18590085340, 身份证是110101199003072957, 银行卡是6225806592337329, 我的邮箱是aka@gmail.com,11010119900307295X'))