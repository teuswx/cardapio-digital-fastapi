from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.depends import get_db_session, token_verifier

# model
from app.models.order.create_order_model import CreateOrderModel

# Services
from app.services.order.create_order_service import CreateOrderService
from app.services.order.list_order_service import ListOrderService

order_router = APIRouter(prefix='/order')

@order_router.post('/create')
def create_order_router(order: CreateOrderModel, db_session: Session = Depends(get_db_session), token_verify = Depends(token_verifier)):

    uc = CreateOrderService(db_session=db_session)
    message = uc.create_order(order)
    
    return JSONResponse(
    content={
        "message": message,
        "payload": token_verify['tipo'],
        "status": status.HTTP_200_OK
    },
    status_code=status.HTTP_200_OK)

@order_router.get('/list')
def list_order_router(db_session: Session = Depends(get_db_session), token_verify = Depends(token_verifier)):
    uc = ListOrderService(db_session=db_session)
    list = uc.list_order()
    
    return JSONResponse(
    content={
        "orders": list,
        "payload": token_verify['tipo'],
        "status": status.HTTP_200_OK
    },
    status_code=status.HTTP_200_OK)