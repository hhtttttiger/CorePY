from sqlalchemy import  Column, DateTime, Integer, String
from datetime import datetime

from db.data_engine import DBBase

class ErrorLog(DBBase):
    __tablename__ = "sys_error"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    error_message = Column(String)