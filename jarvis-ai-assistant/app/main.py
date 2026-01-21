from fastapi import FastAPI
from app.controllers.chat_controller import router

app = FastAPI(title="Jarvis AI Assistant")

app.include_router(router)
