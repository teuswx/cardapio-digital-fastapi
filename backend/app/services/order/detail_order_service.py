from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.order.detail_order_model import DetailOrderModel

from app.schemas.schemas import ItemSchema
class DetailOrderService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def detail_order(self, order_id: DetailOrderModel):
        item = self.db_session.query(ItemSchema).filter_by(id=order_id.id).first()

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Esta ordem não foi encontrada"
            )
        
        return {
        "item":{
            "id": item.id,
            "amount": item.amount,
            "product": {
                "id": item.product.id,
                "name": item.product.name,
                "price": item.product.price,
                "description": item.product.description,
                "banner": item.product.banner,
                "category_id": item.product.category_id,
                "created_at": str(item.product.created_at),
                "updated_at": str(item.product.updated_at)
                },
            "order": {
                "id": item.order.id,
                "table": item.order.table,
                "status": item.order.status,
                "draft": item.order.draft,
                "name": item.order.name,
                "created_at": str(item.order.created_at),
                "updated_at": str(item.order.updated_at)
            }
        }
       
    }
        
        