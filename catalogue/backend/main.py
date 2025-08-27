from fastapi import FastAPI
from .database import Base, engine
from .api.auth import router as auth_router
from .api.products import router as products_router
from .api.cart import router as cart_router
from .api.likes import router as likes_router
from .api.chat import router as chat_router
from .api.system import router as system_router

app = FastAPI()

# Crée les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

# Inclusion des routers
app.include_router(auth_router, prefix="/api/auth")
app.include_router(products_router, prefix="/api/products")
app.include_router(cart_router, prefix="/api/cart")
app.include_router(likes_router, prefix="/api/likes")
app.include_router(chat_router, prefix="/api/chat")
app.include_router(system_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "API catalogue opérationnelle"}
