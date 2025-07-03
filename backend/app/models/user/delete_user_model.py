from pydantic import BaseModel

class DeleteUserModel(BaseModel):
    id: int