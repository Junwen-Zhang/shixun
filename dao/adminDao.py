from model.sqlModel import SqlModel

peanutweb="http://120.78.204.183"
sqlmodel = SqlModel()
def selectAllUsers():
    sql = "SElECT * FROM user"
    data = sqlmodel.sqlSelect(sql,get_one=False)
    return data

#通过用户的账户名删除一个用户
def deleteUser(uname:str):
    sql="DELETE FROM user WHERE user.uname='%s'"%(uname)
    sqlmodel.sqlDelete(sql)
    return 

#通过用户的账户名查找用户  变成模糊查询
def selectUsersByName(uname:str):
    sql = """SElECT * 
            FROM user 
            WHERE user.uname LIKE '%{uname}%'""".format(uname=uname)
    data = sqlmodel.sqlSelect(sql,get_one=False)   #返回user这一列的信息
    # print(data)
    return data
#通过用户的Id查找用户
def selectUsersById(uid:int):
    sql = """SElECT * 
            FROM user 
            WHERE user.uid = {uid}""".format(uid=uid)
    data = sqlmodel.sqlSelect(sql,get_one=False)   #返回user这一列的信息
    # print(data)
    return data

def updateInformationSingleByName(edit_name:str,edit_data:str,uname:str):
    sql = """UPDATE user set %s ='%s'
             WHERE user.uname='%s'""" \
            %(edit_name,edit_data,uname)   #不是uid是uname
    sqlmodel.sqlUpdate(sql)   #返回user那一列的所有信息
    return

def updateInformationAllById(uid:int):
    photo = peanutweb+"/assets/pictures/已注销.png"
    sql = """UPDATE user set uname = "已注销",uphoto="%s",uage="",uemail="",uphone="",usignature="",ubirth=""
             WHERE user.uid=%s""" \
            %(photo,uid)   #不是uid是uname
    sqlmodel.sqlUpdate(sql)   #返回user那一列的所有信息
    return