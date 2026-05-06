from pydantic import BaseModel

class ChatReq(BaseModel):
    user_id: int
    message: str

class ChatRes(BaseModel):
    reply: str
