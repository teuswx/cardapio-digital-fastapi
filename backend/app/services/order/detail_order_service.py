from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.order.detail_order_model import DetailOrderModel

from app.schemas.schemas import ItemSchema
class DetailOrderService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def detail_order(self, order_id: int):
        item = self.db_session.query(ItemSchema).filter_by(id=order_id).first()

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Esta ordem não foi encontrada"
            )
        
        return {
            "id": item.id,
            "amount": item.amount,
            "created_at": str(item.created_at),
            "order_id": item.order_id,
            "product_id": item.product_id,
            "product": {
                "id": item.product.id,
                "name": item.product.name,
                "price": item.product.price,
                "description": item.product.description,
                "banner": item.product.banner,
                "category_id": item.product.category_id,
                },
            "order": {
                "id": item.order.id,
                "table": item.order.table,
                "name": item.order.name,
                "draft": item.order.draft,
                "status": item.order.status

            }
        }
    
    
        
        