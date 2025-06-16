from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.order.detail_order_model import DetailOrderModel

from app.schemas.schemas import OrderSchema

class SendOrderService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def send_order(self, order_id: DetailOrderModel):
        order = self.db_session.query(OrderSchema).filter_by(id=order_id.id).first()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não existe esta ordem no banco de dados"
            )
        
        order.draft = False

        self.db_session.commit()

        return {
                "message": "Item adicionado com sucesso",
                "order": {
                    "id": order.id,
                    "table": order.table,
                    "status": order.status,
                    "draft": order.draft,
                    "name": order.name
                }
            }