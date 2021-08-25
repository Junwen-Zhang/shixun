#引入路由管理
from fastapi import APIRouter,UploadFile,File,Request,Body,Form
#让数据以json格式返回所用到的库
from fastapi.responses import JSONResponse,Response
from service import userService
from model.userModel import UserModel
# from pydantic import Field
router = APIRouter()
'''
这一块就是fastapi的核心，事例
'''
#根据提前设计的接口文档
#获取用户的信息数据   接受了数据之后，还要去做一些反馈
# @router.get("/getUsers/{uname}", tags=["users"]) #tags:标题/分类
# async def getusers(uname:str):
#     ### 1.假设已经通过服务（逻辑层）获取到相应的数据(要去调用相应的服务)
#          #控制层不能有逻辑判断，有就放到逻辑层中，控制层只关心数据的接受和返回
#     # 通过调用相应的服务得到对应的反馈
#     return userService.getUsersInfos(uname)

'''
用户注册以及登陆
'''
# 邮箱验证：输入返回验证码
@router.get("/email_verification", tags=["users"])    #Field只能在pydantic里面使用
async def emailVerification(email:str):
     return userService.emailVerification(email)

# 用户注册
@router.post("/register", tags=["users"])  #请求体格式
async def register(userInfo:UserModel):
     return userService.usersRegister(userInfo)
# 用户登录 接受数据
@router.get("/login", tags=["users"])   #使用get接口不能用请求体作为参数!!!!!!!!!!!!!!
async def login(uname:str,upasswd:str):
     return userService.usersLogin(uname,upasswd)

#修改密码/忘记密码 是通过邮箱来查找
@router.put("/change_password", tags=["users"])
async def changePasswd(uemail:str=Body(...),upasswd:str=Body(...)):
     return userService.changePasswd(uemail,upasswd)


'''
用户个人信息更改 以用户的账户名来查询
'''
#用户头像上传 --------------暂且用post 其实感觉put应该也行？后面就是修改啥的:除密码和头像之外的属性
@router.post("/settings/photo_upload", tags=["users"])
async def photoUpload(uname:str = Form(...), photofile:UploadFile = File(...)):
     return userService.photoUpload(uname, photofile)

##将下面的所有修改变为一个接口     
@router.put("/settings", tags=["users"])
async def informationUpdate(userInfo:UserModel):
     return userService.informationUpdateAll(userInfo)



# #邮箱
# @router.put("/settings/email", tags=["users"])
# async def emailEdit(uname:str=Body(...),email:str=Body(...)):
#      return userService.informationEdit("uemail",uname,email)
# #手机号
# @router.put("/settings/phone", tags=["users"])
# async def phoneEdit(uname:str=Body(...),phone:str=Body(...)):
#      return userService.informationEdit("uphone",uname,phone)    
# #性别 根本就不用单独提出来转化为1,0，直接存男女就好了
# @router.put("/settings/sex", tags=["users"])
# async def sexEdit(uname:str=Body(...),sex:str=Body(...)):
#      return userService.informationEdit("usex",uname,sex)  
# #年龄
# @router.put("/settings/age", tags=["users"])
# async def ageEdit(uname:str=Body(...),age:str=Body(...)):
#      return userService.informationEdit("uage",uname,age)
# #个性签名
# @router.put("/settings/signature", tags=["users"])
# async def signatureEdit(uname:str=Body(...),signature:str=Body(...)):
#      return userService.informationEdit("usignature",uname,signature) 

