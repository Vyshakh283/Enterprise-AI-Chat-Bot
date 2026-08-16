from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from Backend.app.database.dependency import get_db
from Backend.app.Schemas.auth import (UserRegisterRequest,UserLoginRequest,UserResponse,TokenResponse)
from Backend.app.Services.User_service import AuthService
from Backend.app.de

router=APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)

async def register(request:UserRegisterRequest,db:Session=Depends(get_db)):
    service=AuthService(db)
    return service.register_user(request)

@router.post("/login",response_model=TokenResponse)

async def login(request:UserLoginRequest,db:Session=Depends(get_db)):
    service=AuthService(db)
    return service.authenticate_user(request)

@router.get("/me")

async def get_my_profile(currentuser:user=Depends(current))

    
    
    
    
