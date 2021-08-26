from fastapi import APIRouter
from fastapi.responses import JSONResponse
from model.passageModel import PassageModel,PassageLiking,PassageModelList
from service import passageService
from typing import Optional
router = APIRouter()

#----------------------------------------------------------------------------------------------------------------------
#所有文章
#----------------------------------------------------------------------------------------------------------------------

#罗列所有文章列表
@router.get("/getpassages", tags=["passage_all"]) 
async def getPassages():
    # 通过调用相应的服务得到对应的反馈
    return passageService.getPassages()


#查询所有文章（返回所有与所查文章名一样的文章）
@router.get("/getpassages/getpassage", tags=["passage_all"])
async def searchPassage(pname:str):
    return passageService.searchPassage(pname)

#所有文章->单独文章内容反馈
@router.get("/getpassages/getpassage/{pname}/{pid}", tags=["passage_all"])
async def getPassage(pname:str,pid:int):
    return passageService.getPassage(pid)


#----------------------------------------------------------------------------------------------------------------------
#我的文章
#----------------------------------------------------------------------------------------------------------------------

#罗列我的文章列表
@router.get("/getmypassages", tags=["passage_my"]) 
async def getMyPassages(uid:int):
    return passageService.getMyPassages(uid)

#查询我的文章
@router.get("/getmypassages/getmypassage", tags=["passage_my"])
async def searchMyPassage(pname:str,uid:int):
    return passageService.searchMyPassage(pname,uid)

#我的文章->单独文章内容反馈
@router.get("/getmypassages/getmypassage/{pname}/{pid}", tags=["passage_my"])
async def getMyPassage(pname:str,pid:int):
    return passageService.getPassage(pid)

#删除我的文章
@router.delete("/getmypassages/", tags=["passage_my"])
async def deleteMyPassage(passageInfo:PassageModel):
    return passageService.deletePassage(passageInfo)

#发布文章
@router.post("/createpassage/", tags=["passage_my"])
async def postPassage(passageInfo:PassageModel):
     return passageService.postPassage(passageInfo)

#修改我的文章内容
@router.put("/getmypassages/getmypassage/content",tags=["passage_my"])
async def putPassageContent(passageInfo:PassageModel):
     return passageService.putPassageContent(passageInfo)

#修改我的文章标题
@router.put("/getmypassages/getmypassage/title",tags=["passage_my"])
async def putPassageTitle(passageInfo:PassageModel):
     return passageService.putPassageTitle(passageInfo)

#------------------------------------------------------------------------------------------------------------------
#公有功能
#------------------------------------------------------------------------------------------------------------------    
#查看文章评论(pid)
@router.get("/passages/passage/comments/{pname}/{pid}",tags=["passage_common"])
async def getPassageComment(pname:str,pid:int):
     return passageService.getPassageComment(pid)

#点赞(uid,pid)
@router.post("/passages/passage/liking", tags=["passage_common"])
async def postPassageLiking(passageLiking:PassageLiking):
     return passageService.postPassageLiking(passageLiking)
#------------------------------------------------------------------------------------------------------------------
#管理员功能
#------------------------------------------------------------------------------------------------------------------  
#管理员删除文章
@router.delete("/getpassages/", tags=["passage_administrators"])
async def deletePassage(passageInfo:PassageModel):
    return passageService.deletePassage(passageInfo)
#批量删文章
@router.delete("/getpassages/deleteList", tags=["passage_new"])
async def deletePassageList(passageModelList:PassageModelList):
    return passageService.deletePassageList(passageModelList)
