from fastapi import APIRouter
from app.schemas.chat_schema import ChatReq, ChatRes
from app.services.chat_service import process_chat

router = APIRouter(prefix="/chat", tags=["Chatbot"])

@router.post("", response_model=ChatRes)
def chat_endpoint(req: ChatReq):
    return process_chat(req)
