from fastapi import APIRouter, Depends, HTTPException, UploadFile
from middleware.authenticate import authenticate

router = APIRouter()

@router.get("/errlog")
async def errlog():    
    raise HTTPException(status_code=404, detail="资源未找到")

@router.get("/protected")
def protected_route(user: str = Depends(authenticate)):
    return {"message": "You are authorized", "user": user}