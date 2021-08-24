from pydantic import BaseModel
class AudioModel(BaseModel):
    tex:str  #文本内容
    spd:int  #语调
    pit:int  #音调
    vol:int  #音量
    per:int  #发音人
    uid:int=None   #用户id