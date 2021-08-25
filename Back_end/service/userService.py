# 服务层当中，就是方法（服务），服务是不能命名为数据库的操作名字的curd
# 就应该先写服务，接口只是一个桥聊
from fastapi.responses import JSONResponse,Response
from fastapi import Request,File,UploadFile,Body,Form
from dao import userDao #就一定要用到持久化层
from model.userModel import UserModel
from model.emailModel import EmailModel
import hashlib
from pathlib import Path
from aiopathlib import AsyncPath
from fastapi.staticfiles import StaticFiles
import cv2 as cv
from tempfile import NamedTemporaryFile
import shutil
import os
BASE_DIR = Path(__file__).resolve().parent #当前这个文件的父文件

# def getUsersInfos(uname):
#     ## 1、就是做需求的逻辑操作（对数据的处理，可能涉及到持久化层 这个数据不一定要入库，要根据需求决定）
#     data = userDao.selectUsers(uname)
#     ## 2、由服务作出相应的数据反馈
#     return JSONResponse(
#         content={
#             'data':{
#                 "users":data
#             }
#         }
#     )

# def buyProductsService(products):
#     ## 1、下订单
#     ## 2、减库存  可以把这个服务拆分出来，提高代码的复用性
#     pass

# def get_host(req) -> str:
#     return getattr(req,"headers",{}).get("host") or "http://127.0.0.1:8000"

def emailVerification(email:str):
    #首先判断邮箱是否已存在：一个邮箱只能绑定一个账户
    data = userDao.selectUsersByEmail(email)
    if(data):
        return JSONResponse(
        content={
            "code":422,
            "data":{
                "email":email
            },
            "message":"邮箱已注册"
        }
    )

    #增加邮箱验证模块
    try:
        emailmodel = EmailModel()
        emailcode = emailmodel.registerEmail(email) #发送验证码
        return JSONResponse(
        content={
            "code":200,
            "data":{
                "emailCode":emailcode
            },
            "message":"邮箱发送成功"
        }
    )
    except Exception as e:
        return JSONResponse(
        content={
            "code":400,
            "data":{
                "error":e
            },
            "message":"邮箱发送失败"
        }
    )   

def usersRegister(userInfo:UserModel):
    #判断用户是否重名，且“已注销”不合法
    if (userInfo.uname=="已注销"):
        return JSONResponse(
        content={
            "code":400,
            "data":{
                "uname":userInfo.uname,
                "upasswd":userInfo.upasswd,
                "uemail":userInfo.uemail
            },
            "message":"用户名不合法"
        }
    )
    else:
        data = userDao.selectUsersByName(uname=userInfo.uname)
        if(data):
            return JSONResponse(
            content={
                "code":422,
                "data":{
                    "uname":userInfo.uname,
                    "upasswd":userInfo.upasswd,
                    "uemail":userInfo.uemail
                },
                "message":"用户名已存在"
            }
        )
        else:
            userDao.insertUsers(userInfo)
            return JSONResponse(
                content={
                    "code":200,
                    "data":{
                        "uname":userInfo.uname,
                        "upasswd":userInfo.upasswd,
                        "uemail":userInfo.uemail
                    },
                    "message":"用户创建成功"
                }
            )

def usersLogin(uname:str,upasswd:str):
    if (uname == "已注销"):
        return JSONResponse({
                "code":000,
                "data":{
                },
                "message":"该用户名不合法"
            })     
    data = userDao.selectUsersByName(uname)
    # print(data)
    if (data):             #判断元祖是否为空的直接这样
        passwd = data[0]["upasswd"]
        if (upasswd == passwd):
            return JSONResponse({
                "code":200,
                "data":{
                    "user_data":data    ##用户登录，要返回这个user的所有信息
                },
                "message":"密码匹配"
            })
        else:
            return JSONResponse({
                "code":400,
                "data":{
                },
                "message":"密码不匹配"
            })    
    else: 
        return JSONResponse({
                "code":422,        
                "data":{
                },
                "message":"此用户不存在"
            })
        

def informationUpdateAll(userInfo:UserModel):   ##用户更新信息也应该返回，改变的user的这个信息
    userDao.updateInformationAll(userInfo)   #首先更新了
    # data = userDao.selectUsersByName(userInfo.uname)  #然后返回更新的这一条全部的user信息
    return JSONResponse(
        content={
            'code':200,
            'data':{
                "user_data":userInfo.dict()
            },
            'message':'修改成功'
        }
    )
#以邮箱作为key，修改密码，并返回用户信息
def changePasswd(uemail:str,upasswd:str):
    userDao.updateInformationSingleByEmail(edit_name="upasswd",edit_data=upasswd,uemail=uemail)
    data = userDao.selectUsersByEmail(uemail)
    return JSONResponse(
        content={
            'code':200,
            'data':{
                "user_data":data
            },
            'message':'修改密码成功'
        }
    )

#优化photoUpload-------------------
def photoUpload(uname:str=Form(...), photofile:UploadFile=File(...)):   
    peanutweb="http://424z7l3858.qicp.vip"   ##花生壳网址 注意：以后对接的时候，这个花生壳网址会改变！！！！
    suffix = Path(photofile.filename).suffix #尾缀
    localaddress = "./assets/pictures/"+uname+suffix #本地静态资源库的地址 .../表示上一级文件目录:反正就是不对 用./：不知道为什么？？？？？？？
    fileaddress = peanutweb+"/assets/pictures/"+uname+suffix  #在网站上前端访问的地址 
    try:
        '''
        以前该种写法，每次生成的文件的名称不同，就会导致用户以前上传的头像也会被记住，
        如今在命名上为uname，那么一个用户永远只有一个头像文件【不一定，后缀不同】，且命名都是统一的，也可以不用上传到数据库了【还是需要，可能后缀会不同】
        '''
        #以前版本：NamedTemporaryFile的名字是不能定的，因此只能改用file
        # with NamedTemporaryFile(delete=False, suffix=suffix,dir=save_dir,prefix=uname) as tmp:    
        #     shutil.copyfileobj(photofile.file,tmp)
        #     tmp_file_name = Path(tmp.name).name      #查询tmp的名字    
        #     address = peanutweb+"/assets/pictures"+tmp_file_name 
        #     #address = f"http://424z7l3858.qicp.vip/assets/{tmp_file_name}"  #f：格式化字符串
        #     print(address)    
        newfile = open(localaddress,'wb') #以字节形式写入要加b
        shutil.copyfileobj(photofile.file,newfile) #复制文件 用newfile.write也写
        print(fileaddress)
    except Exception as e:
        print("失败",e)
    finally:
        photofile.file.close()
    userDao.updateInformationSingle("uphoto",fileaddress,uname)
    return JSONResponse(
        content={
            'code':200,
            'data':{
                'image':fileaddress
            },
            'message':'上传头像成功'
        }
    )
