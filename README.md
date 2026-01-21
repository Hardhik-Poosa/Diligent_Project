# 🤖 Jarvis AI Assistant

A comprehensive AI-powered conversational assistant built with Python, featuring advanced capabilities for document retrieval, conversation management, and intelligent response generation.

## 📋 Features

- **Conversational AI**: Powered by OpenAI GPT models or local LLMs
- **Vector Search**: RAG (Retrieval Augmented Generation) capabilities with Chroma
- **Embeddings**: Advanced text embeddings using Sentence Transformers
- **Conversation Management**: Save, load, and manage multiple conversations
- **Document Management**: Add and search context documents
- **Streamlit UI**: Interactive web interface for easy interaction
- **Flexible Architecture**: Easy to swap services and repositories
- **Mock Testing**: Built-in mock services for development and testing

## 🏗️ Architecture

```
jarvis-ai-assistant/
├── app/
│   ├── config/              # Configuration settings
│   ├── models/              # Data models (Chat, Documents)
│   ├── repositories/        # Data access layer
│   ├── services/            # Business logic
│   ├── controllers/         # API controllers
│   └── main.py             # Application entry point
├── ui/
│   └── streamlit_app.py    # Streamlit UI
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd jarvis-ai-assistant
```

2. **Create a virtual environment**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy and edit the .env file
cp .env.example .env
# Edit .env with your API keys and settings
```

### Running the Application

#### Using Streamlit UI (Recommended)
```bash
streamlit run ui/streamlit_app.py
```

The app will be available at `http://localhost:8501`

#### Using Python directly
```bash
python -m app.main
```

## 🔧 Configuration

Edit the `.env` file to configure:

- **LLM Settings**: Model choice and API keys
- **Embedding Settings**: Model and API configuration
- **Vector Database**: Type and path
- **Application Settings**: Debug mode, log level, token limits

Example configuration:
```env
LLM_MODEL=gpt-3.5-turbo
LLM_API_KEY=sk-...
EMBEDDING_MODEL=text-embedding-ada-002
VECTOR_DB_TYPE=chroma
DEBUG=False
```

## 📚 Usage Examples

### Basic Chat
```python
from app.main import initialize_app

chat_controller = initialize_app()

# Create a new conversation
result = chat_controller.create_new_conversation("My Chat")

# Send a message
response = chat_controller.send_chat_message("Hello!")
print(response["response"])

# Get history
history = chat_controller.get_conversation_history()
```

### Adding Documents
```python
# Add a document for context
chat_controller.add_document(
    content="Your document content here",
    doc_id="doc_1",
    metadata={"source": "manual"}
)

# Search for relevant context
results = chat_controller.search_context("query here")
```

### Managing Conversations
```python
# Get recent conversations
conversations = chat_controller.get_recent_conversations(limit=10)

# Load a conversation
chat_controller.get_conversation_history()

# Clear current conversation
chat_controller.clear_conversation()

# Delete a conversation
chat_controller.delete_conversation("conversation_id")
```

## 🔌 Services

### LLM Services
- **OpenAILLMService**: Uses OpenAI API (GPT-3.5-turbo, GPT-4)
- **HuggingFaceLLMService**: Uses Hugging Face models
- **MockLLMService**: For testing and development

### Embedding Services
- **OpenAIEmbeddingService**: OpenAI embeddings API
- **HuggingFaceEmbeddingService**: Sentence Transformers via Hugging Face
- **LocalEmbeddingService**: Local Sentence Transformers models

### Repositories
- **InMemoryChatRepository**: In-memory conversation storage
- **FileChatRepository**: File-based conversation storage
- **ChromaVectorRepository**: Vector database for embeddings

## 📦 API Endpoints (if using FastAPI)

```
POST   /chat/conversations           - Create a new conversation
POST   /chat/messages               - Send a message
GET    /chat/conversations/{id}     - Get conversation history
DELETE /chat/conversations/{id}     - Delete a conversation
POST   /documents                   - Add a document
GET    /documents/search            - Search documents
```

## 🧪 Testing

Run tests with pytest:
```bash
pytest tests/
pytest tests/ --cov=app  # With coverage
```

## 🛠️ Development

### Code Style
```bash
# Format code with Black
black app/

# Lint with Flake8
flake8 app/

# Type checking with Mypy
mypy app/
```

### Adding New LLM Service
```python
from app.services.llm_service import LLMServiceBase

class CustomLLMService(LLMServiceBase):
    def generate_response(self, prompt, context=None):
        # Implement your logic
        pass
    
    def generate_chat_response(self, messages, system_prompt=None):
        # Implement your logic
        pass
```

### Adding New Repository
```python
from app.repositories.chat_repository import ChatRepositoryBase

class CustomChatRepository(ChatRepositoryBase):
    def save_conversation(self, conversation):
        # Implement storage logic
        pass
    
    # Implement other abstract methods
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review the code comments

## 🚀 Future Enhancements

- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Real-time collaboration
- [ ] Advanced analytics dashboard
- [ ] Custom knowledge base integration
- [ ] Fine-tuning capabilities
- [ ] WebSocket support for real-time updates
- [ ] Mobile application

## 📄 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Sentence Transformers](https://www.sbert.net)
- [Chroma Documentation](https://docs.trychroma.com)

---

**Built with ❤️ | Powered by AI**
