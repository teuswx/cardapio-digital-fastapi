from pydantic import BaseModel

class DetailOrderModel(BaseModel):
    order_id: int