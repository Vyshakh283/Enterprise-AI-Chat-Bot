from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from Backend.app.database.dependency import get_db
from Backend.app.dependency.auth import get_current_user
from Backend.app.Models.user import User
from Backend.app.Services.document_service import DocumentService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = DocumentService(db)

    document = service.upload_document(
        file=file,
        user_id=current_user.id,
    )

    return {
        "id": document.id,
        "filename": document.filename,
        "content_type": document.file_type,
        "file_path": document.file_path,
        "user_id": document.user_id,
    }