from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Importando o CORSMiddleware
from app.routes.user_routes import user_router
from app.routes.category_routes import category_router
from app.routes.product_routes import product_router
from app.routes.order_routes import order_router

app = FastAPI()

# Configuração de CORS
origins = [
    "http://localhost",  # Permitir local
    "http://localhost:3000",  # Se você estiver rodando no front-end no port 3000, por exemplo
    # Adicione outros domínios conforme necessário, como o seu frontend de produção
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Defina os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

@app.get('/')
def check():
    return "ok, it's working"

app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(order_router)
