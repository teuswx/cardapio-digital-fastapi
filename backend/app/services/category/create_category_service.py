from sqlalchemy.orm import Session 
from app.models.category.create_category_model import CreateCategoryModel
from app.schemas.schemas import CategorySchema
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

class CreateCategoryService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_category(self, category: CreateCategoryModel):
        existing = self.db_session.query(CategorySchema).filter_by(name=category.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Categoria já existe"
            )

        category_model = CategorySchema(name=category.name)

        try:
            self.db_session.add(category_model)
            self.db_session.commit()
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao salvar no banco: {str(e)}"
            )

        return f"Categoria {category.name} criada com sucesso"
