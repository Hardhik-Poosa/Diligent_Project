import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class LocalEmbeddingService:
    def __init__(self):
        """Initialize local embedding service with Sentence Transformers"""
        try:
            logger.info("Loading Sentence Transformer model: all-MiniLM-L6-v2")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}", exc_info=True)
            raise

    def embed_text(self, text: str) -> list[float]:
        """Generate embedding for input text"""
        try:
            if not text or not text.strip():
                logger.warning("Empty text provided for embedding")
                return []
            
            logger.debug(f"Embedding text: {text[:50]}...")
            embedding = self.model.encode(text).tolist()
            logger.debug(f"Embedding generated with dimension: {len(embedding)}")
            return embedding
        except Exception as e:
            logger.error(f"Error embedding text: {e}", exc_info=True)
            raise
