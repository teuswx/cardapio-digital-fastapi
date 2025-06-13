from pydantic import BaseModel

class LoginUserModel(BaseModel):
    username: str
    password: str

