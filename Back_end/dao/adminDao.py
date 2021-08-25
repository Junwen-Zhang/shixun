from model.sqlModel import SqlModel


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

def updateInformationSingle(edit_name:str,edit_data:str,uname:str):
    sql = """UPDATE user set %s ='%s'
             WHERE user.uname='%s'""" \
            %(edit_name,edit_data,uname)   #不是uid是uname
    sqlmodel.sqlUpdate(sql)   #返回user那一列的所有信息
    return