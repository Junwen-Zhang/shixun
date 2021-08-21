from pydantic import BaseModel
class UserModel(BaseModel):
    sname:str
    password:str