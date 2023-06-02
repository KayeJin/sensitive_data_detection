import pymysql
import re, sys
import threading
from pyhanlp import *
# import match

# http://www.360doc.com/content/21/0220/19/13664199_963059614.shtml
moblie_phone_pattern = re.compile(r'1[356789]\d{9}')
phone_pattern = re.compile(r'\d{3}-\d{8}|\d{4}-\d{7}') #固话
id_pattern = re.compile(r'[1-9]\d{5}(?:18|19|(?:[23]\d))\d{2}(?:(?:0[1-9])|(?:10|11|12))(?:(?:[0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]')
email_pattern = re.compile(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)')
bank_card_pattern = re.compile(r'([1-9]{1}\d{15}|\d{18})')
digit_pattern = re.compile(r'0|1|2|3|4|5|6|7|8|9')
Address = r'(ns|nsf|nz)' #地址
Person_Name = r'nr|nrf' #人名

CRFnewSegment = HanLP.newSegment("crf")  # 通过crf算法识别实体

s1 = "无风险"
s2 = "低风险"
s3 = "中风险"
s4 = "高风险"

def check_secret(pattern, value):
    return pattern.findall(value)

def auto_check_secret(value):
    address_list = [] #地址
    name_list = [] #姓名

    if re.match(id_pattern,value): #身份证 -- 高风险
        return (value + '3 %s' % s4)
    elif re.match(bank_card_pattern,value): #银行卡  -- 中风险
        return (value + '5 %s' % s3)
    elif re.match(phone_pattern,value): #固话 --- 中风险
        return (value + '1 %s' % s3)
    elif re.match(email_pattern,value): #邮箱 -- 中风险
        return (value + '4 %s' % s3)
    elif re.match(moblie_phone_pattern,value): #手机号 -- 高风险
        return (value + '2 %s' % s4)
    if ('\u4e00' <= value[0] <= '\u9fa5'): #中文字符 --- 字段
        address_list,name_list =check_chinese_address_and_name(value) #判别地址和姓名
        if address_list :
            return (str(address_list) + '6 %s' % s4) #地址 -- 高风险
        if name_list :
            return (str(name_list) + '7 %s' % s4) #姓名 -- 高风险
    if value is None or re.match(digit_pattern,value):
        return ('8 %s' % s1) # 无风险
    sensitive_list = []
    email,bank_card,phone,mobile_phone,id,address_list,name_list=match(value)
    for column in [email,bank_card,phone] : # 中风险 -- 邮箱、银行卡、固话
            for key in column :
                sensitive_list.append(key + ' %s' % s3) 

    for column in [mobile_phone,id,address_list,name_list]: #高风险 -- 手机号、身份证、地址、姓名
        for key in column :
            sensitive_list.append(key + ' %s' % s4) 
    if sensitive_list :
        return sensitive_list
    else: 
        return ('8 %s' % s1) # 无风险

def check_chinese_address_and_name(value):
    seg_text = CRFnewSegment.seg(value)

    Address = r'(ns|nsf|nz)'
    Person_Name = r'nr'
    
    dict = {}
    
    address_list = []
    name_list = []
    
    for i in seg_text:
        dict[str(i.word)] = [str(i.nature)]
    
    for key, value in dict.items():
        # print(key, value)
        # print("-------------")
        value = str(value)
        if re.search(Address, value):
            address_list.append(key)
        if re.search(Person_Name, value):
            name_list.append(key)
    return address_list, name_list

def NameRecognize(sentence): #中国人名识别
    NER=HanLP.newSegment().enableNameRecognize(True)
    p_name=NER.seg(sentence)
    return p_name

def match(sentence):
    seg_text = NameRecognize(sentence)
    dict = {}
    for i in seg_text:
        dict[str(i.word)] = [str(i.nature)]

    email = check_secret(email_pattern, sentence)

    # mobile_phone = check_secret(moblie_phone_pattern, sentence)
    phone = check_secret(phone_pattern, sentence) #固话
    id = check_secret(id_pattern, sentence)
    # bank_card = check_secret(bank_card_pattern, sentence)
    #英文：nx

    address_list = []
    name_list = []
    # id = []
    phone = []
    mobile_phone = []
    bank_card = []

    for key, value in dict.items():
        value = str(value)
        if re.search(Address, value): #地址 
            address_list.append(key)
        if re.search(Person_Name, value): #姓名 
            name_list.append(key)

        if re.search(r'm', value):
            if not True in [key in i for i in id]: # 不在身份证的数字
                if re.match(bank_card_pattern,key): #银行卡  
                    bank_card.append(key)
                elif re.match(moblie_phone_pattern,key): #手机号 
                    mobile_phone.append(key)
    return email,bank_card,phone,mobile_phone,id,address_list,name_list