from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import shutil
import os
from pathlib import Path
from app.depends import get_db_session, token_verifier

# models
from app.models.product.create_product_model import CreateProductModel

# services
from app.services.product.create_product_service import CreateProductService
from app.services.product.list_product_service import ListProductService

product_router = APIRouter(prefix='/product')

@product_router.post('/create')
def create_product_route(
    name: str = Form(...),
    price: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    file: UploadFile = File(...),
    db_session: Session = Depends(get_db_session),
    token_verify = Depends(token_verifier)
):
    
    if token_verify['tipo'] == 'admin':

        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)

        filename = Path(file.filename).name

        file_location = f"{temp_dir}/{filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)


        product = CreateProductModel(
            name=name,
            price=price,
            description=description,
            banner=file.filename,
            category_id=category_id
        )

        uc = CreateProductService(db_session=db_session)
        product_message = uc.create_product(product=product)
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
        "message": product_message['message'],
        "payload": token_verify['tipo'],
        "status": status.HTTP_200_OK
    },
    status_code=status.HTTP_200_OK)


@product_router.get('/list')
def list_product_router(db_session: Session = Depends(get_db_session), token_verify = Depends(token_verifier)):
    if token_verify['tipo'] == 'admin':
        uc = ListProductService(db_session=db_session)
        product_list = uc.list_product()
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
        "products": product_list,
        "payload": token_verify['tipo'],
        "status": status.HTTP_200_OK
    },
    status_code=status.HTTP_200_OK)
