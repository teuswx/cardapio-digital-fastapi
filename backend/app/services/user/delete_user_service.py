from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user.delete_user_model import DeleteUserModel
from app.schemas.schemas import UserSchema

class DeleteUserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def delete_user(self, user_id: DeleteUserModel):
        user = self.db_session.query(UserSchema).filter_by(id=user_id.id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Usuário não encontrado",
                    "status": status.HTTP_404_NOT_FOUND
                }
            )
        
        self.db_session.delete(user)
        self.db_session.commit()

        return "Usuário deletado com sucesso!"
