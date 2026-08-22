from fastapi import APIRouter,UploadFile,File,Depends
from Backend.app.dependency.auth import get_current_user
from Backend.app.Models.user import User

router=APIRouter(prefix="/documents",
                tags=["Documents"])

@router.post("/upload")
async def upload_document(file:UploadFile,current_user:User=Depends(get_current_user)):
    return{ "filename": file.filename,
        "content_type": file.content_type,
        "user_id": current_user.id,
           }









