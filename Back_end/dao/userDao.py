# 一般，一个表对应一个Dao层的操作 ---每个表有个相应的持久层的操作--拆分的思想
# 约定大于配置

# 数据持久化层 方法名前缀只有 insert, update, select, delete

#pymysql 就是用来做数据库操作的 用的最多的：excute，fecthall、fetchone

import pymysql
from model.userModel import UserModel
from model.sqlModel import SqlModel
from fastapi import Body


# def selectUsers(uname):    ##!!!host最先写错了，210写成201！！！
#     data = sqlmodel.sqlSelct("sql")
#     return data



#插入用户的账户名、密码、邮箱
def insertUsers(userInfo:UserModel):  #用户注册uadmin=0 不是管理员---------
    sqlmodel = SqlModel()
    sql = "INSERT INTO user(uname,upasswd,uemail,uadmin,aspeed,apit,avol,aper) VALUES ('%s','%s','%s',0,5,5,5,0)"%(userInfo.uname,userInfo.upasswd,userInfo.uemail) ##特别注意这里%s上面有引号！！！！
    sqlmodel.sqlInsert(sql)

#通过用户的账户名查找用户
def selectUsersByName(uname:str):
    sqlmodel = SqlModel()
    sql = """SElECT * 
            FROM user 
            WHERE user.uname='%s'"""%(uname)
    data = sqlmodel.sqlSelect(sql)   #返回user这一列的信息
    return data
#通过用户的邮箱查找用户
def selectUsersByEmail(uemail:str):
    sqlmodel = SqlModel()
    sql = """SElECT * 
            FROM user 
            WHERE user.uemail='%s'"""%(uemail)
    data = sqlmodel.sqlSelect(sql)   #返回user这一列的信息
    return data

#更新该用户的所有信息【没有改变的就不管，但是不管是更新一个还是更新所有字段，反正都要更新，就包含在这个函数里面了】
# 6个属性：除了密码和头像不会改变，其他都会改变
# 通过uname修改---
def updateInformationAll(userInfo:UserModel):
    sqlmodel = SqlModel()
    sql = """UPDATE user set uage='%s',usex='%s',uemail='%s',uphone='%s',usignature='%s',ubirth='%s'
             WHERE user.uname='%s'""" \
            %(userInfo.uage,userInfo.usex,userInfo.uemail,userInfo.uphone,userInfo.usignature,userInfo.ubirth,userInfo.uname)   #不是uid是uname
    sqlmodel.sqlUpdate(sql)   #返回user那一列的所有信息
    return 

#更新该用户的一个属性【没有改变的就不管，但是不管是更新一个还是更新所有字段，反正都要更新，就包含在这个函数里面了】8个属性
#还是需要的 -------否则更新照片路径那里不好操作，那里不能生成一个现成userinfo，生成现成的其他属性都是None，可选，就不好
#通过uname修改---
def updateInformationSingle(edit_name:str,edit_data:str,uname:str):
    sqlmodel = SqlModel()
    sql = """UPDATE user set %s ='%s'
             WHERE user.uname='%s'""" \
            %(edit_name,edit_data,uname)   #不是uid是uname
    sqlmodel.sqlUpdate(sql)   #返回user那一列的所有信息
    
    return

def updateInformationSingleByEmail(edit_name:str,edit_data:str,uemail:str):
    sqlmodel = SqlModel()
    sql = """UPDATE user set %s ='%s'
             WHERE user.uemail='%s'""" \
            %(edit_name,edit_data,uemail)   #不是uid是uname
    print(sql)
    sqlmodel.sqlUpdate(sql)   #返回user那一列的所有信息

    return