# 服务层当中，就是方法（服务），服务是不能命名为数据库的操作名字的curd
# 就应该先写服务，接口只是一个桥聊
from fastapi.responses import JSONResponse,Response
from dao import userDao #就一定要用到持久化层
from model.userModel import UserModel

def getUsersInfos(uname):
    ## 1、就是做需求的逻辑操作（对数据的处理，可能涉及到持久化层 这个数据不一定要入库，要根据需求决定）
    data = userDao.selectUsers(uname)
    ## 2、由服务作出相应的数据反馈
    return JSONResponse(
        content={
            'data':{
                "users":data
            }
        }
    )

def buyProductsService(products):
    ## 1、下订单
    ## 2、减库存  可以把这个服务拆分出来，提高代码的复用性
    pass

def usersRegister(userInfo:UserModel):
    userDao.userRegister(userInfo)
    return JSONResponse(
        content={
            "code":"200",
            "data":{
                "user":userInfo.sname,
                "password":userInfo.password,
            },
            "message":"用户创建成功"
        }
    )