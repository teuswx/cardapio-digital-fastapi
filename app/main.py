from fastapi import FastAPI
from app.routes.user_routes import user_router
from app.routes.category_routes import category_router
from app.routes.product_routes import product_router

app = FastAPI()

@app.get('/')
def chek():
    return "ok, its working"

app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)