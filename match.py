import pymysql
import re, sys
from math import ceil
import threading
from pyhanlp import *

# http://www.360doc.com/content/21/0220/19/13664199_963059614.shtml
moblie_phone_pattern = re.compile(r'1[356789]\d{9}')
# moblie_phone_pattern = re.compile(r'(13[0-9]|14[0145-9]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}')
phone_pattern = re.compile(r'0\d{2,3}-[1-9]\d{6,7}') #固话
# id_pattern = re.compile(r'[1-9]\d{5}(?:18|19|(?:[23]\d))\d{2}(?:(?:0[1-9])|(?:10|11|12))(?:(?:[0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]')#18位身份证
id_pattern = re.compile(r'([1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx])|([1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2})')
email_pattern = re.compile(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)')
bank_card_pattern = re.compile(r'([1-9]{1}\d{15}|\d{18})')
digit_pattern = re.compile(r'0|1|2|3|4|5|6|7|8|9')
Address = r'(ns|nsf|nz|nt)' #地址

Person_Name = r'nr|nrf' #人名

CRFnewSegment = HanLP.newSegment("crf")  # 通过crf算法识别实体

s1 = "无风险"
s2 = "低风险"
s3 = "中风险"
s4 = "高风险"

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
            result = [database, table,columns[k],str(i), auto_check_secret(str(i))]
            result_str += str(result) + '\r\n' #对每个字段标识
            k += 1
    return result_str

def check_secret(pattern, value):
    return pattern.findall(value)


def check_id(value):
    if re.match(id_pattern, value):
        return (value + ' 身份证 %s' % s4)
    else :
        return (value + ' 8 %s' % s1) 
    
def check_phone(value):
    if re.match(phone_pattern, value):
        return (value + ' 固话 %s' % s3)
    else :
        return (value + ' 8 %s' % s1)
    
def check_mobile_phone(value):
    if re.match(moblie_phone_pattern,value) and len(value) == 11: #手机号 -- 高风险
        return (value + ' 手机 %s' % s4)
    else :
        return (value + ' 8 %s' % s1)

def check_email(value):
    if re.match(email_pattern,value): #邮箱 -- 中风险
        return (value + ' 邮箱 %s' % s3)
    else :
        return (value + ' 8 %s' % s1)

def check_bank_card(value):
    if re.match(bank_card_pattern,value): #银行卡  -- 中风险
        return (value + ' 银行卡 %s' % s3)
    else :
        return (value + ' 8 %s' % s1)

def check_chinese_address_and_name(value):
    seg_text = CRFnewSegment.seg(value)

    Address = r'(ns|nsf|nz|nt)'
    #大学是 ntu
    Person_Name = r'nr'  

    dict = {}
    address_list = []
    name_list = []
    
    for i in seg_text:
        dict[str(i.word)] = [str(i.nature)]
    
    for key, value in dict.items():
        # print(key, value)
        value = str(value)
        if re.search(Address, value):
            address_list.append(key)
        if re.search(Person_Name, value):
            name_list.append(key)
    return address_list, name_list


def auto_check_secret(value):
    address_list = [] #地址
    name_list = [] #姓名
#and len(value) == 18
    if len(value) <= 1:
        return (' 8 %s' % s1) # 无风险
    
    if re.match(id_pattern,value)  : #身份证 -- 高风险
        return (value + ' 身份证 %s' % s4)
    elif re.match(bank_card_pattern,value) and len(value) == (15 or 18): #银行卡  -- 中风险
        return (value + ' 银行卡 %s' % s3)
    elif re.match(phone_pattern,value): #固话 --- 中风险
        return (value + ' 固话 %s' % s3)
    elif re.match(email_pattern,value): #邮箱 -- 中风险
        return (value + ' 邮箱 %s' % s3)
    elif re.match(moblie_phone_pattern,value) and len(value) == 11: #手机号 -- 高风险
        return (value + ' 手机 %s' % s4)
    # if ('\u4e00' <= value[0] <= '\u9fa5'): #中文字符 --- 字段
    #     address_list,name_list =check_chinese_address_and_name(value) #判别地址和姓名
    #     if address_list :
    #         return (str(value) + ' 地址 %s' % s4) #地址 -- 高风险
    #     if name_list :
    #         return (str(value) + ' 姓名 %s' % s4) #姓名 -- 高风险
    
    sensitive_list = []
    email,bank_card,phone,mobile_phone,id,address_list,name_list=sentence_match(value) #备注消息
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



def NameRecognize(sentence): #识别
    NER=HanLP.newSegment().enableNameRecognize(True)
    p_name=NER.seg(sentence)
    return p_name

def sentence_match(sentence):

    seg_text = NameRecognize(sentence)
    dict = {}
    # print(seg_text)
    for i in seg_text:
        dict[str(i.word)] = [str(i.nature)]

    email = check_secret(email_pattern, sentence) #邮箱

    phone = check_secret(phone_pattern, sentence) #固话

    #英文：nx

    address_list = []
    name_list = []
    mobile_phone = []
    bank_card = []
    id = []
    seg_text = NameRecognize(sentence)
    dict = {}
    for i in seg_text:
        dict[str(i.word)] = [str(i.nature)]

    for key, value in dict.items():
        value = str(value)
        if re.search(Address, value): #地址 
            address_list.append(key)
        if re.search(Person_Name, value): #姓名 
            name_list.append(key)

        if re.search(r'm', value): #值为数字
            if re.match(id_pattern, value) and len(value) == (15 or 18): #身份证
                id.append(key)
            elif re.match(bank_card_pattern,key) and len(value) == 16: #银行卡  
                bank_card.append(key)
            elif re.match(moblie_phone_pattern,key) and len(value) == 11: #手机号 
                mobile_phone.append(key)
    return email,bank_card,phone,mobile_phone,id,address_list,name_list