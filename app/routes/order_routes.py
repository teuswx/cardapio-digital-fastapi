from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.depends import get_db_session, token_verifier

# model
from app.models.order.create_order_model import CreateOrderModel
from app.models.order.detail_order_model import DetailOrderModel
from app.models.order.add_item_model import AddItemModel
from app.models.order.delete_item_model import DeleteItemModel

# Services
from app.services.order.create_order_service import CreateOrderService
from app.services.order.list_order_service import ListOrderService
from app.services.order.detail_order_service import DetailOrderService
from app.services.order.delete_order_service import DeleteOrderService
from app.services.order.add_item_service import AddItemService
from app.services.order.delete_item_service import DeleteItemService
from app.services.order.send_order_service import SendOrderService
from app.services.order.finish_order_service import FinishOrderService
order_router = APIRouter(prefix='/order')

@order_router.post('/create')
def create_order_router(order: CreateOrderModel, db_session: Session = Depends(get_db_session), token_verify = Depends(token_verifier)):

    uc = CreateOrderService(db_session=db_session)
    message = uc.create_order(order)
    
    return JSONResponse(
        content=message,
        status_code=status.HTTP_200_OK
    )

@order_router.get('/list')
def list_order_router(db_session: Session = Depends(get_db_session), token_verify = Depends(token_verifier)):
    uc = ListOrderService(db_session=db_session)
    list = uc.list_order()
    
    return JSONResponse(
        content=list,
        status_code=status.HTTP_200_OK
    )

@order_router.delete('/order')
def delete_order_router(order_id: DetailOrderModel, db_session: Session = Depends(get_db_session), token_verify = Depends(token_verifier)):
    uc = DeleteOrderService(db_session=db_session)
    message = uc.delete_order(order_id)

    return JSONResponse(
        content=message,
        status_code=status.HTTP_200_OK
    )

@order_router.post('/add')
def add_item_router(item: AddItemModel, db_session: Session = Depends(get_db_session), token_verify = Depends(token_verifier)):
    uc = AddItemService(db_session=db_session)
    message = uc.add_item(item)

    return JSONResponse(
        content=message,
        status_code=status.HTTP_200_OK
    )


@order_router.delete('/item')
def delete_item_router(item: DeleteItemModel, db_session: Session = Depends(get_db_session), token_verify = Depends(token_verifier)):
    uc = DeleteItemService(db_session=db_session)
    message = uc.delete_item(item)

    return JSONResponse(
        content=message,
        status_code=status.HTTP_200_OK
    )

@order_router.put('/send')
def send_order_router(order: DetailOrderModel, db_session: Session = Depends(get_db_session), token_verify = Depends(token_verifier)):
    uc = SendOrderService(db_session=db_session)
    message = uc.send_order(order)

    return JSONResponse(
        content=message,
        status_code=status.HTTP_200_OK
    )


@order_router.get('/detail')
def detail_order_router(item_id: DetailOrderModel, db_session: Session = Depends(get_db_session), token_verify = Depends(token_verifier)):
    uc = DetailOrderService(db_session=db_session)
    item_details = uc.detail_order(item_id)

    return JSONResponse(
        content=item_details,
        status_code=status.HTTP_200_OK
    )

@order_router.put('/finish')
def finish_order_router(order_id: DetailOrderModel, db_session: Session = Depends(get_db_session), token_verify = Depends(token_verifier)):
    uc = FinishOrderService(db_session=db_session)
    orders_details = uc.fish_order(order_id)

    return JSONResponse(
        content=orders_details,
        status_code=status.HTTP_200_OK
    )

