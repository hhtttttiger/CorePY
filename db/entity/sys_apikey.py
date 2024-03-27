from sqlalchemy import  Column, DateTime, Integer, String
from datetime import datetime

from db.data_engine import DBBase
class APIKey(DBBase):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)