from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "FastAPI is connected!"}

@router.get("/grade")
async def get_grade():
    # Query db to see if 
    return {"message": "Item created"}