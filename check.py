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
import db_class

    

if __name__ == '__main__':
        
    # process_num = int(input('线程数： '))
    # #数据库
    # db = db_class.DB('localhost','debian-sys-maint','TTOn7ubVfTJJ89Y8','user_test')
    # #多线程------对数据块分线程
    # databases = db.get_database()  #  通过schemata获取所有数据库名称
    # start_time = time.time()
    # for database in databases:
    #     tables = db.get_table(database) #  获取表名
    #     for table in tables:
    #         columns = db.get_column(database,table) #  获取字段名
    #         data = db.get_line(database, table) #按行取数据
    #         #读取数据库数据耗费的时间并不多，可能是因为只有一个表吧:D
    #         print(len(data))
    #         # data[0:2]
    #         res = [] 
    #         # 线程
    #         result_str = []
    #         i = 0
    #         with ThreadPoolExecutor(max_workers=process_num) as t:
    #             res = t.submit(lambda cxp:match.sensitive_word_recognize(*cxp),(database, table,columns, data, 0, 1)).result()
    #             print("-------------------------")
    #             result_str.append(res)
    # end_time = time.time()    
    # print(end_time - start_time)    
    # with open('message2.txt','a+',encoding='UTF-8') as file:
    #     for result in result_str :
    #         file.write(result)       
    #     file.write("耗时：{:.2f}秒".format(end_time-start_time))    

    bc = match.auto_check_secret(input('查询值： '))
    print(bc)
        