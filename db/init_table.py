from db.data_engine import engine
from db.entity.sys_error import ErrorLog

def init_table():
    ErrorLog.metadata.create_all(bind=engine)