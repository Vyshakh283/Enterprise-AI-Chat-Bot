from sqlalchemy.orm import Session
from datetime import datetime, timezone
from fastapi import FastAPI,HTTPException,status

from Backend.app.Models.user import User
# function not created
# from Backend.app.repositories.User_repository import Us
from Backend.app.Schemas.auth import UserRegisterRequest,UserLoginRequest,TokenResponse

from Backend.app.core.security import (hash_password,verify_password,jwt_Token_creation,decode_access_token)

from Backend.app.repositories.user_repository import UserRepository

class AuthService :
    def __init__(self, db: Session):
        self.userrepository=UserRepository(db)
        
    def register_user(
        self,
        request: UserRegisterRequest,
    ) -> User:

        # Check email already exists
        existing_user = self.userrepository.get_by_email(request.Email)

        if existing_user:
            raise ValueError("Email already exists")

        # Hash password
        hashed_password = hash_password(request.password)

        # Create user object
        user = User(
            username=request.username,
            email=request.Email,
            hashed_password=hashed_password,
        )
        return self.userrepository.create(user)
    
    def authenticate_user(
        self,
        request: UserLoginRequest,
    ) -> TokenResponse:

        # Find user
        user = self.userrepository.get_by_email(
            request.email
        )

        # User doesn't exist
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Check locked account
        if user.is_locked:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is locked",
            )

        # Check inactive account
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        # Verify password
        password_valid = verify_password(
            request.password,
            user.hashed_password,
        )

        # Wrong password
        if not password_valid:

            user.failed_login_attempts += 1

            self.userrepository.update(user)

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Successful login
        user.failed_login_attempts = 0

        user.last_login = datetime.now(timezone.utc)

        self.userrepository.update(user)

        # JWT payload
        token_data = {
            "sub": str(user.id),
        }

        # Create access token
        access_token = jwt_Token_creation(
            token_data
        )

        # Return response
        return TokenResponse(
            access_token=access_token,
            token_type="Bearer",
        )

    def create_access_token(
        self,
        user: User
    ) -> str:

        payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }

        return jwt_Token_creation(payload)

    def verify_access_token(
        self,
        token: str,
    ) -> dict:

        payload = decode_access_token(token)

        return payload


        
    
