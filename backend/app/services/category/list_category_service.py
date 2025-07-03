from sqlalchemy.orm import Session
from app.schemas.schemas import CategorySchema
from fastapi import HTTPException, status
class ListCategoryService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def list_categories(self):
        categories = self.db_session.query(CategorySchema).all()

        if not categories:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Não existe categorias cadastradas",
                    "status": status.HTTP_404_NOT_FOUND
                }
            )
        
        return[
            {
                "id": c.id,
                "name": c.name,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "updated_at": c.updated_at.isoformat() if c.updated_at else None
            }
            for c in categories
        ]
  
