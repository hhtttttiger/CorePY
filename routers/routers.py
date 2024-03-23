from fastapi import FastAPI
from routers.document_reader import router as documentReaderRouter

''' 
    路由从这里注册
'''

def initRouter(app: FastAPI):
    app.include_router(documentReaderRouter, prefix="/documentReader")