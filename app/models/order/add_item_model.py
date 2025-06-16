from pydantic import BaseModel

class AddItemModel(BaseModel):
    order_id: int
    product_id: int
    amount: int