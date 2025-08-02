import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes
from app.core.config import settings

app = FastAPI()

ENV = os.getenv("ENV", "development")

if ENV == "production":
    origins = ["https://your-frontend-domain.com"]
else:
    origins = ["http://localhost:8000"]

app.add_middleware( 
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # or restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)