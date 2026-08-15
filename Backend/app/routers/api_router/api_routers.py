from fastapi import APIRouter
from Backend.app.routers.health import router as health_router
from Backend.app.routers.auth import router as authorization_router
from Backend.app.routers.db_temp import router as Db_Test


api_router=APIRouter()

api_router.include_router(health_router)
api_router.include_router(authorization_router)
api_router.include_router(Db_Test)


