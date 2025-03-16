# Created by Sean L. on Mar 15
# 
# emb2emb client
# ollama_conn.py
# 
# PromptCraft, 2025. All rights reserved.

import requests
from utils.const import OLLAMA_ENDPOINT
from typing import List, Dict

class OllamaRequest:
    """Represents a request configuration for the Ollama API endpoint.
    
    Attributes:
        model (str): Identifier of the LLM model used (e.g., "llama3.2:3b")
        prompt (str): Input text for model processing
        options (Dict[str, Any]): Configuration parameters including:
            - temperature (float): Default 0.0, controls randomness (0=deterministic)
            - top_p (float): Default 0.9, nucleus sampling threshold
            - [Additional dynamic options from keyword arguments]

    Example:
        >>> req = OllamaRequest(
        ...     model="llama3.2:3b",
        ...     prompt="Why is the sky blue?",
        ...     top_k=40
        ... )
        >>> req.options
        {'temperature': 0.0, 'top_p': 0.9, 'top_k': 40}
    """
    def __init__(self, model: str, prompt: str, temp: int = 0, **options: Any):
        """Initialize an API request configuration.

        Args:
            model: Target model identifier (e.g., 'llama3.2:3b')
            prompt: Input text for processing
            temp: Temperature parameter (0.0-1.0). Defaults to 0.
            ​**options: Additional model parameters as key-value pairs

        Example:
            >>> req = OllamaRequest(
            ...     model="llama3.2:3b",
            ...     prompt="Why is the sky blue?",
            ...     top_k=40
            ... )
            >>> req.model
            'llama3.2:3b'
            >>> req.prompt 
            'Why is the sky blue?'
            >>> req.options
            {'temperature': 0.0, 'top_p': 0.9, 'top_k': 40}
        """
        self.model = model
        self.prompt = prompt
        self.options = {
            'temperature': temp,
            'top_p': 0.9,   # Default diversity control
            **options
        }

    def ask(self):
        
        """Send the prompt to the Ollama API endpoint for processing.
        
        Returns:
            dict: Parsed JSON response containing:
                - model (str): Model identifier used for generation
                - response (str): Generated text content
                - created_at (str): ISO 8601 timestamp of generation completion
                - done (bool): Completion status (True indicates successful generation)
                - done_reason (str): Termination reason ('stop', 'length', or 'error')
                - context (List[int]): Token sequence for conversation continuation
                - total_duration (int): Total processing time in nanoseconds
                - load_duration (int): Model loading time in nanoseconds  
                - prompt_eval_count (int): Number of tokens processed in prompt
                - prompt_eval_duration (int): Prompt evaluation time in nanoseconds
                - eval_count (int): Number of tokens generated
                - eval_duration (int): Generation evaluation time in nanoseconds

        Raises:
            requests.exceptions.Timeout: If server response exceeds 30 seconds
            requests.exceptions.HTTPError: For 4xx client or 5xx server errors
            requests.exceptions.ConnectionError: Network connectivity failures
            requests.exceptions.RequestException: Base exception for request errors

        Example:
            >>> request = OllamaRequest(model="llama3.2:3b", prompt="Hello")
            >>> response = request.ask()
            >>> print(response['response'])
            'Hello! How can I assist you today?'
        """
        try:
            response = requests.post(
                f'{OLLAMA_ENDPOINT}/api/generate',
                json={
                    'model': self.model,
                    'prompt': self.prompt,
                    'options': self.options,
                    'stream': False
                },
                timeout=30  # Add request timeout for better ux
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {str(e)}")
            raise e