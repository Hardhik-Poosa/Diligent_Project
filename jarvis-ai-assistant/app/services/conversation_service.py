import uuid
import logging
from app.services.embedding_service import LocalEmbeddingService
from app.services.llm_service import MockLLMService
from app.repositories.vector_repository import VectorRepository

logger = logging.getLogger(__name__)


class ConversationService:
    def __init__(self):
        """Initialize conversation service with embeddings, LLM, and vector store"""
        try:
            logger.info("Initializing ConversationService")
            self.embedder = LocalEmbeddingService()
            self.llm = MockLLMService()
            self.vector_repo = VectorRepository()

            # Seed data
            docs = [
                "Company vacation policy allows 15 days leave per year",
                "Office working hours are 9 AM to 6 PM",
                "Remote work allowed two days a week"
            ]

            logger.info(f"Seeding {len(docs)} documents into vector store")
            for doc in docs:
                try:
                    emb = self.embedder.embed_text(doc)
                    self.vector_repo.add_vector(emb, doc)
                    logger.debug(f"Seeded document: {doc[:50]}...")
                except Exception as e:
                    logger.error(f"Error seeding document: {e}")
            
            logger.info("ConversationService initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing ConversationService: {e}", exc_info=True)
            raise

    def chat(self, message: str, session_id: str | None):
        """Process user message and generate response using RAG pipeline"""
        try:
            session_id = session_id or str(uuid.uuid4())
            logger.info(f"Starting chat for session: {session_id}")

            # Embed query
            logger.debug(f"Embedding query: {message[:50]}...")
            query_embedding = self.embedder.embed_text(message)
            logger.debug(f"Query embedding generated with dimension: {len(query_embedding)}")

            # Search for context
            logger.debug("Searching vector repository")
            contexts = self.vector_repo.search(query_embedding)
            logger.info(f"Found {len(contexts)} relevant contexts")

            context_text = "\n".join(contexts)

            prompt = f"""
Context:
{context_text}

Question:
{message}
"""

            # Generate response
            logger.debug("Generating response from LLM")
            answer = self.llm.generate_response(prompt)
            logger.info(f"Response generated for session: {session_id}")

            return session_id, answer, contexts
        except Exception as e:
            logger.error(f"Error in chat method: {e}", exc_info=True)
            raise
