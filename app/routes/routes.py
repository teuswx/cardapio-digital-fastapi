from fastapi import APIRouter, Depends, status, Header, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.depends import get_db_session, token_verifier

#models
from app.models.user import User
from app.models.userLogin import UserLogin

# Controlers
from app.controllers.user.create_user_controller import CreateUserController
from app.controllers.user.auth_user_controller import AuthUserController
from app.controllers.user.list_user_controller import ListUserController
from app.controllers.token.token_decode_controller import TokenDecodeController
router = APIRouter()



#-----------------------------------------User---------------------------------------------------------------------------------
@router.post('/user/register')
def user_register(user: User, db_session: Session = Depends(get_db_session)):
    uc = CreateUserController(db_session=db_session)
    uc.user_register(user=user)

    return JSONResponse(
        content={"msg": "Success"},
        status_code=status.HTTP_201_CREATED
    )

@router.post('/user/login')
def user_login(request_form_user: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db_session)):
    uc = AuthUserController(db_session=db_session)
    # Ajuste: Use o campo username que foi alterado no modelo User
    user = UserLogin(
        username=request_form_user.username,  # Agora estamos usando 'username'
        password=request_form_user.password,
    )
    auth_data = uc.user_login(user=user)
    return JSONResponse(
        content=auth_data,
        status_code=status.HTTP_200_OK
    )

@router.get('/users')
def test_user_verify(db_session: Session = Depends(get_db_session) ,token_verify = Depends(token_verifier)):
    uc = ListUserController(db_session=db_session)
    return uc.list_user()


@router.post('/token')
def token_decode_payload(token_data: dict):  # O token viria no corpo da requisição
    token = token_data["access_token"]  # Extrai o token do corpo da requisição
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token is missing in the body"
        )
    uc = TokenDecodeController()
    return uc.verify_token_payload(token)
