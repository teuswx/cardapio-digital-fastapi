import re
from pydantic import BaseModel, field_validator, EmailStr

class CreateUserModel(BaseModel):
    username: str
    email: EmailStr
    password: str
    tipo: str

    @field_validator('username')
    def validate_username(cls, value):
        if not re.match(r'^[a-zA-Z0-9@]+$', value):
            raise ValueError('Username format invalid')
        return value
