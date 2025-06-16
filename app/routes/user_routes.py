from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.depends import get_db_session, token_verifier

#models
from app.models.user.create_user_model import CreateUserModel
from app.models.user.login_user_model import LoginUserModel
from app.models.user.delete_user_model import DeleteUserModel

# Services
from app.services.user.create_user_service import CreateUserService
from app.services.user.auth_user_service import AuthUserService
from app.services.user.list_user_service import ListUserService
from app.services.user.delete_user_service import DeleteUserService

user_router = APIRouter(prefix='/user')



#-----------------------------------------User---------------------------------------------------------------------------------
@user_router.post('/register')
def user_register(user: CreateUserModel, db_session: Session = Depends(get_db_session)):
    uc = CreateUserService(db_session=db_session)
    uc.user_register(user=user)

    return JSONResponse(
        content={"msg": "Success"},
        status_code=status.HTTP_201_CREATED
    )

@user_router.post('/login')
def user_login(request_form_user: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db_session)):
    uc = AuthUserService(db_session=db_session)
    # Ajuste: Use o campo username que foi alterado no modelo User
    user = LoginUserModel(
        username=request_form_user.username,  # Agora estamos usando 'username'
        password=request_form_user.password,
    )
    auth_data = uc.user_login(user=user)
    return JSONResponse(
        content=auth_data,
        status_code=status.HTTP_200_OK
    )

@user_router.get('/list')
def test_user_verify(db_session: Session = Depends(get_db_session) ,token_verify = Depends(token_verifier)):
    print('oi')
    if token_verify['tipo'] == 'admin':
        uc = ListUserService(db_session=db_session)
        user_list = uc.list_user()
    else:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    'detalhe':'Este tipo de usuário não tem acesso a rota', 
                    'status':status.HTTP_401_UNAUTHORIZED
                }
            )

    
    return JSONResponse(
    content={
        "users": user_list,
        "payload": token_verify['tipo'],
        "status": status.HTTP_200_OK
    },
    status_code=status.HTTP_200_OK)
    

@user_router.delete('/delete')
def delete_user_route(user_id: DeleteUserModel, db_session: Session = Depends(get_db_session), token_verify = Depends(token_verifier)):
    
    if token_verify['tipo'] == 'admin':
        uc = DeleteUserService(db_session=db_session)
        message = uc.delete_user(user_id=user_id)
    else:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    'message':'Este tipo de usuário não tem acesso a rota', 
                    'status':status.HTTP_401_UNAUTHORIZED
                }
            )
    return message

