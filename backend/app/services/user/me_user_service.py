from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.schemas import UserSchema

class MeUserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def me_user(self, user_id: int):  # Agora recebe um user_id como inteiro
        user = self.db_session.query(UserSchema).filter_by(id=user_id).first()  # Usando o user_id diretamente
        
        print(user)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "tipo": user.tipo
        }

