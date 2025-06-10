from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from app.schemas.schemas import UserModel

from app.models.user import User

crypt_context = CryptContext(schemes=['sha256_crypt'])

class CreateUserController:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def user_register(self, user: User):
        user_model = UserModel(
            username=user.username,
            email=user.email,
            password=crypt_context.hash(user.password),
            tipo= user.tipo
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
            return {"message": "User created successfully"}
        except IntegrityError:
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exists'
            )
