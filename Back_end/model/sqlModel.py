import pymysql
class SqlModel():
    #构造函数
    def __init__(self): 
        # 连接：这个在本项目中都是固定的，直接固定
        self.db = pymysql.connect(
            host="101.34.48.210",port=3306,user="root",passwd="Wangweijie123",database="zjw"
        )
        
        # 游标：以字典形式返回 
        self.cur = self.db.cursor(pymysql.cursors.DictCursor)

    #析构函数
    def __del__(self):
        #    self.db.close()
        return 
    # 增
    def sqlInsert(self, sql):                                                          
        try:    
            self.db.ping(reconnect=True)
            self.cur.execute(sql)
            data = self.db.insert_id()  ###要在db.commit()之前才能起作用！！！！
            self.db.commit()
            print("插入成功")
            return data

        except Exception as e:
            print("插入失败",e)
            self.db.rollback()
        self.cur.close()
        self.db.close()
# 删
    def sqlDelete(self, sql):                                                          
        try: 
            self.db.ping(reconnect=True)   
            self.cur.execute(sql)
            self.db.commit()
            print("删除成功")
            
        except Exception as e:
            print("删除失败",e)
            self.db.rollback()
        self.cur.close()
        self.db.close()
# 改
    def sqlUpdate(self, sql):                                                          
        try:
            self.db.ping(reconnect=True)    
            self.cur.execute(sql)
            self.db.commit()
            print("更新成功")
            
        except Exception as e:
            print("更新失败",e)
            self.db.rollback()
        self.cur.close()
        self.db.close()
# 查

    def sqlSelect(self, sql:str, get_one:bool=False):                                                         
        
        try: 
            self.db.ping(reconnect=True)  ###现在设置的时间是10分钟，但是
            self.cur.execute(sql)
            if get_one:
                
                data = self.cur.fetchone()
            else:
                data = self.cur.fetchall()
            self.db.commit()
            print("查询成功")
            return data
        except Exception as e:
            print("查询失败",e)
            self.db.rollback()
        self.cur.close()
        self.db.close()


        
        
    
if __name__=="__main__":
    '''
    目前只有增删改查功能
    类：SqlModel
    类方法:sqlSelect(sql,get_one=false) sql为命令，get_one：Ture：只拿一条 Fals：拿全部 ；默认为False
           sqlInsert(sql)
           sqlDelete(sql)
           sqlUpdate(sql)
    若sql内用变量，替换方法在下面例子中，两种格式化方法

    '''
    #例子------------------
    #创建实例
    sqlmodel = SqlModel()
    
    # 插入
    ## 变量替换方式：两种方式效果相同---------------------------------
    sql = "INSERT INTO xmy(sname,passwd) VALUES ('%s','%s')"%("123","456")
    ss = "INSERT FROM xmy(sname,passwd) VALUES ({v1},{v2})".format(v1="123",v2="456")  
    data2=sqlmodel.sqlInsert(sql)
    print("insert:",data2)
    
    #查询
    sql0 =  "SElECT * FROM xmy"
    data = sqlmodel.sqlSelect(sql,get_one=False)
    print(data)
    # 删除
    sql2 = "DELETE FROM xmy WHERE xmy.sid<2"
    sqlmodel.sqlDelete(sql2)

    #修改
    sql3 = "UPDATE xmy set sname='xixi' WHERE xmy.sid=33"
    sqlmodel.sqlUpdate(sql3)