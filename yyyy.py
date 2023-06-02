from pyhanlp import *
import re, sys

s1 = "无风险"
s2 = "低风险"
s3 = "中风险"
s4 = "高风险"

Address = r'(ns|nsf|nz)' #地址
Person_Name = r'nr|nrf' #人名

bank_card_pattern = r'([1-9]{1}\d{15}|\d{18})' #银行卡号
moblie_phone_pattern = r'1[356789]\d{9}' #手机号
phone_pattern = r'\d{3}-\d{8}|\d{4}-\d{7}' #固话
id_pattern = r'[1-9]\d{5}(?:18|19|(?:[23]\d))\d{2}(?:(?:0[1-9])|(?:10|11|12))(?:(?:[0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]'#身份证
email_pattern = r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)' #邮箱

# def extractPhrase(sentence, num):#短语提取
#     phraseList = HanLP.extractPhrase(sentence,num)
#     return phraseList

# def TranslatedNameRecognize(sentence): #音译名
#     person_ner = HanLP.newSegment().enableTranslatedNameRecognize(True)
#     p_name = person_ner.seg(sentence)
#     return p_name

def NameRecognize(sentence): #中国人名识别
    NER=HanLP.newSegment().enableNameRecognize(True)
    p_name=NER.seg(sentence)
    return p_name

def check_secret(pattern, value):
    return re.findall(pattern, value)

def match(sentence):
    seg_text = NameRecognize(sentence)
    dict = {}
    for i in seg_text:
        dict[str(i.word)] = [str(i.nature)]

    sensitive_list = []
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
    
    # for column in [email,bank_card,phone] : # 中风险 -- 邮箱、银行卡、固话
    #     for key in column :
    #         sensitive_list.append(key + ' %s' % s3) 

    # for column in [mobile_phone,id,address_list,name_list]: #高风险 -- 手机号、身份证、地址、姓名
    #     for key in column :
    #         sensitive_list.append(key + ' %s' % s4) 
    # sensitive_list=[email,bank_card,phone,mobile_phone,id,address_list,name_list]/
    return email,bank_card,phone,mobile_phone,id,address_list,name_list


# print(match('我家在北京市asljda@outlook.com东城区东长安街,gongzheng@qq.com 我叫金翠花, 我的手sdfsdfsd机号是18590085340, 身份证是110101199003072957, 银行卡是6225806592337329, 我的邮箱是aka@gmail.com,11010119900307295X'))
# print(match('11010119900307295'))
# nrf---音译名； nr---名字
#地址：ns|nz

# print('--------------------------------')

# print(TranslatedNameRecognize('微软的gongzheng@qq.com 、Facebook的扎克伯格gongzheng@gmail.com跟桑123123412@qq.com德博格、'))

# print(TranslatedNameRecognize('1232131'))