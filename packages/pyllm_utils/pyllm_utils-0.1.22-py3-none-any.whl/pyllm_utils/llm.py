import json
import pathlib
import logging
import copy
from .gemini_api.gemini_client import GeminiClient
from .anthropic_api.anthropic_client import AnthropicClient
from .openai_api.openai_client import OpenAIClient

class LLMAPIClient:
    """
    A unified client interface for multiple LLM APIs (OpenAI, Anthropic, Google, LlamaCpp).
    
    This client provides a seamless way to interact with different LLM providers through a unified interface.
    It automatically determines the appropriate backend based on the model name and handles parameter conversion
    between different APIs. Key features include:
    
    1. Automatic model backend detection
    2. Dynamic model switching while preserving state and compatible parameters
    3. Parameter mapping between different provider APIs
    4. Chat history management with context preservation
    5. Support for streaming, JSON mode, and tool calling across providers
    
    The client can dynamically switch between models during a conversation, intelligently transferring
    message history and compatible parameters between different providers.
    
    Example usage:
    ```python
    # Initialize with a default model
    client = LLMAPIClient(model="gpt-4o-mini")
    
    # Send messages to the model
    response = client.request_chat(messages=[{"role": "user", "content": "Hello!"}])
    
    # Switch to a different model mid-conversation
    client.switch_model("claude-3-5-sonnet-latest")
    
    # Or switch models directly in a request
    response = client.request_chat(
        model="gemini-1.5-flash",
        messages=[{"role": "user", "content": "Can you continue our conversation?"}]
    )
    ```
    """
    def __init__(self, model: str = "gpt-4o-mini", **kwargs):
        models_path = pathlib.Path(__file__).parent.resolve() / "models" / "models.json"
        local_models_path = pathlib.Path(__file__).parent.resolve() / "models" / "local_models.json"
        
        with open(models_path, "r", encoding="utf-8") as f:
            models = json.load(f)
        with open(local_models_path, "r", encoding="utf-8") as f:
            local_models = json.load(f)
        
        self.model = model
        self.models = models
        self.local_models = local_models
        self.kwargs = kwargs
        
        self._determine_host_and_create_client()
        
    def _determine_host_and_create_client(self):
        self.host = None
        for model_info in self.local_models.get("local_models", []):
            if model_info["name"] == self.model:
                self.host = "llama-cpp"
                break
        
        if not self.host:
            for model_info in self.models.get("openai", []):
                if model_info["name"] == self.model:
                    self.host = "openai"
                    break
            
            for model_info in self.models.get("anthropic", []):
                if model_info["name"] == self.model:
                    self.host = "anthropic"
                    break
                
            for model_info in self.models.get("google", []):
                if model_info["name"] == self.model:
                    self.host = "google"
                    break
            
        if self.host == "openai":
            self.client = OpenAIClient(model=self.model, **self.kwargs)
        elif self.host == "anthropic":
            self.client = AnthropicClient(model=self.model, **self.kwargs)
        elif self.host == "google":
            self.client = GeminiClient(model=self.model, **self.kwargs)
        elif self.host == "llama-cpp":
            from .llama_cpp_api.llama_cpp_client import LlamaCppClient
            self.client = LlamaCppClient(model=self.model, **self.kwargs)
        else:
            raise ValueError(f"Invalid model: {self.model}")
            
    # Parameter mapping between different client types
    # Maps parameters from source client type to target client type
    _parameter_mapping = {
        # From OpenAI to others
        "openai": {
            "anthropic": {
                "max_tokens": "max_tokens",
                "temperature": "temperature",
                "top_p": "top_p",
                "stream": "stream",
                "stop": "stop",
                "json_mode": "json_mode",
                "tools": "tools"
            },
            "google": {
                "max_tokens": "max_completion_tokens",
                "temperature": "temperature",
                "top_p": "top_p",
                "frequency_penalty": "frequency_penalty",
                "presence_penalty": "presence_penalty",
                "stream": "stream",
                "stop": "stop",
                "tools": "tools"
            },
            "llama-cpp": {
                "max_tokens": "max_completion_tokens",
                "temperature": "temperature",
                "top_p": "top_p",
                "frequency_penalty": "frequency_penalty",
                "presence_penalty": "presence_penalty",
                "stream": "stream",
                "stop": "stop",
                "tools": "tools",
                "json_mode": "json_mode"
            }
        },
        # From Anthropic to others
        "anthropic": {
            "openai": {
                "max_tokens": "max_tokens",
                "temperature": "temperature",
                "top_p": "top_p",
                "stream": "stream",
                "stop": "stop",
                "json_mode": "json_mode",
                "tools": "tools",
                "top_k": "logit_bias"
            },
            "google": {
                "max_tokens": "max_completion_tokens",
                "temperature": "temperature",
                "top_p": "top_p",
                "top_k": "top_k",
                "stream": "stream",
                "stop": "stop",
                "tools": "tools"
            },
            "llama-cpp": {
                "max_tokens": "max_completion_tokens",
                "temperature": "temperature", 
                "top_p": "top_p",
                "top_k": "top_k",
                "stream": "stream",
                "stop": "stop",
                "tools": "tools",
                "json_mode": "json_mode"
            }
        },
        # From Google to others
        "google": {
            "openai": {
                "max_completion_tokens": "max_tokens",
                "temperature": "temperature",
                "top_p": "top_p",
                "frequency_penalty": "frequency_penalty",
                "presence_penalty": "presence_penalty",
                "stream": "stream",
                "stop": "stop",
                "tools": "tools"
            },
            "anthropic": {
                "max_completion_tokens": "max_tokens",
                "temperature": "temperature",
                "top_p": "top_p",
                "stream": "stream",
                "stop": "stop",
                "tools": "tools",
                "top_k": "top_k"
            },
            "llama-cpp": {
                "max_completion_tokens": "max_completion_tokens",
                "temperature": "temperature",
                "top_p": "top_p",
                "top_k": "top_k",
                "frequency_penalty": "frequency_penalty",
                "presence_penalty": "presence_penalty",
                "stream": "stream",
                "stop": "stop",
                "tools": "tools",
                "response_schema": "response_format"
            }
        },
        # From LlamaCpp to others
        "llama-cpp": {
            "openai": {
                "max_completion_tokens": "max_tokens",
                "temperature": "temperature",
                "top_p": "top_p",
                "frequency_penalty": "frequency_penalty",
                "presence_penalty": "presence_penalty",
                "stream": "stream",
                "stop": "stop",
                "tools": "tools",
                "json_mode": "json_mode",
                "seed": "seed"
            },
            "anthropic": {
                "max_completion_tokens": "max_tokens",
                "temperature": "temperature",
                "top_p": "top_p",
                "top_k": "top_k",
                "stream": "stream",
                "stop": "stop",
                "tools": "tools",
                "json_mode": "json_mode"
            },
            "google": {
                "max_completion_tokens": "max_completion_tokens",
                "temperature": "temperature",
                "top_p": "top_p",
                "top_k": "top_k",
                "frequency_penalty": "frequency_penalty",
                "presence_penalty": "presence_penalty",
                "stream": "stream",
                "stop": "stop",
                "tools": "tools",
                "response_format": "response_schema"
            }
        }
    }
    
    # Common parameters that exist across all clients
    _common_parameters = [
        "messages",
        "model",
        "temperature",
        "stream",
        "tools",
        "json_mode"
    ]
            
    def switch_model(self, model: str, preserve_state: bool = True, **additional_kwargs):
        """
        Switch to a different model while preserving common parameters and state.
        
        Args:
            model (str): The name of the model to switch to
            preserve_state (bool): Whether to preserve message history and other state
            **additional_kwargs: Additional parameters specific to the new model
            
        Returns:
            None
        """
        if model == self.model:
            logging.info(f"Already using model {model}, no switch needed")
            return
            
        previous_client = self.client
        previous_host = self.host
        
        # Save current state if needed
        current_messages = []
        current_state = {}
        current_client_params = {}
        
        if preserve_state:
            # Save messages history
            if hasattr(previous_client, 'messages') and previous_client.messages:
                current_messages = copy.deepcopy(previous_client.messages)
                
            # Extract additional state parameters that we want to preserve
            if hasattr(previous_client, 'latest_complete_response'):
                current_state['latest_complete_response'] = previous_client.latest_complete_response
                
            # Common flags to preserve if they exist
            for flag in ['json_stream', 'json_non_stream', 'normal_stream', 'normal_non_stream', 'tool_called']:
                if hasattr(previous_client, flag):
                    current_state[flag] = getattr(previous_client, flag)
                    
            # Extract parameters from the current client
            if hasattr(previous_client, 'defined_params'):
                try:
                    defined_params = previous_client.defined_params
                    for param in defined_params:
                        if hasattr(previous_client, param) and param != 'self' and param != 'kwargs':
                            value = getattr(previous_client, param)
                            if value is not None:
                                current_client_params[param] = value
                except Exception as e:
                    logging.warning(f"Error extracting parameters from previous client: {e}")
            
            # Also check the kwargs dictionary if it exists
            if hasattr(previous_client, 'kwargs'):
                try:
                    for key, value in previous_client.kwargs.items():
                        if value is not None and key not in current_client_params:
                            current_client_params[key] = value
                except Exception as e:
                    logging.warning(f"Error extracting kwargs from previous client: {e}")
        
        # Update model and create new client
        self.model = model
        old_kwargs = self.kwargs.copy()
        
        # Map parameters from the old client type to the new client type
        new_kwargs = {}
        
        # First, determine the target host
        target_host = None
        for model_info in self.local_models.get("local_models", []):
            if model_info["name"] == model:
                target_host = "llama-cpp"
                break
        
        if not target_host:
            for model_info in self.models.get("openai", []):
                if model_info["name"] == model:
                    target_host = "openai"
                    break
            
            for model_info in self.models.get("anthropic", []):
                if model_info["name"] == model:
                    target_host = "anthropic"
                    break
                
            for model_info in self.models.get("google", []):
                if model_info["name"] == model:
                    target_host = "google"
                    break
        
        # Verify that we found a valid host for the model
        if not target_host:
            raise ValueError(f"Model '{model}' not found in any of the supported providers. Please check the model name or update your models.json file.")
            
        # If we have parameter mapping for this transition
        if preserve_state and previous_host in self._parameter_mapping and target_host in self._parameter_mapping[previous_host]:
            param_map = self._parameter_mapping[previous_host][target_host]
            
            # Map the parameters
            for source_param, target_param in param_map.items():
                if source_param in current_client_params:
                    new_kwargs[target_param] = current_client_params[source_param]
                    
            # Also include common parameters
            for param in self._common_parameters:
                if param in current_client_params and param not in new_kwargs:
                    new_kwargs[param] = current_client_params[param]
        
        # Update with additional kwargs and default kwargs
        for key, value in self.kwargs.items():
            if key not in new_kwargs:
                new_kwargs[key] = value
                
        new_kwargs.update(additional_kwargs)
        self.kwargs = new_kwargs
        
        # Determine new host and create client
        old_host = self.host
        self._determine_host_and_create_client()
        
        if preserve_state and current_messages:
            # Set messages if the new client supports it
            if hasattr(self.client, 'messages'):
                try:
                    self.client.messages = current_messages
                    
                    # If the client has a chat history manager, update it
                    if hasattr(self.client, 'chat_history_manager'):
                        if hasattr(self.client.chat_history_manager, 'update_messages'):
                            self.client.chat_history_manager.update_messages(current_messages)
                        elif hasattr(self.client.chat_history_manager, 'messages'):
                            self.client.chat_history_manager.messages = current_messages
                except Exception as e:
                    logging.warning(f"Failed to transfer message history: {e}")
            else:
                logging.warning(f"New client {self.host} does not support message history transfer")
                
        # Transfer other state parameters
        for key, value in current_state.items():
            if hasattr(self.client, key):
                try:
                    setattr(self.client, key, value)
                except Exception as e:
                    logging.warning(f"Failed to transfer state parameter '{key}': {e}")
                
        logging.info(f"Switched from {old_host} model to {self.host} model: {model}")
        return self.client
    
    def request_messages(self, **kwargs):
        """
        Request messages from the LLM API.
        
        Args:
            **kwargs: Parameters for the request
            
        Returns:
            The response from the LLM API
        """
        # Check if a model switch is requested
        if 'model' in kwargs and kwargs['model'] != self.model:
            model = kwargs.pop('model')
            logging.info(f"Model switch requested in request_messages from {self.model} to {model}")
            self.switch_model(model)
        
        return self.client.request_messages(**kwargs)
    
    def request_chat(self, **kwargs):
        """
        Request a chat completion from the LLM API.
        
        Args:
            **kwargs: Parameters for the request
            
        Returns:
            The response from the LLM API
        """
        # Check if a model switch is requested
        if 'model' in kwargs and kwargs['model'] != self.model:
            model = kwargs.pop('model')
            logging.info(f"Model switch requested in request_chat from {self.model} to {model}")
            self.switch_model(model)
            
        return self.client.request_chat(**kwargs)
    
    def get_latest_response(self):
        """
        Get the latest response from the LLM API.
        
        Returns:
            The latest response from the LLM API
        """
        return self.client.get_latest_response()
    
    def clear_chat_history(self):
        """
        Clear the chat history.
        
        Returns:
            The result of clearing the chat history
        """
        return self.client.clear_chat_history()

    def request_embeddings(self, input: str, model: str = "text-embedding-3-large"):
        return self.client.request_embeddings(input, model)
    
    async def async_request_embeddings(self, input: str, model: str = "text-embedding-3-large"):
        """
        Asynchronously request embeddings for the given input.
        
        Args:
            input: The input to generate embeddings for
            model: The model to use for embeddings
            
        Returns:
            The embeddings for the input
        """
        # Since some clients may not have async capability, we'll just use the synchronous version
        return self.request_embeddings(input, model)
    