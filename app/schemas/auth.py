from pydantic import BaseModel, EmailStr, constr, validator
from typing import List

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: constr(min_length=6)
    password_confirm: str

    @validator('password_confirm')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str = None

