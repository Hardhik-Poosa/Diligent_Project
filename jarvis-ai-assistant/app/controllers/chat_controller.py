from fastapi import APIRouter
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.conversation_service import ConversationService

router = APIRouter()
service = ConversationService()


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    session_id, answer, sources = service.chat(
        request.message,
        request.session_id
    )

    return ChatResponse(
        session_id=session_id,
        message=answer,
        sources=sources
    )
