import asyncio
from fastapi import FastAPI
from loguru import logger

from routers.routers import initRouter

logger.info("服务开始启动!")
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

