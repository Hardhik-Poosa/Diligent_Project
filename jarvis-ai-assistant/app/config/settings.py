import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
    LLM_MODEL_PATH = os.getenv("LLM_MODEL_PATH")

settings = Settings()
