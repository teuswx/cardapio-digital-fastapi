from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.models.order.detail_order_model import DetailOrderModel

from app.schemas.schemas import OrderSchema
class DeleteOrderService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def delete_order(self, order_id: DetailOrderModel):
        order = self.db_session.query(OrderSchema).filter_by(id=order_id.id).first()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Esta ordem não existe"
            )
        
        self.db_session.delete(order)
        self.db_session.commit()

        return JSONResponse(
            content={
                "message": "Ordem deletada com sucesso!",
            },
            status_code=status.HTTP_200_OK
        )
        
