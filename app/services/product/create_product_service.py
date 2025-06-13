from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.models.product.create_product_model import CreateProductModel

from app.schemas.schemas import ProductSchema

class CreateProductService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_product(self, product: CreateProductModel):
        exist = self.db_session.query(ProductSchema).filter_by(name = product.name).first()

        if exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail= "Produto já existe"
            )
        
        product_model = ProductSchema(
            name= product.name,
            price = product.price,
            description = product.description,
            banner = product.banner
        ) 

        try:
            self.db_session.add(product_model)
            self.db_session.commit()
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao salvar no banco: {str(e)}"
            )

        return {"message": f"Produto criado com sucesso"}