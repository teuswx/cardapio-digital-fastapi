from app.database.connection import SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.services.token.verify_token_service import VerifyTokenSerice

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')
def get_db_session():
    try:
        session = SessionLocal()
        yield session
    finally:

        session.close()

def token_verifier(db_session: Session = Depends(get_db_session), token = Depends(oauth_scheme)):
    uc = VerifyTokenSerice(db_session=db_session)
    payload = uc.verify_token(access_token=token)
    return payload