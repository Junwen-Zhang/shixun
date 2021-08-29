from fastapi.responses import JSONResponse,Response
from fastapi import Request,File,UploadFile,Body,Form
from model.audioModel import AudioModel
import hashlib
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from tempfile import NamedTemporaryFile
import shutil
import os
from aip import AipSpeech
from dao import audioDao  

BASE_DIR = Path(__file__).resolve().parent

path="http://424z7l3858.qicp.vip"


#内部调用百度语音合成的接口，生成mp3文件
def baiduApi(tex='1111',spd=5,pit=5,vol=5,per=4,urlpath="./assets/listentest_temp.mp3"):
    APP_ID = '24728077'
    API_KEY = 'quVd2saw3uNmMXlo7Bygq4WO'
    SECRET_KEY = 'F2IaA0N6k6GIWLCxN45Od53PQmdctCwl'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result  = client.synthesis(tex, 'zh', 1, {
        'vol': vol,
        'spd':spd,
        'pit':pit,
        'per':per
    })
    print("试听文件的语音设置：",spd,pit,vol,per)
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(urlpath, 'wb') as f:
            f.write(result)
        print(tex)
        print(spd,pit,vol,per)
        print("语音文件生成成功:",urlpath)
        return True
    else:
        print(dict)
        print(tex)
        print(spd,pit,vol,per)
        print("语音文件生成失败:",urlpath)
        return False



## 生成文章和生成评论时,调用的函数
## [nkx,lqq直接调这个,pcmark为1是文章,2是评论,返回的是mp3的url]
def createAudio(uid,tex,pcmark,pcid):
    if pcmark==1:   #发表文章
        relativepath="/assets/audio/passage/passage"+str(pcid)+".mp3"
    elif pcmark==2:   #发表评论
        relativepath="/assets/audio/comment/comment"+str(pcid)+".mp3"

    spd,pid,vol,per=audioDao.search_audioinfo(uid)

    baiduApi(tex,spd,pid,vol,per,"."+relativepath)

    return path+relativepath



    
# 试听功能的服务层
def audioListentest(audioInfo:AudioModel):

    if baiduApi(audioInfo.tex,audioInfo.spd,audioInfo.pit,audioInfo.vol,audioInfo.per):
        return JSONResponse(
                content={
                    "code":"200",
                    "data":{
                        ## 这里注意合代码的时候改路径
                        "audiopath":path+"/assets/listentest_temp.mp3",
                    },
                    "message":"试听文件生成成功！"
                }
            )
    else:
        return JSONResponse(
            content={
                "code":"300",
                "data":{
                },
                "message":"试听文件生成失败！"
            }
        )

def setAudio(audioInfo:AudioModel):
    audioDao.updateAudioinfo(audioInfo.spd,audioInfo.pit,audioInfo.vol,audioInfo.per,audioInfo.uid)
    print("更新的语音设置：",audioInfo.spd,audioInfo.pit,audioInfo.vol,audioInfo.per,audioInfo.uid)
    return JSONResponse(
                content={
                    "code":"200",
                    "data":{
                        'uid':audioInfo.uid
                    },
                    "message":"语音设置成功!"
                }
            )
