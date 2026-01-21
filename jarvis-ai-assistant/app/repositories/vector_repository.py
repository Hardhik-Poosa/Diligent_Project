import logging
import faiss
import numpy as np

logger = logging.getLogger(__name__)


class VectorRepository:
    """Vector repository for managing embeddings using FAISS"""
    
    def __init__(self, dimension: int = 384):
        """Initialize FAISS index with specified dimension"""
        try:
            logger.info(f"Initializing VectorRepository with dimension: {dimension}")
            self.index = faiss.IndexFlatL2(dimension)
            self.texts = []
            self.dimension = dimension
            logger.info("VectorRepository initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing VectorRepository: {e}", exc_info=True)
            raise

    def add_vector(self, embedding: list[float], text: str):
        """Add embedding and associated text to the index"""
        try:
            if not embedding:
                logger.warning(f"Empty embedding provided for text: {text[:50]}...")
                return
            
            if len(embedding) != self.dimension:
                logger.warning(f"Embedding dimension {len(embedding)} does not match index dimension {self.dimension}")
                return
            
            logger.debug(f"Adding vector for text: {text[:50]}...")
            self.index.add(np.array([embedding]).astype("float32"))
            self.texts.append(text)
            logger.debug(f"Vector added. Total vectors: {self.index.ntotal}")
        except Exception as e:
            logger.error(f"Error adding vector: {e}", exc_info=True)
            raise

    def search(self, embedding: list[float], top_k: int = 3):
        """Search for top-k similar vectors"""
        try:
            if self.index.ntotal == 0:
                logger.warning("Vector index is empty")
                return []
            
            if len(embedding) != self.dimension:
                logger.warning(f"Query embedding dimension {len(embedding)} does not match index dimension {self.dimension}")
                return []
            
            logger.debug(f"Searching for top-{top_k} similar vectors")
            distances, indices = self.index.search(
                np.array([embedding]).astype("float32"), top_k
            )
            
            results = [self.texts[i] for i in indices[0]]
            logger.info(f"Search returned {len(results)} results with distances: {distances[0].tolist()}")
            return results
        except Exception as e:
            logger.error(f"Error searching vectors: {e}", exc_info=True)
            raise
