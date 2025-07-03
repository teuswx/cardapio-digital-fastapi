from pydantic import BaseModel

class DeleteItemModel(BaseModel):
    id: int