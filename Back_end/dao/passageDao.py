from model.passageModel import PassageModel,PassageLiking
from model.sqlModel import SqlModel
from model.commentModel import DeleteCommentModel
from dao import commentDao
import datetime
import os
sqlmodel = SqlModel()
datapath="./assets/audio/passage/"
#----------------------------------------------------------------------------------------------------------------------
#所有文章
#----------------------------------------------------------------------------------------------------------------------
#分页罗列所有文章列表
def selectAllPassage(page):  
    sqlmodel = SqlModel()
    #passage.pid,pname,ptime,pcontent,user.uname
    begin=(page-1)*4
    sql = """SELECT passage.pid,pname,ptime,pcontent,plook,user.uname,user.uid from passage 
            INNER JOIN user_passage ON passage.pid=user_passage.pid
            INNER JOIN user ON user.uid=user_passage.uid
            order by ptime desc
            limit %s,4"""%(begin)
    
    data = sqlmodel.sqlSelect(sql,get_one=False)

    addallpassageliking(data)

    return data

#查询所有文章（返回所有与所查文章名一样的文章）
def selectSearchPassage(pname:str):   
    sqlmodel = SqlModel()
    sql = """SELECT passage.pid,pname,ptime,pcontent,plook,user.uname from passage
            INNER JOIN user_passage ON passage.pid=user_passage.pid
            INNER JOIN user ON user.uid=user_passage.uid
            WHERE passage.pname LIKE '%%%s%%'
            order by ptime desc
            """%(pname)
    data = sqlmodel.sqlSelect(sql,get_one=False)

    addallpassageliking(data)

    return data

#所有文章->单独文章内容反馈
def selectChosenPassage(pid):  
    sqlmodel = SqlModel() 
    updatePassageLook(pid)  
    sql = """SELECT passage.pid,pname,ptime,pcontent,plook,user.uname from passage
            INNER JOIN user_passage ON passage.pid=user_passage.pid
            INNER JOIN user ON user.uid=user_passage.uid
            WHERE passage.pid=%s"""%(pid)
    data = sqlmodel.sqlSelect(sql,get_one=False)
    addpassageliking(data)
    return data


#----------------------------------------------------------------------------------------------------------------------
#我的文章
#----------------------------------------------------------------------------------------------------------------------

#罗列我的文章列表
def selectMyPassage(uid,page): 
    begin=(page-1)*4
    sqlmodel = SqlModel()
    sql="""  SELECT * from passage
            INNER JOIN user_passage ON passage.pid=user_passage.pid
            WHERE user_passage.uid=%s
            order by ptime desc
            limit %s,4"""%(uid,begin)
    data = sqlmodel.sqlSelect(sql,get_one=False)
    addpassageliking(data)
    return data

#查询我的文章
def selectMySearchPassage(pname:str,uid:int):  
    sqlmodel = SqlModel() 
    sql = """SELECT passage.pid,pname,ptime,pcontent,plook from passage
            INNER JOIN user_passage ON passage.pid=user_passage.pid
            INNER JOIN user ON user.uid=user_passage.uid
            WHERE user.uid=%s AND passage.pname LIKE '%%%s%%'
            order by ptime desc
            """%(uid,pname)
                
    data = sqlmodel.sqlSelect(sql,get_one=False)
    return data

#我的文章->单独文章内容反馈
def selectMyChosenPassage(pid): 
    updatePassageLook(pid)  
    sqlmodel = SqlModel()
    sql = """SELECT passage.pcontent, passage.pname,passage.ptime,plook from passage
                WHERE pid=%s"""%(pid)
    data = sqlmodel.sqlSelect(sql,get_one=False)
    addpassageliking(data)
    
    return data

    
#发布文章
def insertPassage(passageInfo:PassageModel):   
    

    sqlmodel = SqlModel()

    #判断之前是否有人写过完全相同的文章
    sql= """SELECT passage.pid from passage
             WHERE pcontent='%s'"""%(passageInfo.pcontent)
    data = sqlmodel.sqlSelect(sql,get_one=False)


    if(len(data)==0):
        sql = """INSERT INTO passage(pname,pcontent,ptime,plook)
                VALUES ('%s','%s','%s',%s)"""%(passageInfo.pname,passageInfo.pcontent,datetime.datetime.now(),0)  
        sqlmodel.sqlInsert(sql)

        sql2= """SELECT passage.pid from passage
                WHERE pcontent='%s' AND pname='%s'"""%(passageInfo.pcontent,passageInfo.pname)
        dataa = sqlmodel.sqlSelect(sql2,get_one=False)
        sql3="""INSERT INTO user_passage(pid,uid)
                VALUES ('%s','%s')"""%(dataa[0]['pid'],passageInfo.passage_uid) 
        sqlmodel.sqlInsert(sql3)
   
        return dataa
    else:
        data=0
        return 0
    


