from pydantic import BaseModel

class CreateOrderModel(BaseModel):
    table: int
    name: str