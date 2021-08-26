from fastapi.responses import JSONResponse,Response
from dao import passageDao
from model.passageModel import PassageModel,PassageLiking,PassageModelList
from model.timeModel import DateEnconding,Enconding
from service import audioService

encond=Enconding()
dateEnconding=DateEnconding()

#----------------------------------------------------------------------------------------------------------------------
#所有文章
#----------------------------------------------------------------------------------------------------------------------
#罗列所有文章列表
def getPassages(page):
    data = passageDao.selectAllPassage(page)
    return JSONResponse(    
        content={
            "code":"200",
            'data':{
                "passage":encond.enconding(data),
            },
            "message":"数据访问成功"
        }
    )

#查询所有文章（返回所有与所查文章名一样的文章）
def searchPassage(pname:str):
    data = passageDao.selectSearchPassage(pname)

    if(len(data)==0):
        return JSONResponse(
            content={
                
                "code":"204",
                'data':{
                    "data":encond.enconding(data)
                    },
                    
                "message":"数据访问成功"
            }
        )
    else:
         return JSONResponse(
            content={
                
                "code":"200",
                'data':{
                    "data":encond.enconding(data)
                    },
                    
                "message":"数据访问成功"
            }
        )

#所有文章->单独文章内容反馈
def getPassage(pid:int):
    data = passageDao.selectChosenPassage(pid)

    return JSONResponse(
        content={
            
            "code":"200",
            'data':{
                "data":encond.enconding(data),
                },
                
            "message":"数据访问成功"
        }
    )

#----------------------------------------------------------------------------------------------------------------------
#我的文章
#----------------------------------------------------------------------------------------------------------------------

#罗列我的文章列表
def getMyPassages(uid:int,page:int):

    data = passageDao.selectMyPassage(uid,page)
    return JSONResponse(
        content={
            "code":"200",
            'data':{
                "passage":encond.enconding(data)
            },
            "message":"数据访问成功"
        }
    )

#查询我的文章
def searchMyPassage(pname:str,uid:int):

    data = passageDao.selectMySearchPassage(pname,uid)
    return JSONResponse(
        content={
            
            "code":"200",
            'data':{
                "data":encond.enconding(data)
                },
                
            "message":"数据访问成功"
        }
    )

#我的文章->单独文章内容反馈
def getMyPassage(pid:int):
    data = passageDao.selectMyChosenPassage(pid)
    return JSONResponse(
        content={
            
            "code":"200",
            'data':{
                "data":encond.enconding(data),
                },
                
            "message":"数据访问成功"
        }
    )


#发布文章
def postPassage(passageInfo:PassageModel):
    data=passageDao.insertPassage(passageInfo)
    if(data==0):
        return JSONResponse(
        content={
            "code":"200",
            "data":{
            },
            "message":"之前有人发布过完全相同的内容哦"
        }
    )
    else:
        pid=data[0]['pid']
        #audioService=AudioService()
        audioService.createAudio(passageInfo.passage_uid,passageInfo.pcontent,1,pid)
        return JSONResponse(
                content={
                    "code":"200",
                    "data":{
                        "pname":passageInfo.pname,
                        "pcontent":passageInfo.pcontent,
                    },
                    "message":"文章发布成功"
                }
        )

#修改我的文章内容
def putPassageContent(passageInfo:PassageModel):
    data=passageDao.updatePassageContent(passageInfo)
    #audioService=AudioService()
    audioService.createAudio(data[0]['uid'],passageInfo.pcontent,1,passageInfo.pid)
    return JSONResponse(
        content={
            "code":"200",
            "data":{},
            "message":"文章修改成功"
        }
    )
#修改我的文章标题
def putPassageTitle(passageInfo:PassageModel):
    passageDao.updatePassageTitle(passageInfo)
    return JSONResponse(
        content={
            "code":"200",
            "data":{},
            "message":"文章修改成功"
        }
    )

#----------------------------------------------------------------------------------------------------------------------
#公有功能
#----------------------------------------------------------------------------------------------------------------------


#查看文章评论(pid)
def getPassageComment(pid:int):
    data=passageDao.selectPassageComment(pid)
    return JSONResponse(
        content={
            "code":"200",
            "data":{
                'data':data,
                'cnt':len(data)
            },
            "message":"评论查看成功"
        }
    )

#点赞动作
def postPassageLiking(passageLiking:PassageLiking):
    data=passageDao.postPassageLiking(passageLiking)
    return JSONResponse(
        content={
            "code":"200",
            "data":{
                
            },
            "message":data
        }
    )




#------------------------------------------------------------------------------------------------------------------
#管理员和用户本人功能
#------------------------------------------------------------------------------------------------------------------  

#删除文章
def deletePassage(passageInfo:PassageModel):
    passageDao.deletePassage(passageInfo)
    return JSONResponse(
        content={
            "code":"200",
             "data":{
            },
            "message":"文章删除成功",
        }
    )

#批量删除文章
def deletePassageList(passageModelList:PassageModelList):
    for i in passageModelList.plist:
        if(i['pid']==0): break
        else:
            passageModel=PassageModel()
            passageModel.pid=i['pid']
            passageDao.deletePassage(passageModel)
    return JSONResponse(
            content={
                "code":"200",
                "data":{
                },
                "message":"文章删除成功",
            }
    )
