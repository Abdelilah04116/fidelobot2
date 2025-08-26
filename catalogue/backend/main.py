from fastapi import FastAPI
from .database import Base, engine

app = FastAPI()

# Crée les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "API catalogue opérationnelle"}
