from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.models.order.detail_order_model import DetailOrderModel

from app.schemas.schemas import OrderSchema

class FinishOrderService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def fish_order(self, order_id: DetailOrderModel):
        order = self.db_session.query(OrderSchema).filter_by(id=order_id.order_id).first()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Esta orderm não existe"
            )
        
        order.status = True
        self.db_session.commit()

        return {
            "order": {
                "id": order.id,
                "table": order.table,
                "status": order.status,
                "draft": order.draft,
                "name": order.name,
                "created_at": str(order.created_at),
                "updated_at": str(order.updated_at)
            }
        }