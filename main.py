import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ENV = os.getenv("ENV", "development")

if ENV == "production":
    origins = ["https://your-frontend-domain.com"]
else:
    origins = ["http://localhost:8000"]

app.add_middleware( 
    CORSMiddleware,
    allow_origins=origins,  # or restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/")
async def post():
    return {"message": "Item created"}