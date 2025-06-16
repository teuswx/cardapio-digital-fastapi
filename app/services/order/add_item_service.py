from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException, status

from app.models.order.add_item_model import AddItemModel

from app.schemas.schemas import ItemSchema
class AddItemService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_item(self, item: AddItemModel):
    
        try:
            order_model = ItemSchema(
                order_id=item.order_id,
                product_id=item.product_id,
                amount=item.amount
            )

            self.db_session.add(order_model)
            self.db_session.commit()

            return {
                "message": "Item adicionado com sucesso",
                "item": {
                    "id": order_model.id,
                    "order_id": order_model.order_id,
                    "product_id": order_model.product_id,
                    "amount": order_model.amount
                }
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