from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from brain_app.api import routes

app = FastAPI(title="Produtores Rurais API", version="0.1.0")

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
