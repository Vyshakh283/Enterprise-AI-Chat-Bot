from pydantic import BaseModel,ConfigDict,EmailStr,Field
from Backend.app.Schemas.base_schema import BaseSchema

class UserRegisterRequest(BaseSchema):
    '''Request body validation'''
    username:str=Field(min_length=3,max_length=15,description="Unique name")
    
    Email:EmailStr
    
    password:str=Field(min_length=8,max_length=32,description="User Password")
    
    model_config=ConfigDict(extra="forbid",str_strip_whitespace=True)
    
class UserLoginRequest(BaseSchema):
     """
     Request body for user login.
     """
     email: EmailStr

     password: str


class TokenResponse(BaseSchema):
    """
    JWT access token returned after authentication.
    """

    access_token: str

    token_type: str = "Bearer"


class UserResponse(BaseSchema):
    """
    User information returned to the client.
    """

    id: int

    username: str

    email: EmailStr
    
    