from fastapi import APIRouter, Depends
from . import schemas
from . database import get_db
from sqlalchemy.orm import Session
from .response import generate_response


router = APIRouter(
    prefix = "/chat",
    tags= ["chat"]
)

@router.post("/generate")
async def generate(request:schemas.ChatMessage, db:Session = Depends(get_db) ):
    response =generate_response(request.query, db, request.file_id)
    return {"query": request.query,
        "response": response}
