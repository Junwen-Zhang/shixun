import pymysql
from model.sqlModel import SqlModel
from fastapi import Body

sqlmodel = SqlModel()

def search_audioinfo(uid:int):
    sql = """SElECT * 
             FROM user 
             WHERE user.uid='%s'"""%(uid)
    data = sqlmodel.sqlSelect(sql)   #返回用户名和密码
    print(data[0])
    return data[0]["aspeed"],data[0]["apit"],data[0]["avol"],data[0]["aper"]


def updateAudioinfo(spd,pit,vol,per,uid):
    sql = """UPDATE user 
    set %s =%s,%s =%s,%s =%s,%s =%s 
    WHERE user.uid=%s"""%("aspeed",spd,"apit",pit,"avol",vol,"aper",per,uid)   
    print(sql)
    sqlmodel.sqlUpdate(sql)   
    return