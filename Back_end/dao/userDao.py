# # 一般，一个表对应一个Dao层的操作 ---每个表有个相应的持久层的操作--拆分的思想
# # 约定大于配置

# # 数据持久化层 方法名前缀只有 insert, update, select, delete

# #pymysql 就是用来做数据库操作的 用的最多的：excute，fecthall、fetchone
# import pymysql
# from model.userModel import UserModel

# def selectUsers(uname):    ##!!!host最先写错了，210写成201！！！
#     db = pymysql.connect(host="101.34.48.210",port=3306,user="root",passwd="Wangweijie123",database="zjw")
#     # 使用 cursor() 方法创建一个游标对象 cursor
#     cursor = db.cursor(cursor = pymysql.cursors.DictCursor) ##pymysql返回字典，本来是元组变成字典【这里直接做了，可以就不用模型层了】
#     #使用sql语句
#     sql = """SELECT * from `student` """  ##可以现在数据库里面运行一下 这里重点是sql语句--------------
#     # 使用 execute()  方法执行 SQL 查询 
#     try:
#     #执行sql语句
#         cursor.execute(sql)
#         data = cursor.fetchall()
#     ## 游标可以进行循环（循环游标进行数据的填充）
#     ## 可以加查询的数据填充（组合）到自定义的模型中（model层里面：就是一些模版）

#     #提交到数据库执行
#         db.commit()
#     #如果有错误则进行回滚
#     except:
#         db.rollback()
#     # 关闭数据库连接  --可以找那种可以不用一直开关的
#     db.close()
#     return data

# def userRegister(userInfo:UserModel):
#     db = pymysql.connect(host="101.34.48.210",port=3306,user="root",passwd="Wangweijie123",database="zjw")
#     # 
#     cursor = db.cursor(cursor = pymysql.cursors.DictCursor) 
    
#     sql = """INSERT INTO xmy(sname,passwd)
#             VALUES 
#             (%s,%s)
#             """
#     sname = userInfo.sname
#     passwd = userInfo.password
#     values = (sname,passwd)
#     try:
        
#         cursor.execute(sql,values)
#         # data = cursor.fetchall()
    

 
#         db.commit()
 
#     except:
#         db.rollback()
  
#     db.close()
#     return 