from model.commentModel import CommentModel,DeleteCommentModel,NewCcontentModel,LikeModel
from fastapi.responses import JSONResponse
from dao import commentDao
from service import audioService
# import audioService
import time

# 创建评论信息
def createCommentInfos(comment:CommentModel):
    comment.cdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    comment_id = commentDao.insertComment(comment)
    url = audioService.createAudio(comment.user_id,comment.ccontent,2,comment_id)
    return JSONResponse(
        content={
            "code": "200",
            "data": {
                "date": comment.cdate,
                "comment_id": comment_id,        # 需要数据库返回id
                "content": comment.ccontent,
                "passage_id": comment.passage_id,
                "music_url":url
            },
            "message": "评论发布成功"
        }
    )

# 查看个人发布的评论
def searchComment(user_id:int):
    ccontent_list = commentDao.selectComment(user_id)
    return ccontent_list

# 删评
def deleteComment(deleteComment:DeleteCommentModel):
    commentDao.deleteComment(deleteComment)
    return JSONResponse(
        content={
            "code": "200",
            "data": {
            },
            "message": "评论删除成功"
        }
    )
# 改评
def updateComment(newCcontent:NewCcontentModel):
    commentDao.updateComment(newCcontent)
    user_id = commentDao.selectUidByComment(newCcontent.comment_id)
    url = audioService.createAudio(user_id, newCcontent.new_ccontent, 2, newCcontent.comment_id)
    return JSONResponse(
        content={
            "code": "200",
            "data": {
            },
            "message": "评论修改成功"
        }
    )


# 查看该评论对应的文章
def selectPassage(comment_id:int):
    res = commentDao.selectPassage(comment_id)
    # print("res:",res)
    return res
# 查看passage_id对应的作者名字
def getUnameByPid(passage_id:int):
    res = commentDao.selectUnameByPid(passage_id)
    return res


# 查看评论的的具体信息
def viewComment(comment_id:int):
    return commentDao.selectOneComment(comment_id)


# 更新评论的点赞数
def updateLike(like:LikeModel):
    return commentDao.updateLike(like)


# 通过评论id查看评论者名字
def ViewUnameByCid(comment_id:int):
    return commentDao.selectUnameByCid(comment_id)

