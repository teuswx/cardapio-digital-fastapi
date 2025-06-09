from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.depends import get_db_session, token_verifier

from app.controllers.auth_user_controller import AuthUserController
from app.controllers.login_user_controller import LoginUserController
from app.schemas.user import User
from app.schemas.userLogin import UserLogin
router = APIRouter()

@router.post('/user/register')
def user_register(user: User, db_session: Session = Depends(get_db_session)):
    uc = AuthUserController(db_session=db_session)
    uc.user_register(user=user)

    return JSONResponse(
        content={"msg": "Success"},
        status_code=status.HTTP_201_CREATED
    )

@router.post('/user/login')
def user_login(request_form_user: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db_session)):
    uc = LoginUserController(db_session=db_session)
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

@router.get('/test')
def test_user_verify(token_verify = Depends(token_verifier)):
    return 'Its works'