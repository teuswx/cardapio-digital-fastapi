from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.models.order.delete_item_model import DeleteItemModel

from app.schemas.schemas import ItemSchema

class DeleteItemService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def delete_item(self, item_id: DeleteItemModel):
        item = self.db_session.query(ItemSchema).filter_by(id=item_id.id).first()

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Este item não existe"
            )
        
        self.db_session.delete(item)
        self.db_session.commit()

        return JSONResponse(
            content={
                "message": "Item deletado com sucesso!",
            },
            status_code=status.HTTP_200_OK
        )