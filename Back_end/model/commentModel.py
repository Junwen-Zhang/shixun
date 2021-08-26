from pydantic import BaseModel


class CommentModel(BaseModel):
    passage_id: int  # 文章的id
    user_id: int  # 评论者的id
    ccontent:str  # 评论的内容
    cdate:str    # 评论的时间
    def __int__(self, passage_id, user_uid, ccontent):
        self.passage_id = passage_id
        self.user_uid = user_uid
        self.ccontent = ccontent
        self.date = ''

# 用于接收“删除评论信息”的类
class DeleteCommentModel(BaseModel):
    comment_id:int
    def __int__(self,comment_id):
        self.comment_id = comment_id

# 用于接收“修改评论信息”的类
class NewCcontentModel(BaseModel):
    comment_id: int        # 评论所属的用户id
    new_ccontent : str
    def __int__(self,comment_id, new_ccontent):
        self.comment_id = comment_id
        self.new_ccontent=new_ccontent

# 用于接收“点赞”的类
class LikeModel(BaseModel):
    user_id:int
    comment_id:int
    def __int__(self,user_id, comment_id):
        self.user_id = user_id
        self.comment_id = comment_id