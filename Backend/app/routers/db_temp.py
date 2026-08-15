from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from Backend.app.database.dependency import get_db


router = APIRouter()


@router.get(
    "/db-test",
    summary="Test PostgreSQL database connection",
)
def database_test(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }