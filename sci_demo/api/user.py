#引入路由管理
from fastapi import APIRouter
#让数据以json格式返回所用到的库
from fastapi.responses import JSONResponse,Response
router = APIRouter()
from service import userService
from model.userModel import UserModel

'''
这一块就是fastapi的核心
'''
#根据提前设计的接口文档
#获取用户的信息数据   接受了数据之后，还要去做一些反馈
@router.get("/getUsers/{uname}", tags=["users"]) #tags:标题/分类
async def getusers(uname:str):
    ### 1.假设已经通过服务（逻辑层）获取到相应的数据(要去调用相应的服务)
         #控制层不能有逻辑判断，有就放到逻辑层中，控制层只关心数据的接受和返回
    # 通过调用相应的服务得到对应的反馈
    return userService.getUsersInfos(uname)

@router.post("/request_body/register", tags=["users"])
async def register(userInfo:UserModel):
     print("control layer---")
     
     return userService.usersRegister(userInfo)