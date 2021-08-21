import uvicorn
from fastapi import FastAPI
from api import user
# from api import item
from starlette.middleware.cors import CORSMiddleware
#返回json格式的数据
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
# 配置静态资源
from fastapi.staticfiles import StaticFiles

#生命fastapi的实例
app = FastAPI()
# 配置静态资源的存放路径以及请求的路径
app.mount("/assets",StaticFiles(directory="assets"),name="assets")
# 跨域配置
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins =origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
#注册api模块
app.include_router(user.router,prefix="/api")

# 配置容器启动相应的实例
if __name__=="__main__": #除了命令行，还可以使用程序直接运行
    uvicorn.run('main:app',host='127.0.0.1',port=8000,reload=True,debug=True,workers=1) #workers：进程的数量

'''
没有服务器，就用花生壳穿透，让大家都能用：实名认证+6块钱
'''