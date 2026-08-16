from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from Backend.app.database.dependency import get_db
from Backend.app.Schemas.auth import (UserRegisterRequest,UserLoginRequest,UserResponse,TokenResponse)
from Backend.app.Services.User_service import AuthService
from Backend.app.dependency.auth import get_current_user
from Backend.app.Models.user import User


router=APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)

async def register(request:UserRegisterRequest,db:Session=Depends(get_db)):
    service=AuthService(db)
    return service.register_user(request)

'''@router.post("/login",response_model=TokenResponse)

async def login(request:UserLoginRequest,db:Session=Depends(get_db)):
    service=AuthService(db)
    return service.authenticate_user(request)'''

@router.get("/me")

async def get_my_profile(current_user:User=Depends(get_current_user)):
    return{ "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "department": current_user.department,
        "is_active": current_user.is_active,
    }

@router.post("/oauth2-login", response_model=TokenResponse)

async def oauth2_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    request = UserLoginRequest(
        email=form_data.username,
        password=form_data.password,
    )

    return service.authenticate_user(request)
    
    
    
