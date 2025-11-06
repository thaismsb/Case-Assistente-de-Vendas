from pydantic import BaseModel, Field

class MessageInput(BaseModel):
    message: str = Field(..., min_length=1)

class ChatResponse(BaseModel):
    resposta: str
