# 服务层当中，就是方法（服务），服务是不能命名为数据库的操作名字的curd
# 就应该先写服务，接口只是一个桥聊
from fastapi.responses import JSONResponse,Response
from fastapi import Request,File,UploadFile,Body,Form
from dao import userDao #就一定要用到持久化层
from model.userModel import UserModel
from model.emailModel import EmailModel
from model.faceModel import FaceModel
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

def emailVerification_Register(email:str):
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
def emailVerification_Changepasswd(email:str):
    # #首先判断邮箱是否已存在：一个邮箱只能绑定一个账户
    # data = userDao.selectUsersByEmail(email)
    # if(data):
    #     return JSONResponse(
    #     content={
    #         "code":422,
    #         "data":{
    #             "email":email
    #         },
    #         "message":"邮箱已注册"
    #     }
    # )

    #增加邮箱验证模块
    try:
        emailmodel = EmailModel()
        emailcode = emailmodel.changePasswdEmail(email) #发送验证码
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
        return JSONResponse(
            content={
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
            return JSONResponse(
                content={
                "code":200,
                "data":{
                    "user_data":data    ##用户登录，要返回这个user的所有信息
                },
                "message":"密码匹配"
            })
        else:
            return JSONResponse(
                content={
                "code":400,
                "data":{
                },
                "message":"密码不匹配"
            })    
    else: 
        return JSONResponse(
            content={
                "code":422,        
                "data":{
                },
                "message":"此用户不存在"
            })
        

def informationUpdateAll(userInfo:UserModel):   ##用户更新信息也应该返回，改变的user的这个信息
    userDao.updateInformationAllByName(userInfo)   #首先更新了
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
        newfile.close()
    userDao.updateInformationSingleByName("uphoto",fileaddress,uname)
    return JSONResponse(
        content={
            'code':200,
            'data':{
                'image':fileaddress
            },
            'message':'上传头像成功'
        }
    )



def faceRecognition(uname:str=Body(...),face:UploadFile=File(...)):
    facemodel = FaceModel()
    #首先判断传入的照片是否有人脸
    # number = facemodel.face_detect(face.file)
    # if (number==0 or number>1):
    #     return JSONResponse(
    #         content={
    #             'code':422,
    #             'data':{
                    
    #             },
    #             'message':'图片未检测到人脸或图片有多张人脸'
    #         }
    #     )
    
    #从数据库中找到之前上传的照片
    data = userDao.selectUsersByName(uname)
    data_face = data[0]["uface"]
    face_path = "./assets/faces/"+data_face
    face_save = open(face_path,'rb')
    
    #刚传入的face去跟数据库里面的图片进行比对
    #是可以保证两张图片都有人脸的
    '''
    为什么这里face.file就可以呢？
    '''
    # face_tobe = open("./assets/temporary/",'rb')
    suffix = Path(face.filename).suffix
    localaddress = "./assets/temporary/"+uname+suffix #静态资源库地址
    face_to = open(localaddress,'wb')
    shutil.copyfileobj(face.file,face_to)
    face_to = open(localaddress,'rb')

    # number = facemodel.face_detect(face_to)    #这一步在前面使用face.file后face.file就损坏了！！在前面又损坏了！！！！！！！
    # if (number==0 or number>1):
    #     return JSONResponse(
    #         content={
    #             'code':422,
    #             'data':{
                    
    #             },
    #             'message':'图片未检测到人脸或图片有多张人脸'
    #         }
    #     )

    try: 
        result = facemodel.face_comparison(face_to,face_save)
        if (not result["face_found_in_image"]):
            return JSONResponse(
            content={
                'code':422,
                'data':{
                    
                },
                'message':'图片未检测到人脸或图片有多张人脸'
            }
        )
        # result = facemodel.face_comparison(face.file,face_save)    ### face.file！！！！！！
        if (result["is_same_person"]):
                return JSONResponse(
                content={
                    'code':200,
                    'data':{
                        'result':result
                    },
                    'message':"比对成功"
                }
            )
        else:
                return JSONResponse(
                content={
                    'code':400,
                    'data':{
                        'result':result
                    },
                    'message':"比对失败"
                }
            )
    except Exception as e:
        print("人脸比对失败",e)


#跟photoload差不多，不过多了一个人脸检测
#上传到uface的参数也改一下
def faceUpload(uname:str=Body(...),face:UploadFile=File(...)):
    facemodel = FaceModel()
    '''
    这种不行!!!!!!!!!!! 因为tmp不是一个文件流，除非先打开,但是临时文件不能打开
    不一定是文件流的错，face.file也是可以传给face_detect进行识别的，但是这个时候上传到静态资源库的图片就是打不开（有损坏），也不知道为什么。
    '''
    # #首先判断传入的照片是否有人脸----------------------------------------------
    # face_ori = face.file
    # # with NamedTemporaryFile(delete=True) as tmp:    
    # #     shutil.copyfileobj(face_ori,tmp)
    # #     tmp_stream = open(tmp,'rb')
    # number = facemodel.face_detect(face.file)
    # if (number==0 or number>1):
    #     return JSONResponse(
    #             content={
    #                 'code':422,
    #                 'data':{
                        
    #                 },
    #                 'message':'图片未检测到人脸或图片有多张人脸'
    #             }
    #         )

    ##然后进行上传到静态资源和命名上传给数据库的工作
    peanutweb="http://424z7l3858.qicp.vip"   
    suffix = Path(face.filename).suffix
    localaddress = "./assets/faces/"+uname+suffix #静态资源库地址
    fileaddress = peanutweb+"/assets/faces/"+uname+suffix #外面可以访问到的地址
    print(localaddress)

    try:
        newfile = open(localaddress,'wb') #以字节形式写入要加b
        shutil.copyfileobj(face.file,newfile) #复制文件 用newfile.write也写
        '''
        这是目前的解决方法，但是这样做必须记得下面的事项。
        ####这样做，必须变成文件流才行，而且必须要变成'rb'!!!!!!!!!!!!!!
        '''
        #可以先上传后，再检测人脸，反正一个人最多存几种格式的
        newfile = open(localaddress,'rb')
        number = facemodel.face_detect(newfile)
        if (number==0 or number>1):
            return JSONResponse(
                    content={
                        'code':422,
                        'data':{
                            
                        },
                        'message':'图片未检测到人脸或图片有多张人脸'
                    }
                )
    except Exception as e:
        print("失败",e)
    finally:
        face.file.close()
        newfile.close()
    #传给uface的只有静态资源库的命名，因为该图片信息可以不进行展示--------------------------------
    facename = uname+suffix
    userDao.updateInformationSingleByName("uface",facename,uname)
    return JSONResponse(
        content={
            'code':200,
            'data':{
                'image':fileaddress
            },
            'message':'人脸照片上传成功'
        }
    )

'''
关注相关功能
'''
def followOther(uname,uname_other):  #uname和uname_other一定是存在的，所以这里就不判断是否data为空了
    #这里统一都把id找出来
    user_data = userDao.selectUsersByName(uname)
    user_other_data = userDao.selectUsersByName(uname_other)
    user_id = user_data[0]["uid"]
    user_other_id= user_other_data[0]["uid"]
    #首先要看看关注没有
    data = userDao.selectFollowRelationship(user_id,user_other_id)
    #若关注，则取消关注------------------------------------------
    #uname的关注减去1
    data1_follow = user_data[0]["ufollow"]-1
    userDao.updateInformationSingleByName(edit_name="ufollow",edit_data=data1_follow,uname=uname)
    #uname_other的粉丝数减去1
    data2_fans = user_other_data[0]["ufans"]-1
    #user_user表的删除
    userDao.updateInformationSingleByName(edit_name="ufans",edit_data=data2_fans,uname=uname_other)
    if (data):
        userDao.deleteFollowRelationship(user_id,user_other_id)
        return JSONResponse(
        content={
            'code':200,
            'data':{
                'user_follow':data1_follow,    #先暂且这么返回吧
                'user_other_fans':data2_fans
            },
            'message':'%s取消关注%s成功'%(uname,uname_other)
        }
    )
    #若没有关注：则关注----------------------------------------
    #uname的关注增加1
    data1_follow = user_data[0]["ufollow"]+1
    userDao.updateInformationSingleByName(edit_name="ufollow",edit_data=data1_follow,uname=uname)
    #uname_other的粉丝数增加1
    data2_fans = user_other_data[0]["ufans"]+1
    userDao.updateInformationSingleByName(edit_name="ufans",edit_data=data2_fans,uname=uname_other)
    #user_user表增加映射关系------------------------------------------------------------------------只关注一次，或者再一次就取消
    userDao.insertFollowRelationship(user_id,user_other_id)
    return JSONResponse(
        content={
            'code':200,
            'data':{
                'user_follow':data1_follow,    #先暂且这么返回吧
                'user_other_fans':data2_fans
            },
            'message':'%s关注%s成功'%(uname,uname_other)
        }
    )

def selectFollow(uname):
    data = userDao.selectFollow(uname)
    return JSONResponse(
        content={
            'code':200,
            'data':{
                'users_data':data,
                'number':len(data)     
            },
            'message':'返回成功'
        }
    )
#大致和上面差不多，不过sql语句要发生变化
def selectFans(uname):
    data = userDao.selectFans(uname)
    return JSONResponse(
        content={
            'code':200,
            'data':{
                'users_data':data,
                'number':len(data)     
            },
            'message':'返回成功'
        }
    )

'''
访问他人页面
'''
def visit(uname:str,uname_other:str):
    #查找uname是否关注uname_other
    user_data = userDao.selectUsersByName(uname)
    data = user_other_data = userDao.selectUsersByName(uname_other)
    user_id = user_data[0]["uid"]
    user_other_id= user_other_data[0]["uid"]
    data_follow = userDao.selectFollowRelationship(user_id,user_other_id)
    follow=False #标识
    if (data_follow):
        follow=True
    return JSONResponse(
        content={
            'code':200,
            'data':{
                'uphoto':data[0]["uphoto"],
                'ufans':data[0]["ufans"],
                'ufollow':data[0]["ufollow"],
                'usignature':data[0]["usignature"],
                'bool_follow':follow
            },
            'message':'返回成功'
        }
    )