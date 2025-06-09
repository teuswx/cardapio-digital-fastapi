from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.UserModel import UserModel
from jose import jwt, JWTError
from decouple import config
from app.schemas.userLogin import UserLogin
from passlib.context import CryptContext

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
crypt_context = CryptContext(schemes=['sha256_crypt'])

class LoginUserController:
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
            'exp': expiration
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        expiration_str = expiration.isoformat()
        return {
            'access_token': access_token,
            'expiration': expiration_str
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