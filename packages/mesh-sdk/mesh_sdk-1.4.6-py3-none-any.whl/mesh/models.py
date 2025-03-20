"""
Model configuration and constants for Mesh SDK.

This module provides constants and helper functions for working with AI models
from various providers.
"""

from typing import Dict, Any, List, Optional

# OpenAI Models
class OpenAI:
    """Constants for OpenAI models"""
    # GPT-4.5 models
    GPT_4_5_PREVIEW = "gpt-4.5-preview"
    
    # GPT-4o models
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    
    # O1 models
    O1 = "o1"
    O1_MINI = "o1-mini"
    
    # GPT-4 Turbo and GPT-4
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4 = "gpt-4"
    
    # GPT-3.5 Turbo
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    
    # Default model
    DEFAULT = GPT_4O

# Anthropic Models
class Anthropic:
    """Constants for Anthropic models"""
    # Claude 3.7 models
    CLAUDE_3_7_SONNET = "claude-3-7-sonnet-20250219"
    
    # Claude 3.5 models
    CLAUDE_3_5_SONNET = "claude-3-5-sonnet-20241022"
    CLAUDE_3_5_HAIKU = "claude-3-5-haiku-20241022"
    
    # Claude 3 models
    CLAUDE_3_OPUS = "claude-3-opus-20240229"
    CLAUDE_3_SONNET = "claude-3-sonnet-20240229"
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
    
    # Default model
    DEFAULT = CLAUDE_3_7_SONNET

# Provider constants
class Provider:
    """Constants for AI model providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

# Model aliases for easier reference
MODEL_ALIASES = {
    # OpenAI aliases
    "gpt4": "gpt-4",
    "gpt4o": "gpt-4o",
    "gpt4.5": "gpt-4.5-preview",
    "gpt45": "gpt-4.5-preview",
    "gpt3": "gpt-3.5-turbo",
    "gpt35": "gpt-3.5-turbo",
    "gpt3.5": "gpt-3.5-turbo",
    "gpt4omni": "gpt-4o",
    
    # Claude 3.7 aliases
    "claude": "claude-3-7-sonnet-20250219",  # Default to latest Claude
    "claude37": "claude-3-7-sonnet-20250219",
    "claude37sonnet": "claude-3-7-sonnet-20250219",
    "claude37s": "claude-3-7-sonnet-20250219",
    "claude3.7": "claude-3-7-sonnet-20250219",
    "claude-37": "claude-3-7-sonnet-20250219",
    "claude-3-7": "claude-3-7-sonnet-20250219",
    "claude-3.7": "claude-3-7-sonnet-20250219",
    "claude-3.7-sonnet": "claude-3-7-sonnet-20250219",
    
    # Claude 3.5 aliases
    "claude35": "claude-3-5-sonnet-20241022",
    "claude35sonnet": "claude-3-5-sonnet-20241022",
    "claude35s": "claude-3-5-sonnet-20241022",
    "claude3.5": "claude-3-5-sonnet-20241022",
    
    # Claude 3.5 Haiku aliases
    "claude35haiku": "claude-3-5-haiku-20241022",
    "claude35h": "claude-3-5-haiku-20241022",
    
    # Claude 3 Opus aliases
    "claude3opus": "claude-3-opus-20240229",
    "claudeopus": "claude-3-opus-20240229",
    
    # Claude 3 Sonnet aliases
    "claude3sonnet": "claude-3-sonnet-20240229",
    "claude3s": "claude-3-sonnet-20240229",
    
    # Claude 3 Haiku aliases
    "claude3haiku": "claude-3-haiku-20240307",
    "claude3h": "claude-3-haiku-20240307",
}

# Provider-specific model mappings
PROVIDER_MODELS = {
    "openai": {
        # GPT-4.5 models
        "gpt-4.5-preview": "gpt-4.5-preview",
        
        # GPT-4o models
        "gpt-4o": "gpt-4o",
        "gpt-4o-mini": "gpt-4o-mini",
        
        # O1 models
        "o1": "o1",
        "o1-mini": "o1-mini",
        
        # GPT-4 Turbo and GPT-4
        "gpt-4-turbo": "gpt-4-turbo",
        "gpt-4": "gpt-4",
        
        # GPT-3.5 Turbo
        "gpt-3.5-turbo": "gpt-3.5-turbo",
    },
    "anthropic": {
        # Claude 3.7 models
        "claude-3-7-sonnet-20250219": "claude-3-7-sonnet-20250219",
        
        # Claude 3.5 models
        "claude-3-5-sonnet-20241022": "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022": "claude-3-5-haiku-20241022",
        
        # Claude 3 models
        "claude-3-opus-20240229": "claude-3-opus-20240229",
        "claude-3-sonnet-20240229": "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307": "claude-3-haiku-20240307",
    }
}

def normalize_model_name(model_name: str) -> str:
    """
    Normalize a model name to its canonical form.
    
    Args:
        model_name: A model name or alias
        
    Returns:
        str: The canonical model name
    """
    # Check if it's a direct alias
    if model_name.lower() in MODEL_ALIASES:
        return MODEL_ALIASES[model_name.lower()]
    
    # Otherwise return as is
    return model_name

def get_provider_for_model(model_name: str) -> str:
    """
    Determine the provider for a given model.
    
    Args:
        model_name: The model name
        
    Returns:
        str: The provider name ("openai", "anthropic", or "unknown")
    """
    # Normalize the model name first
    model = normalize_model_name(model_name)
    
    # Check each provider's models
    for provider, models in PROVIDER_MODELS.items():
        if model in models.values():
            return provider
    
    # No exact match, use heuristics
    if model.startswith("gpt") or model.startswith("o1"):
        return "openai"
    elif model.startswith("claude"):
        return "anthropic"
    
    # Default to OpenAI
    return "unknown"

def get_best_model(provider: Optional[str] = None) -> str:
    """
    Get the best available model.
    
    Args:
        provider: Optional provider to constrain the choice
        
    Returns:
        str: The best model
    """
    if provider:
        provider = provider.lower()
        if provider == "openai":
            return OpenAI.GPT_4O
        elif provider == "anthropic":
            return Anthropic.CLAUDE_3_7_SONNET
    
    # Default to the best overall model
    return Anthropic.CLAUDE_3_7_SONNET

def get_fastest_model(provider: Optional[str] = None) -> str:
    """
    Get the fastest available model.
    
    Args:
        provider: Optional provider to constrain the choice
        
    Returns:
        str: The fastest model
    """
    if provider:
        provider = provider.lower()
        if provider == "openai":
            return OpenAI.GPT_4O_MINI
        elif provider == "anthropic":
            return Anthropic.CLAUDE_3_5_HAIKU
    
    # Default to the fastest overall model
    return OpenAI.GPT_4O_MINI

def get_cheapest_model(provider: Optional[str] = None) -> str:
    """
    Get the cheapest available model.
    
    Args:
        provider: Optional provider to constrain the choice
        
    Returns:
        str: The cheapest model
    """
    if provider:
        provider = provider.lower()
        if provider == "openai":
            return OpenAI.GPT_3_5_TURBO
        elif provider == "anthropic":
            return Anthropic.CLAUDE_3_5_HAIKU
    
    # Default to the cheapest overall model
    return OpenAI.GPT_3_5_TURBO