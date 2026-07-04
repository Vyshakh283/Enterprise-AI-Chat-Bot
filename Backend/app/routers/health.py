from datetime import datetime,timezone
from fastapi import APIRouter


router=APIRouter()

@router.get(
    "/health",
    summary="Health")
async def Health():
    return {"msg":"Healthy"}

@router.get(
    "/live",
    summary="is live or not")
async def live():
    return {"msg":"status is live"}

@router.get(
    "/status",
    summary="ready")
async def status():
    return {"msg":"status is ready"}

