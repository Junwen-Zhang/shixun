from pydantic import BaseModel
from DateTime import DateTime
class PassageModel(BaseModel):
    pid=0
    pname="string"
    pcontent="string"
    passage_uid=0
    def __int__(self, pid, pname, pcontent,passage_uid):
        self.pid = pid
        self.pname = pname
        self.pcontent = pcontent
        self.passage_uid =passage_uid
class PassageLiking(BaseModel):
    pid=0
    wholiking_id=0

def createlist():
        plist=[]
        passageModel=PassageModel()
        for i in list(range(10)):   
            plist.append(passageModel)
        return plist
class PassageModelList(BaseModel):
    plist=createlist()

