from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.depends import get_db_session, token_verifier

# models
from app.models.category.create_category_model import CreateCategoryModel

# services
from app.services.category.create_category_service import CreateCategoryService
from app.services.category.list_category_service import ListCategoryService


category_router = APIRouter(prefix='/category')

@category_router.post('/create')
def create_category_route(category: CreateCategoryModel, db_session: Session = Depends(get_db_session), token_verify = Depends(token_verifier)):
    if token_verify['tipo'] == 'admin':
        uc = CreateCategoryService(db_session=db_session)
        message = uc.create_category(category=category)
    else:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    'detalhe':'Este tipo de usuário não tem acesso a rota', 
                    'status':status.HTTP_401_UNAUTHORIZED
                }
            )

    return JSONResponse(
        content=message,
        status_code=status.HTTP_200_OK
    )


@category_router.get('/list')
def list_category_route(db_session: Session = Depends(get_db_session), token_verify = Depends(token_verifier)):
    if token_verify['tipo'] == 'admin':
        uc = ListCategoryService(db_session=db_session)
        category_list = uc.list_categories()
    else:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    'detalhe':'Este tipo de usuário não tem acesso a rota', 
                    'status':status.HTTP_401_UNAUTHORIZED
                }
            )

    
    return JSONResponse(
        content=category_list,
        status_code=status.HTTP_200_OK
    )
