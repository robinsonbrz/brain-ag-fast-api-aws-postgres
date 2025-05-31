from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from brain_app.api import routes
from brain_app.core.database import engine
from brain_app.models import models
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Produtores Rurais API", version="0.1.0", lifespan=lifespan)

 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health-check")
async def health_check():
    return {"status": "Healthy!"}

app.include_router(routes.router)
