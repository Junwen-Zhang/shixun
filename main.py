# 容器
import uvicorn
# FASTAPI模板
from fastapi import FastAPI
# 注册相应的api
from api import audio,passage,admin,user,comment
# 配置跨域
from starlette.middleware.cors import CORSMiddleware
# 返回json格式的数据
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
# 配置静态资源
from fastapi.staticfiles import StaticFiles

from service import audioService

## 声明fastapi的实例
app = FastAPI()
## 配置静态资源的存放路径以及请求的路径
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
## 跨域配置
origins = ["*"]
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"])  

## 注册api模块
app.include_router(audio.router,prefix="/api/audios")
app.include_router(passage.router,prefix="/yyjsb/passage")
app.include_router(admin.router,prefix="/yyjsb/admin")
app.include_router(user.router,prefix="/yyjsb/user")
app.include_router(comment.router,prefix="/yyjsb/comment")

## 配置容器启动相应的实例
if __name__ == '__main__':
    uvicorn.run(app='main:app', port=10086,reload=True)

