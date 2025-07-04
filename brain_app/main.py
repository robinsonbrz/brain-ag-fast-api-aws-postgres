from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from brain_app.api import routes
from brain_app.core import init_db
from brain_app.core.exception_middleware import ExceptionLoggingMiddleware
from brain_app.core.logging_middleware import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db.init_db()
    yield


app = FastAPI(title="Api - Robinson - Produtores Rurais", version="0.1.2", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ExceptionLoggingMiddleware)


@app.get("/")
async def root_status():
    return {"status": "Healthy!"}


app.include_router(routes.router)
handler = Mangum(app, lifespan="off")
