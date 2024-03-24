from fastapi import APIRouter, HTTPException, UploadFile

router = APIRouter()

@router.get("/errlog")
async def errlog():    
    raise HTTPException(status_code=404, detail="资源未找到")