#修改我的文章内容
def updatePassageContent(passageInfo:PassageModel):
    sqlmodel = SqlModel()
    sql="""UPDATE passage set pcontent='%s'
           WHERE passage.pid=%s"""%(passageInfo.pcontent,passageInfo.pid)
    sqlmodel.sqlUpdate(sql)
    sql="""SELECT uid from user_passage
             WHERE pid=%s"""%(passageInfo.pid)
    data=sqlmodel.sqlSelect(sql,get_one=False)
    return data
#修改我的文章标题
def updatePassageTitle(passageInfo:PassageModel):

    sqlmodel = SqlModel()
    sql="""UPDATE passage set pname='%s'
           WHERE passage.pid=%s"""%(passageInfo.pname,passageInfo.pid)
    sqlmodel.sqlUpdate(sql)

#----------------------------------------------------------------------------------------------------------------------
#文章公有功能
#----------------------------------------------------------------------------------------------------------------------   
#查看文章评论
def selectPassageComment(pid:int):

    sqlmodel = SqlModel()
    sql="""SELECT comment.comment_id,ccontent,cdate,user.uname,user.uid from comment
            INNER JOIN user_comment ON user_comment.comment_id=comment.comment_id
            INNER JOIN user ON uid=user_comment.user_id
            INNER JOIN comment_passage ON comment.comment_id=comment_passage.comment_id
            INNER JOIN passage ON passage.pid=comment_passage.passage_id
            WHERE passage.pid=%s
            order by cdate desc"""%(pid)
    data=sqlmodel.sqlSelect(sql,get_one=False)
    return data
#查看文章点赞
def selectPassageLiking(pid:int):

    sqlmodel = SqlModel()
    sql="""SELECT uname,user.uid from user
            INNER Join nkxtest_user_likingpassage ON user.uid=nkxtest_user_likingpassage.uid
            INNER Join passage ON passage.pid=nkxtest_user_likingpassage.pid
            WHERE passage.pid=%s"""%(pid)
    data=sqlmodel.sqlSelect(sql,get_one=False)
    return data
#点赞操作(user_likingpassage)(只能点赞一次)
def postPassageLiking(passageLiking:PassageLiking):
    sucornot="点赞成功"
    flag=0

    sqlmodel = SqlModel()
    sql="""SELECT pid from nkxtest_user_likingpassage
             WHERE uid=%s"""%(passageLiking.wholiking_id)
    data=sqlmodel.sqlSelect(sql,get_one=False)
    for sdata in data:
        if(sdata['pid']==passageLiking.pid):
            sucornot="不能重复点赞哦"
            flag=1
    if(flag==0):
        sql="""INSERT INTO nkxtest_user_likingpassage(uid,pid)
            VALUES (%s,%s)"""%(passageLiking.wholiking_id,passageLiking.pid)
        sqlmodel.sqlInsert(sql)
    return sucornot

#添加浏览量(进入文章具体页面时调用)
def updatePassageLook(pid:int):
    sqlmodel = SqlModel()
    sql="""UPDATE passage set plook=plook+1
           WHERE passage.pid=%s"""%(pid)
    sqlmodel.sqlUpdate(sql)

#所有文章数据，没有评论内容和点赞人
def addallpassageliking(data):
    for sdata in data:
        like=selectPassageLiking(sdata['pid'])
        #sdata['who_like']=like
        sdata['like_cnt']=len(like)
        comment=selectPassageComment(sdata['pid'])
        #sdata['comment']=comment
        sdata['comment_cnt']=len(comment)
    
#data数据中添加点赞评论信息
def addpassageliking(data):
    for sdata in data:
        like=selectPassageLiking(sdata['pid'])
        sdata['who_like']=like
        sdata['like_cnt']=len(like)
        comment=selectPassageComment(sdata['pid'])
        sdata['comment']=comment
        sdata['comment_cnt']=len(comment)
    
#------------------------------------------------------------------------------------------------------------------
#管理员和用户本人功能
#------------------------------------------------------------------------------------------------------------------  
#删除文章
def deletePassage(passageInfo:PassageModel):
    sqlmodel = SqlModel()
    #删文
    sql="""DELETE FROM passage
            WHERE  passage.pid = %s"""%(passageInfo.pid)
    sqlmodel.sqlDelete(sql)


    sql="""DELETE FROM user_passage
            WHERE  pid = %s"""%(passageInfo.pid)
    sqlmodel.sqlDelete(sql)

    #删音
    filename="passage"+str(passageInfo.pid)+".mp3"
    os.remove(os.path.join(datapath,filename))

    #删评
    sql="""SELECT comment_passage.comment_id from comment_passage
           WHERE passage_id=%s"""%(passageInfo.pid)

    d=sqlmodel.sqlSelect(sql,get_one=False)

    for dictt in d: 
        deletone=DeleteCommentModel()
        deletone.comment_id=dictt['comment_id']
        commentDao.deleteComment(deletone)
    
