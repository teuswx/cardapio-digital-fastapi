from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from decouple import config
from passlib.context import CryptContext

from app.models.userLogin import UserLogin
from app.schemas.schemas import UserModel


SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
crypt_context = CryptContext(schemes=['sha256_crypt'])

class AuthUserController:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def user_login(self, user: UserLogin, expires_in: int = 30):
        user_on_db = self.db_session.query(UserModel).filter_by(username=user.username).first()
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
            'tipo': user_on_db.tipo
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        expiration_str = expiration.isoformat()
        return {
            'access_token': access_token,
            'expiration': expiration_str,
            'tipo': user_on_db.tipo
        }

    def verify_token(self, access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )
        user_on_db = self.db_session.query(UserModel).filter_by(username=data['sub']).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )