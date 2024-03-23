from fastapi import APIRouter, HTTPException, UploadFile
from services.document_reader.reader import reader

router = APIRouter()

@router.post("/")
async def document_reader(file: UploadFile):    
    try:
        text = await reader(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"解析文档出错: {str(e)}")
    
    return {
        "result": text
    }