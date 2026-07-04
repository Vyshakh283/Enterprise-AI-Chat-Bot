from passlib.context import CryptContext
from typing import Any
from datetime import datetime,timedelta,timezone
from jose import JWTError,jwt
from Backend.app.core.configure import settings

# password hashing
# password verification
# encoding
# -------Future implements--------
# jwt creation
# jwt token validation
# OAuth2 configuration
# API key validation

pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
# password hashing
def hash_password(password:str)-> str :
    
# plain text to secured hash psw
    
    return pwd_context.hash(password)

 # verify the DB_password and user password
def verify_password(password:str,hash_password:str)-> bool :
    return pwd_context.verify(password,hash_password)

 # after verification jwt token creation
def jwt_Token_creation( data:dict[str,Any],expires_delta:timedelta | None=None,)->str:
    
    payload=data.copy()
    
    now = datetime.now(timezone.utc)

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    payload.update({"exp": expire})
        
    encoded_jwt=jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    
    return encoded_jwt

# Decode and validate a JWT.
def decode_access_token(token: str,) -> dict[str, Any]:
    
    payload=jwt.decode(token,
                       settings.JWT_SECRET_KEY,
                       algorithms=[settings.JWT_ALGORITHM])
    return payload
    
    