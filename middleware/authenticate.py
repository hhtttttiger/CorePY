from fastapi import HTTPException, Header, status
from db.data_engine import SessionLocal
from db.entity.sys_apikey import APIKey


def authenticate(api_key: str = Header(...)):
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key is required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db = SessionLocal()
    db_api_key = db.query(APIKey).filter(APIKey.key == api_key).first()
    if db_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True
