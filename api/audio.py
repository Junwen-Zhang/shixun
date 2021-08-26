#引入路由管理
from fastapi import APIRouter,UploadFile,File,Request,Body,Form
#让数据以json格式返回所用到的库
from fastapi.responses import JSONResponse,Response
from service import audioService
from model.audioModel import AudioModel

router = APIRouter()
'''
这一块就是fastapi的核心，事例
'''

@router.post("/listentest", tags=["audios"])  #请求体格式
async def audio(audioInfo:AudioModel):
     return audioService.audioListentest(audioInfo)

@router.post("/saveaudioparameters", tags=["audios"])  #请求体格式
async def audio(audioInfo:AudioModel):
     return audioService.setAudio(audioInfo)