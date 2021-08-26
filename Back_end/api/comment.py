# 控制层————接收数据，返回数据
# 引入路由管理
from fastapi import APIRouter
import json
# 让数据以json的格式返回
from fastapi.responses import JSONResponse
from model.commentModel import CommentModel,DeleteCommentModel,NewCcontentModel,LikeModel
from service import commentService
# 构建api路由
router = APIRouter()

# 发布评论
@router.post("/createComment", tags=["comment"])
async def creatComment(comment:CommentModel):
    return commentService.createCommentInfos(comment)

# 查看个人发布的所有评论
@router.get("/searchMyComment", tags=["comment"])
async def searchMyComment(uid:int,page_id:int):
    # print(uid)
    return commentService.searchComment(uid,page_id)

# 删除个人发布的评价
@router.post("/deleteMyComment", tags=["comment"])
async def deleteMyComment(deleteComment:DeleteCommentModel):
    return commentService.deleteComment(deleteComment)

# 更改个人发布的评价
@router.post("/editMyComment", tags=["comment"])
async def deleteMyComment(newCcontent:NewCcontentModel):
    return commentService.updateComment(newCcontent)


# 查看该评论对应的原文章
@router.get("/viewPassageByComment", tags=["comment"])
async def viewPassage(comment_id:int):
    return commentService.selectPassage(comment_id)


# 查看passage_id对应的作者名字
@router.get("/getUnameByPid", tags=["comment"])
async def getUnameByPid(pid:int):
    return commentService.getUnameByPid(pid)


# 查看个人发布的某条评论
@router.get("/ViewComment", tags=["comment"])
async def viewComment(comment_id:int):
    # print(uid)
    return commentService.viewComment(comment_id)


# 更新点赞数,返回该条评论的点赞数
@router.post("/createLikes", tags=["comment"])
async def createLikes(like:LikeModel):
    return commentService.updateLike(like)


# 通过评论id查看评论者名字
@router.get("/ViewUnameByCid", tags=["comment"])
async def viewComment(comment_id:int):
    return commentService.ViewUnameByCid(comment_id)



