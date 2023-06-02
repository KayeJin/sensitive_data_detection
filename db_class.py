import pymysql

class DB(object):
    def __init__(self,ip,username,password,db_name):
        self.ip = ip
        self.username = username
        self.password = password
        self.db_name = db_name
        self.db = pymysql.connect(host=self.ip,user=self.username,password=self.password,database=self.db_name)
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
        # self.cursor.execute("select %s from %s.%s LIMIT 0,1" %(column,database,table)) #选择前1条数据
        self.cursor.execute("select %s from %s.%s " %(column,database,table)) 
        content = self.cursor.fetchall()
        return content
        # if content:
        #     return content[0][0]
    
    #  获取所有行数据
    def get_line(self,database,table):
        self.cursor.execute("select * from %s.%s" %(database,table))
        content = self.cursor.fetchall()
        return content
    
    def __del__(self):
        self.db.close()