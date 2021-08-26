#引入路由管理
from fastapi import APIRouter,UploadFile,File,Request,Body,Form
#让数据以json格式返回所用到的库
from fastapi.responses import JSONResponse,Response
from service import adminService
from model.userModel import UserModel


router = APIRouter()

#显示所有用户和数量
@router.get("/display_users",tags=["admin"])
async def displayUsers():
    return adminService.displayUsers()


#目前是假删
#删除用户 传过来uname进行删除   只做了那个删除数据表里面的人！！！！！uname=已注销 所有东西都清空
@router.post("/delete_user",tags=["admin"])
async def deleteUserFake(uname:str=Body(...)):   #delete这里是不是一定要请求体？？？？？
    return adminService.deleteUserFake(uname)


#查询用户--模糊查询用户
@router.get("/select_user",tags=["admin"])
async def selectUser(uname:str):
    return adminService.selectUserByName(uname)
