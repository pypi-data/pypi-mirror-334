"""
Mesh API Client SDK

This package provides a simple, powerful interface to the Mesh API.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional, List, Union

# Set up logging
if os.environ.get("DEBUG", "").lower() in ('true', '1', 'yes'):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mesh")

# Export client classes for advanced usage
from .client import MeshClient
from .zkp_client import MeshZKPClient
from .auto_refresh_client import AutoRefreshMeshClient

# Export model constants
from .models import OpenAI, Anthropic, Provider, get_best_model, get_fastest_model, get_cheapest_model

# Export auth functions
from .auth import authenticate, clear_token, is_authenticated, get_device_code, poll_for_device_token

# Create a singleton client instance
_client = None

def _get_client() -> MeshClient:
    """Get or create a singleton client instance with automatic authentication
    
    Returns:
        MeshClient: An authenticated client with auto-refresh capabilities
    """
    global _client
    
    # Return existing client if available
    if _client is not None:
        return _client
    
    # Import here to avoid circular imports
    from .token_manager import get_token, is_token_valid
    from .auth import authenticate
    
    # Check for existing token
    token_data = get_token()
    
    # Authenticate if needed
    if not token_data or not is_token_valid(token_data):
        # Try to authenticate with backend
        try:
            # The authenticate function will automatically detect environment
            # and choose browser-based or device flow as appropriate
            token_data = authenticate()
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            token_data = None
            
        # Still no token? Raise exception
        if not token_data:
            raise RuntimeError("Authentication failed. Please try again by running 'mesh-auth' from the command line.")
    
    # Create client with token and auto-refresh enabled
    _client = MeshClient(auto_refresh=True)
    
    # The token will be loaded automatically in the client constructor,
    # but we set it explicitly to ensure it's using the latest token
    if token_data and "access_token" in token_data:
        _client.auth_token = token_data["access_token"]
    
    return _client

# =========================
# Simplified API Functions
# =========================

def chat(
    messages: Union[str, List[Dict[str, str]]],
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    thinking: Optional[bool] = None,
    provider: Optional[str] = None,
    **kwargs
) -> Union[str, Dict[str, Any]]:
    """Send a chat request to an AI model.
    
    Args:
        messages: Either a string message or a list of message objects with 'role' and 'content'
        model: Model name to use (e.g., "gpt-4o", "claude-3-opus-20240229")
        temperature: Temperature for generation (0.0-2.0)
        max_tokens: Maximum tokens to generate
        thinking: Whether to enable thinking/reasoning
        provider: Model provider ("openai" or "anthropic")
        **kwargs: Additional model parameters
    
    Returns:
        By default, returns a string containing just the response content.
        If using a custom MeshClient with return_content_only=False, returns the full response dict.
    """
    client = _get_client()
    
    # Convert string to proper message format if needed
    if isinstance(messages, str):
        # If it's a string, just pass it directly to client.chat()
        return client.chat(
            message=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            thinking=thinking,
            provider=provider,
            **kwargs
        )
    else:
        # For message arrays, create proper format
        return client.chat(
            message=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            thinking=thinking,
            provider=provider,
            **kwargs
        )

def complete(
    prompt: str, 
    model: Optional[str] = None, 
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    thinking: Optional[bool] = None,
    provider: Optional[str] = None,
    **kwargs
) -> str:
    """
    Generate text completion from a prompt.
    
    Args:
        prompt: Text prompt for completion
        model: Model name to use (e.g., "gpt-4o", "claude-3-opus-20240229")
        temperature: Temperature for generation (0.0-2.0)
        max_tokens: Maximum tokens to generate
        thinking: Whether to enable thinking/reasoning
        provider: Model provider ("openai" or "anthropic")
        **kwargs: Additional model parameters
    
    Returns:
        String containing the generated text
    """
    messages = [{"role": "user", "content": prompt}]
    response = chat(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        thinking=thinking,
        provider=provider,
        **kwargs
    )
    return response.get("choices", [{}])[0].get("message", {}).get("content", "")

def store_key(key_name: str, key_value: str, user_id: str = None) -> Dict[str, Any]:
    """Store a key in the Mesh API
    
    Args:
        key_name: Name of the key to store
        key_value: Value of the key to store
        user_id: Optional User ID to associate with the key. If not provided, extracted from auth token.
        
    Returns:
        dict: Result of the operation
    """
    client = _get_client()
    return client.store_key(key_name=key_name, key_value=key_value, user_id=user_id)

def get_key(key_name: str, user_id: str = None) -> Optional[str]:
    """Get a key from the Mesh API
    
    Args:
        key_name: Name of the key to retrieve
        user_id: Optional User ID to retrieve key for. If not provided, extracted from auth token.
        
    Returns:
        Optional[str]: The key value if found, or None if not found
    """
    client = _get_client()
    return client.get_key(key_name=key_name, user_id=user_id)

def store_key_zkp(key_name: str, key_value: str, user_id: str = None) -> Dict[str, Any]:
    """Store a key using Zero-Knowledge Proofs
    
    Args:
        key_name: Name of the key to store
        key_value: Value of the key to store
        user_id: Optional User ID to associate with the key. If not provided, extracted from auth token.
        
    Returns:
        dict: Result of the operation
    """
    from .zkp_client import MeshZKPClient
    client = MeshZKPClient()
    
    # Transfer authentication from singleton client
    main_client = _get_client()
    client.auth_token = main_client.auth_token
    
    return client.store_key_zkp(key_name=key_name, key_value=key_value, user_id=user_id)

def verify_key(key_name: str, key_value: str, user_id: str = None) -> bool:
    """Verify a key using Zero-Knowledge Proofs
    
    Args:
        key_name: Name of the key to verify
        key_value: Value of the key to verify
        user_id: Optional User ID to verify key for. If not provided, extracted from auth token.
        
    Returns:
        bool: True if key verified successfully, False otherwise
    """
    from .zkp_client import MeshZKPClient
    client = MeshZKPClient()
    
    # Transfer authentication from singleton client
    main_client = _get_client()
    client.auth_token = main_client.auth_token
    
    result = client.verify_key(key_name=key_name, key_value=key_value, user_id=user_id)
    return result.get("verified", False)

def list_keys(user_id: str = None) -> List[str]:
    """List all keys stored for a user
    
    Args:
        user_id: Optional User ID to list keys for. If not provided, extracted from auth token.
        
    Returns:
        List[str]: A list of key names (without the user_id prefix)
    """
    client = _get_client()
    return client.list_keys(user_id=user_id)

# Set version
__version__ = "1.4.6"

# Export simplified API functions and client classes
__all__ = [
    # Simplified API functions
    'chat',
    'complete',
    'store_key',
    'get_key',
    'store_key_zkp',
    'verify_key',
    'list_keys',
    
    # Client classes for advanced usage
    'MeshClient',
    'MeshZKPClient',
    'AutoRefreshMeshClient',
    
    # Auth utilities
    'authenticate',
    'clear_token',
    'is_authenticated',
    'get_device_code',
    'poll_for_device_token',
    
    # Model utilities
    'get_best_model',
    'get_fastest_model',
    'get_cheapest_model'
]