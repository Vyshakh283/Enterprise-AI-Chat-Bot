from sqlalchemy.orm import Session

from Backend.app.Models.user import User
# function not created
# from Backend.app.repositories.User_repository import Us
from Backend.app.Schemas.auth import UserRegisterRequest,UserResponse,UserLoginRequest

from Backend.app.core.security import hash_password,verify_password,jwt_Token_creation,decode_access_token

class AuthService :
    def register_user(
        self,
        db: Session,
        request: UserRegisterRequest,
    ) -> User:

        # Check email already exists
        existing_user = (
            db.query(User).filter(User.email == request.Email).first()
        )

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

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def authenticate_user(
        self,
        db: Session,
        request: UserLoginRequest,
    ) -> str:

        user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(
            request.password,
            user.hashed_password):
            raise ValueError("Invalid credentials")

        return self.create_access_token(user)

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


auth_service = AuthService()
        
    
