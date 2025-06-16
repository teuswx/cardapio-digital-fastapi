from sqlalchemy.orm import Session
from fastapi import HTTPException, status


from app.schemas.schemas import OrderSchema


class ListOrderService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def list_order(self):
        orders = self.db_session.query(OrderSchema).all()

        if not orders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Não existe ordens cadastradas",
                    "status": status.HTTP_404_NOT_FOUND
                }
            )
        
    
        return{
            "ordens: ":
            [
                {
                    "id": o.id,
                    "name":o.name,
                    "status":o.status,
                    "draft": o.draft,
                    "table":o.table,
                    "created_at": o.created_at.isoformat() if o.created_at else None,
                    "updated_at": o.updated_at.isoformat() if o.updated_at else None
                }
                for o in orders
            ]
        }
