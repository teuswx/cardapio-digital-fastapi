from pydantic import BaseModel

class CreateCategoryModel(BaseModel):
    name: str