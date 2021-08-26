# 数据持久化  方法名前缀 insert update select delete
import time
from model.commentModel import CommentModel,DeleteCommentModel,NewCcontentModel,LikeModel
from model.sqlModel import SqlModel


# 增加一条评论，返回该评论的id
def insertComment(commentModel:CommentModel):
    sqlmodel = SqlModel()
    # 对评论内容id和评论内容表 添加数据，评论内容id自增
    sql = """INSERT INTO comment(cdate,ccontent,like_number)  
                VALUES 
                ('%s','%s',"%d")
                """%(commentModel.cdate,commentModel.ccontent, 0)
    comment_id = sqlmodel.sqlInsert(sql)

    # 对评论者id和评论内容id表 添加数据
    sql = """INSERT INTO user_comment(user_id,comment_id)
                VALUES
                ('%d','%d')
                    """%(commentModel.user_id,comment_id)
    sqlmodel.sqlInsert(sql)

    # 对评论内容id和原文章id表 添加数据
    sql = """INSERT INTO comment_passage(comment_id,passage_id)
                VALUES
                ('%d','%d')
                    """%(comment_id, commentModel.passage_id)
    sqlmodel.sqlInsert(sql)
    return comment_id


# 由用户id来查看该用户所发表的评论内容的id,返回一个“评论内容id-时间-评论内容”的集合
def selectComment(uid:int):
    sqlmodel = SqlModel()
    sql = """SELECT * FROM user_comment
            WHERE user_id='%d'
            """ % (uid)
    uid_commentid_list = sqlmodel.sqlSelect(sql,False)
    ccontent_list=[]
    for row in uid_commentid_list:
        commentid = row['comment_id']            # row
        sql = """SELECT * FROM comment
            WHERE comment_id='%d'
            """ % (commentid)
        temp = sqlmodel.sqlSelect(sql, True)
        ccontent_list.append(temp)
    return ccontent_list

# 删除评论
def deleteComment(deleteComment:DeleteCommentModel):
    sqlmodel = SqlModel()
    sql = '''DELETE FROM comment
                WHERE comment_id='%d'
                ''' % (deleteComment.comment_id)
    sqlmodel.sqlDelete(sql)

    sql = '''DELETE FROM user_comment
            WHERE comment_id='%d'
            '''%(deleteComment.comment_id)
    sqlmodel.sqlDelete(sql)

    sql = '''DELETE FROM comment_passage
                WHERE comment_id='%d'
                ''' % (deleteComment.comment_id)
    sqlmodel.sqlDelete(sql)

    # 将点赞记录中关于该评论的记录全部删除
    sql = '''DELETE FROM `like`
                    WHERE comment_id = '%d'
            ''' % (deleteComment.comment_id)
    sqlmodel.sqlDelete(sql)


# 修改评论
def updateComment(newCcontent:NewCcontentModel):
    sqlmodel = SqlModel()
    sql = '''UPDATE comment set cdate='%s',ccontent='%s'
            WHERE comment_id='%d'
            '''%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),newCcontent.new_ccontent, newCcontent.comment_id)
    sqlmodel.sqlUpdate(sql)


# 查看评论对应的文章
def selectPassage(cid:int):
    sqlmodel = SqlModel()
    sql = """SELECT * FROM comment_passage
            WHERE comment_id='%d'
            """ % (cid)
    temp = sqlmodel.sqlSelect(sql, True)

    passage_id = temp['passage_id']

    sql = """SELECT * FROM passage
                WHERE pid='%d'
                """ % (passage_id)
    temp2 = sqlmodel.sqlSelect(sql, True)

    return temp2
# 查看passage_id对应的作者名字
def selectUnameByPid(passage_id:int):
    sqlmodel = SqlModel()
    sql = """SELECT * FROM user_passage
                    WHERE pid='%d'
                    """ % (passage_id)
    temp = sqlmodel.sqlSelect(sql, True)
    uid = temp['uid']
    sql = """SELECT * FROM user
                    WHERE uid='%d'
                        """ % (uid)
    temp = sqlmodel.sqlSelect(sql, True)
    return temp['uname']


# 点击某个评论查看详情
def selectOneComment(cid:int):
    sqlmodel = SqlModel()
    sql = '''SELECT * FROM comment
            WHERE comment_id='%d'
        ''' % (cid)
    return sqlmodel.sqlSelect(sql, True)


def updateLike(like:LikeModel):
    sqlmodel = SqlModel()
    sql = '''SELECT * FROM `like`
             WHERE user_id='%d' and comment_id = '%d'
             '''%(like.user_id, like.comment_id)
    temp = sqlmodel.sqlSelect(sql,True)
    # print(temp)
    message = ""
    if temp == None:   # 如果在like表(某用户对某评论的点赞记录，每个赞都有记录)里面没有该记录，说明该用户之前未给该评论点过赞,
        # 就执行插入点赞记录
        sql = """INSERT INTO `like`(user_id, comment_id)  
                VALUES 
                ('%d','%d')
                """ %(like.user_id, like.comment_id)
        sqlmodel.sqlInsert(sql)
        # 执行该评论点赞数+1
        sql = '''UPDATE comment set like_number = like_number+1
        WHERE comment_id = '%d'
        ''' %(like.comment_id)
        sqlmodel.sqlUpdate(sql)
        message = "点赞成功"
    else:  #  该用户已对该评论点过赞，则什么都不做,直接返回点赞数
        message = "只能点赞一次哦"
    return message


def selectUnameByCid(cid:int):
    sqlmodel = SqlModel()
    sql = '''SELECT * FROM user_comment
                 WHERE comment_id = '%d'
            ''' % (cid)
    uid_cid = sqlmodel.sqlSelect(sql, True)
    user_id = uid_cid['user_id']
    sql = '''SELECT * FROM `user`
                     WHERE uid = '%d'
                ''' % (user_id)
    uid_uname = sqlmodel.sqlSelect(sql, True)
    uname = uid_uname['uname']
    return uname

def selectUidByComment(cid:int):
    sqlmodel = SqlModel()
    sql = '''SELECT * FROM user_comment
                     WHERE comment_id = '%d'
                ''' % (cid)
    uid_cid = sqlmodel.sqlSelect(sql, True)
    user_id = uid_cid['user_id']
    return user_id

