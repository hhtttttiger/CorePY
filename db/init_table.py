from db.data_engine import engine
from db.entity.sys_error import ErrorLog
from db.entity.sys_apikey import APIKey

def init_table():
    ErrorLog.metadata.create_all(bind=engine)
    APIKey.metadata.create_all(bind=engine)