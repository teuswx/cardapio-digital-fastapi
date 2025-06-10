from sqlalchemy.orm import Session
from app.schemas.schemas import UserModel
from fastapi import HTTPException, status

class ListUserController:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def list_user(self):
        usuarios = self.db_session.query(UserModel.id, UserModel.username, UserModel.email, UserModel.tipo).all()
        
        if not usuarios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No users found in the database"
            )
        
        usuario_data = [{"id": usuario.id, "username": usuario.username, "email": usuario.email, "tipo": usuario.tipo} for usuario in usuarios]
        
        return {'Usuarios': usuario_data}
