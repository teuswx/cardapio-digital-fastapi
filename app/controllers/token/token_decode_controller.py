from fastapi import HTTPException, status
from jose import jwt, JWTError
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

class TokenDecodeController:

    @staticmethod
    def verify_token_payload(access_token: str):  # Tornar o método estático
        try:
            # Decodifica e verifica a assinatura do token
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token or expired token"
            )
