import uuid
from app.services.embedding_service import LocalEmbeddingService
from app.services.ollama_llm_service import OllamaLLMService
from app.repositories.vector_repository import VectorRepository


class ConversationService:
    def __init__(self):
        self.embedder = LocalEmbeddingService()
        self.llm = OllamaLLMService()
        self.vector_repo = VectorRepository()

        # 🔥 Seed data ONCE
        docs = [
            "Company vacation policy allows 15 days leave per year",
            "Office working hours are from 9 AM to 6 PM",
            "Employees can work remotely two days a week"
        ]

        for doc in docs:
            emb = self.embedder.embed_text(doc)
            self.vector_repo.add_vector(emb, doc)

    def chat(self, message: str, session_id: str | None):
        session_id = session_id or str(uuid.uuid4())

        query_embedding = self.embedder.embed_text(message)
        contexts = self.vector_repo.search(query_embedding)

        prompt = f"""You are an AI assistant.
Use the context below to answer.
If context is insufficient, say so.

Context:
{chr(10).join(contexts)}

Question:
{message}
"""

        answer = self.llm.generate_response(prompt)

        return session_id, answer, contexts
