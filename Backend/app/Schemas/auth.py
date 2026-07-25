from pydantic import BaseModel,ConfigDict,EmailStr,Field
from Backend.app.Schemas.base_schema import BaseSchema

class UserRegisterRequest(BaseSchema):
    '''Request body validation'''
    username:str=Field(min_length=3,max_length=15,description="Unique name")
    
    Email:EmailStr
    
    password:str=Field(min_length=8,max_length=32,description="User Password")
    
    model_config=ConfigDict(extra="forbid",str_strip_whitespace=True)
    
    