"""
Interface for all LLM interactions.
Abstracts away the specific API calls for different providers.
"""

import json
from autonomous_app_writer import config
from autonomous_app_writer.core.logging_setup import get_logger

# This is a placeholder for a more robust implementation.
# In a real scenario, you would use libraries like 'openai', 'anthropic', etc.
# and handle authentication, retries, and error handling properly.

logger = get_logger(__name__)

class LLMService:
    """
    A wrapper for interacting with a Large Language Model.
    """
    def __init__(self, provider=config.LLM_PROVIDER, api_key=None):
        self.provider = provider
        self.api_key = api_key
        self.cache = {}
        logger.info(f"Initializing LLM Service with provider: {self.provider}")

        if self.provider == "openai" and not self.api_key:
            self.api_key = config.OPENAI_API_KEY
        elif self.provider == "google" and not self.api_key:
            self.api_key = config.GOOGLE_API_KEY
        # Add other providers like 'anthropic' here
        
        if not self.api_key:
            logger.warning(f"API key for {self.provider} is not configured.")

    def generate_text(self, prompt, model=config.DEFAULT_MAIN_MODEL, temperature=0.7):
        """
        Generates text using the configured LLM.
        
        Args:
            prompt (str): The input prompt for the LLM.
            model (str): The specific model to use.
            temperature (float): The creativity of the response.

        Returns:
            str: The generated text from the LLM.
        """
        cache_key = (prompt, model, temperature)
        if cache_key in self.cache:
            logger.info("Returning cached LLM response.")
            return self.cache[cache_key]

        logger.debug(f"Generating text with model {model} and temperature {temperature}")
        
        # This is a mock implementation.
        # Replace this with actual API calls to your LLM provider.
        if not self.api_key:
            logger.error("LLM API key not found. Returning mock response.")
            return f"Mock response for prompt: '{prompt}'"

        # Example for OpenAI (requires 'openai' library):
        # from openai import OpenAI
        # client = OpenAI(api_key=self.api_key)
        # response = client.chat.completions.create(
        #     model=model,
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=temperature,
        # )
        # return response.choices[0].message.content

        # For now, returning a simple placeholder
        result = f"LLM ({self.provider}/{model}): Successfully processed prompt - '{prompt[:50]}...'"
        self.cache[cache_key] = result
        return result


    def parse_json_response(self, response_str):
        """
        Safely parses a JSON object from an LLM's string response,
        which may include markdown code blocks.
        """
        logger.debug(f"Parsing JSON from response: {response_str[:100]}...")
        try:
            # Find the start and end of the JSON block
            json_start = response_str.find('{')
            json_end = response_str.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON object found in the response.")

            json_str = response_str[json_start:json_end]
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse JSON response: {e}\nResponse was: {response_str}")
            raise

# A default instance to be used across the application
default_llm_service = LLMService()

def get_llm_service():
    """
    Returns the default LLM service instance.
    """
    return default_llm_service
