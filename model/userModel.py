from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile,File
# from datetime import date
class UserModel(BaseModel):
    uname:str
    upasswd:str   
    uemail:str  #前三个属性是必须的，在用户注册那里就是必须了的。 修改属性那里也总是必须有的
    uage: Optional[str]=None
    usex:Optional[str]=None
    uphone:Optional[str]=None
    usignature:Optional[str]=None
    ubirth:Optional[str]=None
    aspeed:Optional[int]=5
    apit:Optional[int]=5
    avol:Optional[int]=5
    aper:Optional[int]=0
# class PhotoModel(BaseModel):
#     uname:str
#     photofile:UploadFile = File(...) #这是错误的！！！！！！！，不能和UploadFile兼容
    