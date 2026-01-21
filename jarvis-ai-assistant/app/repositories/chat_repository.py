"""
Chat repository for managing conversations and messages
"""
from typing import List, Optional
from abc import ABC, abstractmethod
from app.models.chat_models import Conversation, Message


class ChatRepositoryBase(ABC):
    """Abstract base class for chat repository implementations"""
    
    @abstractmethod
    def save_conversation(self, conversation: Conversation) -> bool:
        """Save a conversation"""
        pass
    
    @abstractmethod
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a conversation by ID"""
        pass
    
    @abstractmethod
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation"""
        pass
    
    @abstractmethod
    def add_message(self, conversation_id: str, message: Message) -> bool:
        """Add a message to a conversation"""
        pass
    
    @abstractmethod
    def get_conversations(self, limit: int = 10) -> List[Conversation]:
        """Get recent conversations"""
        pass


class InMemoryChatRepository(ChatRepositoryBase):
    """In-memory implementation of chat repository"""
    
    def __init__(self):
        """Initialize in-memory repository"""
        self.conversations: dict = {}
    
    def save_conversation(self, conversation: Conversation) -> bool:
        """Save a conversation in memory"""
        self.conversations[conversation.conversation_id] = conversation
        return True
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a conversation from memory"""
        return self.conversations.get(conversation_id)
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation from memory"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False
    
    def add_message(self, conversation_id: str, message: Message) -> bool:
        """Add a message to a conversation"""
        conversation = self.conversations.get(conversation_id)
        if conversation:
            conversation.add_message(message)
            return True
        return False
    
    def get_conversations(self, limit: int = 10) -> List[Conversation]:
        """Get recent conversations"""
        conversations = list(self.conversations.values())
        conversations.sort(key=lambda x: x.updated_at, reverse=True)
        return conversations[:limit]


class FileChatRepository(ChatRepositoryBase):
    """File-based implementation of chat repository"""
    
    def __init__(self, base_path: str = "./data/conversations"):
        """Initialize file-based repository"""
        import os
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
    
    def save_conversation(self, conversation: Conversation) -> bool:
        """Save a conversation to file"""
        try:
            import json
            import os
            
            file_path = os.path.join(self.base_path, f"{conversation.conversation_id}.json")
            
            # Convert conversation to dict
            conv_dict = {
                "conversation_id": conversation.conversation_id,
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat(),
                "metadata": conversation.metadata,
                "messages": [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "timestamp": msg.timestamp.isoformat(),
                        "metadata": msg.metadata
                    }
                    for msg in conversation.messages
                ]
            }
            
            with open(file_path, 'w') as f:
                json.dump(conv_dict, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a conversation from file"""
        try:
            import json
            import os
            from datetime import datetime
            
            file_path = os.path.join(self.base_path, f"{conversation_id}.json")
            
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r') as f:
                conv_dict = json.load(f)
            
            messages = [
                Message(
                    role=msg["role"],
                    content=msg["content"],
                    timestamp=datetime.fromisoformat(msg["timestamp"]),
                    metadata=msg.get("metadata", {})
                )
                for msg in conv_dict["messages"]
            ]
            
            return Conversation(
                conversation_id=conv_dict["conversation_id"],
                messages=messages,
                created_at=datetime.fromisoformat(conv_dict["created_at"]),
                updated_at=datetime.fromisoformat(conv_dict["updated_at"]),
                title=conv_dict.get("title"),
                metadata=conv_dict.get("metadata", {})
            )
        except Exception as e:
            print(f"Error reading conversation: {e}")
            return None
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation file"""
        try:
            import os
            file_path = os.path.join(self.base_path, f"{conversation_id}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting conversation: {e}")
            return False
    
    def add_message(self, conversation_id: str, message: Message) -> bool:
        """Add a message to a conversation file"""
        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.add_message(message)
            return self.save_conversation(conversation)
        return False
    
    def get_conversations(self, limit: int = 10) -> List[Conversation]:
        """Get recent conversations from files"""
        try:
            import os
            conversations = []
            
            for filename in os.listdir(self.base_path):
                if filename.endswith(".json"):
                    conversation_id = filename[:-5]
                    conv = self.get_conversation(conversation_id)
                    if conv:
                        conversations.append(conv)
            
            conversations.sort(key=lambda x: x.updated_at, reverse=True)
            return conversations[:limit]
        except Exception as e:
            print(f"Error reading conversations: {e}")
            return []
