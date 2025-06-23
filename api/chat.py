from fastapi import APIRouter
from . import schemas
from . database import get_db
from sqlalchemy.orm import Session
from .response import generate_response


router = APIRouter(
    prefix = "/chat",
    tags= ["chat"]
)

@router.post("/generate")
async def generate(request:schemas.ChatMessage, db:Session = get_db ):
    response =generate_response(request.query, db, request.file_id)
    return {"response": response}
