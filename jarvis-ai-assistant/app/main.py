import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.chat_controller import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Jarvis AI Assistant",
    description="A production-ready RAG pipeline with vector search and embeddings",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("=" * 50)
    logger.info("Jarvis AI Assistant Starting Up")
    logger.info("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("=" * 50)
    logger.info("Jarvis AI Assistant Shutting Down")
    logger.info("=" * 50)
