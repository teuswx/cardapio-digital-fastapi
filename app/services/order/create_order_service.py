from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException, status

from app.models.order.create_order_model import CreateOrderModel

from app.schemas.schemas import OrderSchema
class CreateOrderService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_order(self, order: CreateOrderModel):
        
       from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException, status

class CreateOrderService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_order(self, order: CreateOrderModel):
        try:
            order_model = OrderSchema(
                table=order.table,
                name=order.name
            )

            self.db_session.add(order_model)
            self.db_session.commit()

            return {
                "message": "Ordem criada com sucesso",
                "status": status.HTTP_202_ACCEPTED
            }

        except IntegrityError:
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro de integridade: dados duplicados ou inválidos."
            )

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro no banco de dados: {str(e)}"
            )
