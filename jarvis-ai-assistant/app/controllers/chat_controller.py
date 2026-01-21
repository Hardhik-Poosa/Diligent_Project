import logging
from fastapi import APIRouter, HTTPException
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.conversation_service import ConversationService

logger = logging.getLogger(__name__)

router = APIRouter()
service = ConversationService()


@router.get("/health")
def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "service": "Jarvis AI Assistant",
        "version": "1.0.0"
    }


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """Chat endpoint for conversational AI"""
    try:
        logger.info(f"Processing message: {request.message[:50]}...")
        
        session_id, answer, sources = service.chat(
            request.message,
            request.session_id
        )
        
        logger.info(f"Response generated for session: {session_id}")
        return ChatResponse(
            session_id=session_id,
            answer=answer,
            sources=sources
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
