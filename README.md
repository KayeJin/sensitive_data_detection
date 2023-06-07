# sensitive_data_detection

db_class.py
处理数据库

check.py
判断接口

match.py

1. check\_实体名
   如 check_id、check_phone、check_mobile_phone、check_email、check_bank_card、check_chinese_address_and_name 分别检查输入的字符串是否属于身份证、固话、手机号、邮箱、银行卡、中文地址与姓名

2. check_secret
   使用正则表达式的 findall()，找到所有输入参数中满足 pattern 的字符串

3. sensitive_word_recognize
   对数据块的所有字段进行识别，index 和 size 参数方便在调用该函数前 对数据块分块

4. auto_check_secret
   自动识别敏感数据，可以识别单个实体与一段话

5. NameRecognize
   使用 Hanlp 进行分词

6. sentence_match
   识别一段话中的敏感消息
