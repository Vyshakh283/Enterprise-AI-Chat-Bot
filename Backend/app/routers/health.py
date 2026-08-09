from fastapi import APIRouter


router=APIRouter(prefix="/health")

@router.get("")
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

