from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from decouple import config
from passlib.context import CryptContext

from app.models.user.login_user_model import LoginUserModel
from app.schemas.schemas import UserSchema


SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
crypt_context = CryptContext(schemes=['sha256_crypt'])

class AuthUserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def user_login(self, user: LoginUserModel, expires_in: int = 30):
        user_on_db = self.db_session.query(UserSchema).filter_by(username=user.username).first()
        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )

        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )

        expiration = datetime.now(timezone.utc) + timedelta(minutes=expires_in)
        payload = {
            'sub': user.username,
            'exp': expiration,
            'tipo': user_on_db.tipo,
            'id': user_on_db.id
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        expiration_str = expiration.isoformat()
        return {
            'token': access_token,
            'expiration': expiration_str,
        }

    