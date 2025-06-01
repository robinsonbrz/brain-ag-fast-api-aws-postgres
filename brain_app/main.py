from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from brain_app.api import routes
from brain_app.core import init_db
from contextlib import asynccontextmanager
from brain_app.core.exception_middleware import ExceptionLoggingMiddleware
from brain_app.core.logging_middleware import LoggingMiddleware


from brain_app.core import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db.init_db()
    yield
app = FastAPI(title="Produtores Rurais API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ExceptionLoggingMiddleware)

@app.get("/health-check")
async def health_check():
    return {"status": "Healthy!"}

app.include_router(routes.router)
