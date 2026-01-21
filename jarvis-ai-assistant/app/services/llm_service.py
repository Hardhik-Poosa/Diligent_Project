import logging

logger = logging.getLogger(__name__)


class MockLLMService:
    """Mock LLM service for testing and development"""
    
    def __init__(self):
        """Initialize mock LLM service"""
        logger.info("Initializing MockLLMService")
        self.model_name = "mock-gpt"
    
    def generate_response(self, prompt: str) -> str:
        """Generate mock response based on prompt"""
        try:
            if not prompt or not prompt.strip():
                logger.warning("Empty prompt provided")
                return "I received an empty prompt. Please provide a question."
            
            logger.debug(f"Generating mock response for prompt: {prompt[:100]}...")
            response = f"Mock response based on prompt:\n{prompt}"
            logger.debug("Mock response generated successfully")
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}", exc_info=True)
            raise
