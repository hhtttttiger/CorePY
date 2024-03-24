import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger
from db.data_engine import SessionLocal
from db.init_table import init_table
from db.entity.sys_error import *
from routers.routers import initRouter

logger.info("服务开始启动!")
init_table()
try:
    app = FastAPI()
    pass
except Exception as e:
    logger.info(f"服务启动失败!{str(e)}")

# 启动事件
@app.on_event("startup")
async def app_start():
    # 简易的后台任务
    #asyncio.create_task(async_cron())
    logger.info("服务启动成功!")


# 路由注册
initRouter(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 简单的定时任务例子，在启动时间中用asyncio.create_task调用
async def async_cron():
    while True:
        print('执行 Async 定时任务')
        await asyncio.sleep(10)


# 定义异常处理器
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    # 将错误信息写入数据库
    db = SessionLocal()
    error_log = ErrorLog(error_message=exc.detail)
    db.add(error_log)
    db.commit()
    db.close()
    # 返回自定义的错误消息
    return JSONResponse(
        status_code= 200,
        content=jsonable_encoder({"detail": exc.detail}),
    )
