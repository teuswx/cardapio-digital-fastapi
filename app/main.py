from fastapi import FastAPI
from app.routes.routes import router

app = FastAPI()

@app.get('/')
def chek():
    return "ok, its working"

app.include_router(router)