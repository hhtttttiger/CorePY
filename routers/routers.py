from fastapi import FastAPI
from routers.document_reader import router as documentReaderRouter
from routers.debug import router as debugRouter

''' 
    路由从这里注册
'''

def initRouter(app: FastAPI):
    app.include_router(debugRouter, prefix="/debug")
    app.include_router(documentReaderRouter, prefix="/documentReader")