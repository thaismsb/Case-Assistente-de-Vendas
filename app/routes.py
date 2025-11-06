from fastapi import APIRouter, HTTPException
from app.models import MessageInput, ChatResponse
from app.client import BedrockClient, get_bedrock_client

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/api/question-and-answer", response_model=ChatResponse)
def gerar_resposta(input_data: MessageInput):
    try:
        client: BedrockClient = get_bedrock_client()
        content = client.chat(input_data.message)  # ⬅️ chama o método chat
        return ChatResponse(resposta=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao chamar Bedrock: {e}")
