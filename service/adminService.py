from dao import adminDao
from fastapi.responses import JSONResponse

def displayUsers():
    data = adminDao.selectAllUsers() 
    return JSONResponse(
        content={
            "code":200,
            "data":{
                "users_data":data,
                "users_amount":len(data)
            },
            "message":"成功返回所有用户"
        }
    ) 

def deleteUserFake(uid:int):
    data = adminDao.selectUsersById(uid)
    print(data)
    if (data[0]["uname"]=="已注销"):
        return JSONResponse(
        content={
            "code":422,
            "data":{
                "user_id":uid
            },
            "message":"该用户已删除"
        }
    )
    adminDao.updateInformationAllById(uid)
    return JSONResponse(
        content={
            "code":200,
            "data":{
                "user_id":uid
            },
            "message":"删除该用户成功"
        }
    )

#变为模糊查询
def selectUserByName(uname:str):
    data = adminDao.selectUsersByName(uname)
    if (data):             #判断元祖是否为空的直接这样
        return JSONResponse({
                    "code":200,
                    "data":{
                        "user_data":data,
                        "user_number":len(data)
                    },
                    "message":"查找成功"
                })
    else: 
        return JSONResponse({
                    "code":422,        
                    "data":{
                    },
                    "message":"此用户不存在"
                })