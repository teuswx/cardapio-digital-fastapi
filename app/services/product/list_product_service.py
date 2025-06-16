from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.schemas import ProductSchema

class ListProductService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def list_product(self):
        products = self.db_session.query(ProductSchema).all()

        if not products:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Não existe produtos cadastrados",
                    "status": status.HTTP_404_NOT_FOUND
                }
            )
        
        return[
            {
                "id": p.id,
                "name": p.name,
                "price":p.price,
                "description":p.description,
                "banner":p.banner,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "updated_at": p.updated_at.isoformat() if p.updated_at else None
            }
            for p in products
        ]