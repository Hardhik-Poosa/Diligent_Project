import os
from pinecone import Pinecone


class VectorRepository:
    def __init__(self, dimension: int = 384):
        try:
            api_key = os.getenv("PINECONE_API_KEY")
            if not api_key or api_key == "your_real_key_here":
                raise ValueError("PINECONE_API_KEY not configured or is placeholder")
            
            pc = Pinecone(api_key=api_key)
            index_name = os.getenv("PINECONE_INDEX_NAME", "jarvis-index")

            try:
                if index_name not in pc.list_indexes().names():
                    pc.create_index(
                        name=index_name,
                        dimension=dimension,
                        metric="cosine"
                    )
            except Exception as e:
                print(f"Warning: Could not create/list indexes: {e}")

            self.index = pc.Index(index_name)
        except Exception as e:
            print(f"Warning: Pinecone not available: {e}. Using mock index.")
            self.index = None

    def add_vector(self, embedding: list[float], text: str):
        if self.index is None:
            return
        try:
            self.index.upsert([
                (
                    str(hash(text)),
                    embedding,
                    {"content": text}
                )
            ])
        except Exception as e:
            print(f"Warning: Could not add vector: {e}")

    def search(self, embedding: list[float], top_k: int = 3):
        if self.index is None:
            return []
        try:
            results = self.index.query(
                vector=embedding,
                top_k=top_k,
                include_metadata=True
            )

            return [m.metadata["content"] for m in results.matches]
        except Exception as e:
            print(f"Warning: Could not search vectors: {e}")
            return []
