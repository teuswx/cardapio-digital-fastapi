from pydantic import BaseModel
from fastapi import Form
class CreateProductModel(BaseModel):
    name: str
    price: str
    description: str
    banner: str
    category_id: int