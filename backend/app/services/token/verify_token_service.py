from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi import HTTPException, status
from decouple import config

from app.schemas.schemas import UserSchema
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

class VerifyTokenSerice:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    def verify_token(self, access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )
        user_on_db = self.db_session.query(UserSchema).filter_by(username=data['sub']).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )
        return data