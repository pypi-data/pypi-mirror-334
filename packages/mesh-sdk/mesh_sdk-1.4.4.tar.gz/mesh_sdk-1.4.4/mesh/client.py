"""
Mesh API Client

This module provides a comprehensive client for interacting with the Mesh API,
including key management, Zero-Knowledge Proofs, chat completions, and usage tracking.
"""

import json
import os
import time
import hashlib
import logging
import requests
import threading
from typing import Dict, Any, Optional, List, Set, Union

# Import configuration
from .config import (
    get_config, is_debug_enabled, get_default_model, get_default_provider,
    is_thinking_enabled, get_default_thinking_budget, get_default_thinking_max_tokens,
    get_default_model_with_override, get_all_config, get_auth_config_endpoint, 
    get_auth_url_endpoint, get_token_exchange_endpoint, get_token_validate_endpoint
)

# Import token manager and auth functions
from .token_manager import store_token, get_token, is_token_valid, clear_token
from .auth import authenticate, refresh_auth_token, authenticate_with_browser

# Import models
from .models import normalize_model_name, get_provider_for_model, MODEL_ALIASES, PROVIDER_MODELS

# Set up logging
logger = logging.getLogger("mesh_client")
logger.setLevel(logging.WARNING)  # Default to WARNING to reduce verbosity
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Disable logging from the requests library
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Default configuration
DEFAULT_CONFIG = {
    "normalize_response": True,
    "original_response": False,
    "return_content_only": True,
    "debug": False
}

class MeshClient:
    """
    Unified client for the Mesh API with key management, ZKP, and chat capabilities
    
    This client provides a unified interface to interact with both the main API server
    and the ZKP microservice. It handles:
    
    1. Basic key management (store/retrieve keys)
    2. Chat functionality with OpenAI and Anthropic models
    3. Usage tracking and billing
    
    Authentication is handled automatically using the backend-managed flow.
    """
    
    def __init__(
        self,
        api_url=None,
        auth_token=None,
        response_format=None,
        auto_refresh=True,
        health_monitor=True
    ):
        """
        Initialize the Mesh client with optional parameters.
        
        Args:
            api_url: URL of the API server (defaults to configured value)
            auth_token: Optional auth token (for backward compatibility)
            response_format: Default response format for chat (dict or string)
            auto_refresh: Whether to automatically refresh tokens
            health_monitor: Whether to monitor token health
        """
        # Configure logging
        self.logger = logging.getLogger("MeshClient")
        self.logger.setLevel(logging.WARNING)  # Default to WARNING
        
        # Set debug mode if enabled
        if is_debug_enabled():
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug("Debug mode enabled")
            logging.getLogger("mesh_client").setLevel(logging.DEBUG)
        
        # Set up token management
        self._auth_token = None
        self._token_data = None
        self.auto_refresh = auto_refresh
        
        # Set server URLs, using config values as defaults
        self.api_url = api_url or get_config("MESH_API_URL")
        
        # Use provided auth token or try to load from storage
        if auth_token:
            self.auth_token = auth_token
        else:
            self._load_token()
        
        # Configure response format
        self.config = DEFAULT_CONFIG.copy()
        if response_format:
            if isinstance(response_format, dict):
                self.config.update(response_format)
            elif response_format.lower() == "string":
                self.config["return_content_only"] = True
            elif response_format.lower() == "dict":
                self.config["return_content_only"] = False
        
        # Initialize user profile attributes
        self._profile_checked = False
        self._user_profile = None
        
        # Start token health monitor if enabled
        if health_monitor and auto_refresh:
            self._start_token_health_monitor()
    
    def _load_token(self) -> None:
        """Load authentication token from secure storage"""
        token_data = get_token()
        if token_data and isinstance(token_data, dict):
            self._token_data = token_data
            self._auth_token = token_data.get("access_token")
            self.logger.debug("Loaded auth token from storage")
    
    def _validate_token(self) -> bool:
        """
        Validate the current authentication token.
        
        First performs a local validation check based on token expiration.
        If the backend supports the /auth/validate endpoint, also validates with the backend.
        
        Returns:
            bool: True if the token is valid, False otherwise
        """
        # No token data or token, not valid
        if not self._token_data or not self._auth_token:
            self.logger.debug("No token data available to validate")
            return False
            
        # First do a local check based on expiration
        if not is_token_valid(self._token_data):
            # Token is locally known to be expired, but we have refresh capability
            if self.auto_refresh and "refresh_token" in self._token_data:
                self.logger.debug("Token expired but refresh capability available")
                return self._refresh_token()
            else:
                self.logger.debug("Token expired and no refresh capability")
                return False
                
        # At this point, we know the token is not expired locally
        # Try to validate with backend if possible
        try:
            # Only attempt backend validation if token passes basic structure check
            if self._auth_token and len(self._auth_token.split('.')) == 3:
                self.logger.debug("Token has valid JWT format (3 parts)")
                
                # Try using the backend /auth/validate endpoint to validate the token
                validate_url = get_token_validate_endpoint()
                headers = {"Authorization": f"Bearer {self._auth_token}"}
                
                try:
                    # Use a short timeout to avoid hanging if endpoint doesn't respond
                    response = requests.get(validate_url, headers=headers, timeout=3)
                    
                    if response.status_code == 200:
                        self.logger.debug("Token validated by backend")
                        return True
                    elif response.status_code == 404:
                        # Endpoint doesn't exist, this is fine - fall back to local validation
                        self.logger.debug("Backend validation endpoint not available, using local validation")
                        return True  # Already passed local validation above
                    elif response.status_code in (401, 403):
                        # Token is actually invalid according to backend
                        self.logger.debug("Backend rejected token as invalid")
                        if self.auto_refresh and "refresh_token" in self._token_data:
                            self.logger.debug("Attempting token refresh after validation failure")
                            return self._refresh_token()
                        return False
                    else:
                        # Other error, fall back to local validation
                        self.logger.debug(f"Unexpected response from validation endpoint: {response.status_code}")
                        return True  # Already passed local validation
                        
                except requests.RequestException as e:
                    # Connection error, can't reach validation endpoint
                    self.logger.debug(f"Could not connect to validation endpoint: {str(e)}")
                    return True  # Fall back to local validation which already passed
            else:
                self.logger.debug("Token does not have valid JWT format")
                return False
                
        except Exception as e:
            self.logger.warning(f"Error during token validation: {str(e)}")
            # Default to local expiration check which already passed
            return True
    
    def _refresh_token(self) -> bool:
        """
        Refresh the authentication token.
        
        Returns:
            bool: True if refresh succeeded, False otherwise
        """
        if not self._token_data or "refresh_token" not in self._token_data:
            self.logger.debug("No refresh token available")
            return False
        
        refresh_token = self._token_data.get("refresh_token")
        if not refresh_token:
            self.logger.debug("Refresh token is empty")
            return False
        
        self.logger.debug("Attempting to refresh token")
        
        # Try to refresh the token
        try:
            new_token_data = refresh_auth_token(refresh_token=refresh_token)
            
            if new_token_data and "access_token" in new_token_data:
                # Update the token data and auth token
                self._token_data = new_token_data
                self._auth_token = new_token_data.get("access_token")
                
                # Store the new token
                store_token(new_token_data)
                
                self.logger.debug("Successfully refreshed token")
                return True
            else:
                self.logger.warning("Token refresh failed")
                return False
        except Exception as e:
            self.logger.warning(f"Error during token refresh: {str(e)}")
            return False
    
    def _authenticate(self) -> bool:
        """
        Authenticate with the backend.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            # Try to authenticate
            token_data = authenticate()
            
            if token_data and "access_token" in token_data:
                # Update the token data and auth token
                self._token_data = token_data
                self._auth_token = token_data.get("access_token")
                
                self.logger.debug("Authentication successful")
                return True
            else:
                self.logger.warning("Authentication failed")
                return False
        except Exception as e:
            self.logger.warning(f"Error during authentication: {str(e)}")
            return False
    
    @property
    def auth_token(self) -> str:
        """Get the authentication token"""
        return self._auth_token
    
    @auth_token.setter
    def auth_token(self, value: str):
        """Set the authentication token and persist it to secure storage"""
        self._auth_token = value
        
        # Store the token in the token manager
        if value:
            # Create minimal token data if we only have the token string
            expires_at = time.time() + 3600  # Default expiry of 1 hour
            token_data = {
                "access_token": value,
                "expires_at": expires_at
            }
            
            # Preserve refresh token if we have it
            if self._token_data and "refresh_token" in self._token_data:
                token_data["refresh_token"] = self._token_data["refresh_token"]
                
            # Store in token manager
            store_token(token_data)
            self._token_data = token_data
            
            logger.debug("Stored token in token manager")
    
    def _get_url(self, endpoint: str) -> str:
        """
        Get the full URL for an API endpoint
        
        Args:
            endpoint: The endpoint path (e.g., '/v1/chat')
            
        Returns:
            str: The full URL
        """
        # Ensure endpoint starts with a slash
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
            
        # Looking at server.js, all endpoints are properly mapped to /api/v1/...
        # Just ensure we are using the standardized paths
        if endpoint.startswith('/api/v1/'):
            # Already using the standardized API path, nothing to change
            pass
        elif endpoint == '/chat/completions':
            endpoint = '/api/v1/chat/completions'
        elif endpoint == '/completions':
            endpoint = '/api/v1/completions'
        elif endpoint == '/storeKey':
            endpoint = '/api/v1/storeKey'
        elif endpoint == '/getKey':
            endpoint = '/api/v1/getKey'
        elif endpoint == '/listKeys':
            endpoint = '/api/v1/listKeys'
        
        # Log for debugging
        logger.debug(f"Using endpoint: {endpoint}")
        
        return f"{self.api_url}{endpoint}"
    
    def _ensure_authenticated(self) -> bool:
        """
        Make sure we're authenticated to the service
        
        This method will:
        1. Check if we have a valid token
        2. If not, try to refresh the token
        3. If that fails, initiate the authentication flow
        
        Returns:
            bool: True if authentication succeeded
        """
        # If we're already authenticated with a valid token, we're done
        if self._validate_token():
            self.logger.debug("Already authenticated with valid token")
            return True
            
        self.logger.info("No valid token, trying authentication")
        
        # Try to authenticate
        return self._authenticate()
    
    def clear_token(self) -> bool:
        """
        Clear the stored authentication token
        
        This is useful for testing authentication flows or logging out.
        
        Returns:
            bool: True if token was cleared successfully
        """
        try:
            # Clear in-memory token
            self._token_data = None
            self._auth_token = None
            
            # Clear stored token
            clear_token()
            
            self.logger.info("Token cleared successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error clearing token: {str(e)}")
            return False
    
    def _get_headers(self, additional_headers=None) -> Dict[str, str]:
        """
        Get headers with authentication if available
        
        Args:
            additional_headers: Additional headers to include
            
        Returns:
            dict: Headers with authentication if available
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add auth token if available
        if self._auth_token:
            # Make sure token doesn't have any accidental whitespace
            token = self._auth_token.strip()
            headers["Authorization"] = f"Bearer {token}"
            
        else:
            logger.warning("No authentication token available for request")
        
        # Add additional headers
        if additional_headers:
            headers.update(additional_headers)
            
        return headers
    
    def _start_token_health_monitor(self):
        """Start background thread to monitor token health"""
        def monitor_token_health():
            """Background thread to monitor token health"""
            while True:
                try:
                    # Check if we need to refresh the token
                    # Only refresh if we have less than 5 minutes left
                    if self._token_data and "expires_at" in self._token_data:
                        expires_at = self._token_data["expires_at"]
                        now = time.time()
                        time_to_expiry = expires_at - now
                        
                        if time_to_expiry < 300:  # Less than 5 minutes
                            self.logger.debug("Token about to expire, refreshing...")
                            self._refresh_token()
                except Exception as e:
                    self.logger.error(f"Error in token health monitor: {str(e)}")
                
                # Sleep for 1 minute
                time.sleep(60)
        
        # Start the monitor thread
        monitor_thread = threading.Thread(target=monitor_token_health)
        monitor_thread.daemon = True
        monitor_thread.start()
    
    def _ensure_user_registered(self) -> Dict[str, Any]:
        """
        Ensure the user is registered with the backend
        
        This method:
        1. Gets the user profile from the backend
        2. Stores it in memory for later use
        
        Returns:
            dict: User profile if successful, None otherwise
        """
        # Return cached profile if we already checked
        if self._profile_checked and self._user_profile:
            return self._user_profile
        
        # Make sure we're authenticated
        if not self._ensure_authenticated():
            self.logger.error("Could not authenticate to get user profile")
            return None
        
        # Get the user profile from the backend
        try:
            profile_url = f"{self.api_url}/auth/profile"
            headers = self._get_headers()
            
            response = requests.get(profile_url, headers=headers)
            if response.status_code == 200:
                profile_data = response.json()
                self.logger.debug(f"Received user profile data: {profile_data}")
                self._user_profile = profile_data
                self._profile_checked = True
                
                # Log the structure to help with debugging
                if 'profile' in profile_data:
                    self.logger.debug("Profile data has nested 'profile' key")
                if 'id' in profile_data:
                    self.logger.debug("Profile data has 'id' key at root level")
                elif profile_data.get('profile', {}).get('id'):
                    self.logger.debug("Profile data has 'id' key in nested 'profile'")
                    
                return self._user_profile
            else:
                self.logger.warning(f"Failed to get user profile: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Error getting user profile: {str(e)}")
            return None
    
    # =========================
    # Key Management Methods
    # =========================
    
    def store_key(self, key_name: str = None, key_value: str = None, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Store a key in the Mesh API
        
        Args:
            key_name: Name of the key (will be stored as {userId}_{key_name})
            key_value: Value of the key to store
            user_id: Optional User ID to associate with the key. If not provided, extracted from auth token.
            
        Returns:
            dict: Result of the operation
        """
        # Validate required parameters
        if not key_name or not key_value:
            return {
                "success": False,
                "error": "Missing required parameters: key_name and key_value must be provided"
            }
            
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            return {
                "success": False,
                "error": "Authentication failed",
                "details": "Could not authenticate with Auth0"
            }
        
        # Get user profile to extract user ID if not provided
        if not user_id:
            if not self._user_profile:
                self._ensure_user_registered()
            
            # Debug the user profile
            self.logger.debug(f"User profile: {self._user_profile}")
            
            if self._user_profile and 'id' in self._user_profile:
                user_id = self._user_profile.get('id')
                logger.info(f"Using user ID from profile: {user_id}")
            elif self._user_profile and 'profile' in self._user_profile and 'id' in self._user_profile['profile']:
                # Try the nested profile structure
                user_id = self._user_profile['profile'].get('id')
                logger.info(f"Using user ID from nested profile: {user_id}")
            else:
                return {
                    "success": False,
                    "error": "User ID not provided and could not be extracted from authentication token",
                    "troubleshooting": [
                        "Provide a user_id parameter",
                        "Ensure you are properly authenticated",
                        "Check that the server URL is correct"
                    ]
                }
        
        # Create the storage path: {userId}_{key_name}
        storage_path = f"{user_id}_{key_name}"
        logger.info(f"Storing key with path: {storage_path}")
        
        url = self._get_url("/api/v1/storeKey")
        self.logger.debug(f"Using storeKey URL: {url}")
        
        # Make the request
        headers = self._get_headers()
        payload = {
            "userId": user_id,
            "keyName": storage_path,  # Use the combined path as key name
            "keyValue": key_value
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                # Add our parameters to the response for verification
                result.update({
                    "storagePath": storage_path,
                    "originalKeyName": key_name
                })
                return result
            else:
                # Simple error handling with clean error messages
                error_data = response.json() if response.content else {}
                self.logger.error(f"Failed to store key: {url} → {response.status_code}")
                
                return {
                    "success": False,
                    "error": f"Failed to store key: {response.status_code}",
                    "details": error_data
                }
                
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def get_key(self, key_name: str = None, user_id: Optional[str] = None) -> Optional[str]:
        """
        Get a key from the Mesh API
        
        Args:
            key_name: Name of the key (will be retrieved using {userId}_{key_name})
            user_id: Optional User ID to retrieve key for. If not provided, extracted from auth token.
            
        Returns:
            str: The key value if found, None if not found or error occurs
        """
        # Validate required parameters
        if not key_name:
            logger.error("Missing required parameter: key_name")
            return None
                
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            logger.error("Authentication failed")
            return None
        
        # Get user profile to extract user ID if not provided
        if not user_id:
            if not self._user_profile:
                self._ensure_user_registered()
            
            # Debug the user profile
            self.logger.debug(f"User profile: {self._user_profile}")
            
            if self._user_profile and 'id' in self._user_profile:
                user_id = self._user_profile.get('id')
                logger.info(f"Using user ID from profile: {user_id}")
            elif self._user_profile and 'profile' in self._user_profile and 'id' in self._user_profile['profile']:
                # Try the nested profile structure
                user_id = self._user_profile['profile'].get('id')
                logger.info(f"Using user ID from nested profile: {user_id}")
            else:
                logger.error("Could not determine user ID")
                return None
        
        # Create the storage path: {userId}_{key_name}
        storage_path = f"{user_id}_{key_name}"
        logger.info(f"Retrieving key with path: {storage_path}")
        
        # Make the request
        url = self._get_url("/api/v1/getKey")
        self.logger.debug(f"Using getKey URL: {url}")
        headers = self._get_headers()
        params = {
            "userId": user_id,
            "keyName": storage_path  # Use the combined path as key name
        }
        
        try:
            response = requests.get(
                url,
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Return None if request failed
                if not result.get("success"):
                    logger.warning(f"Key retrieval failed: {result.get('error', 'Unknown error')}")
                    return None
                    
                # Return the key value - handle both response formats
                key_value = result.get("keyValue") or result.get("key")
                if key_value:
                    logger.info(f"Successfully retrieved key for path: {storage_path}")
                    return key_value
                else:
                    logger.warning(f"No key value found in response for path: {storage_path}")
                    return None
            else:
                # Simple error logging
                logger.error(f"Failed to retrieve key: {url} → {response.status_code}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return None
    
    def list_keys(self, user_id: Optional[str] = None) -> List[str]:
        """
        List all keys stored for a user
        
        Args:
            user_id: Optional User ID to list keys for. If not provided, extracted from auth token.
            
        Returns:
            List[str]: A list of key names (without the user_id prefix)
        """
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            logger.error("Authentication failed")
            return []
        
        # Get user profile to extract user ID if not provided
        if not user_id:
            if not self._user_profile:
                self._ensure_user_registered()
            
            # Debug the user profile
            self.logger.debug(f"User profile for list_keys: {self._user_profile}")
            
            if self._user_profile and 'id' in self._user_profile:
                user_id = self._user_profile.get('id')
                logger.info(f"Using user ID from profile: {user_id}")
            elif self._user_profile and 'profile' in self._user_profile and 'id' in self._user_profile['profile']:
                # Try the nested profile structure
                user_id = self._user_profile['profile'].get('id')
                logger.info(f"Using user ID from nested profile: {user_id}")
            else:
                logger.error("Could not determine user ID")
                return []
        
        # Make the request
        url = self._get_url("/api/v1/listKeys")
        self.logger.debug(f"Using listKeys URL: {url}")
        headers = self._get_headers()
        params = {"userId": user_id}
        
        try:
            response = requests.get(
                url,
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract keys from response
                keys = result.get("keys", [])
                
                # Strip the user ID prefix from the keys
                prefix = f"{user_id}_"
                stripped_keys = []
                
                for key in keys:
                    if key.startswith(prefix):
                        stripped_keys.append(key[len(prefix):])
                    else:
                        stripped_keys.append(key)
                
                return stripped_keys
            else:
                # Simple error logging
                logger.error(f"Failed to list keys: {url} → {response.status_code}")
                return []
                
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return []
    
    # =========================
    # Chat Methods
    # =========================
    
    def chat(
        self, 
        message: Union[str, List[Dict[str, str]]], 
        model: Optional[str] = None, 
        provider: Optional[str] = None,
        **kwargs
    ) -> Union[Dict[str, Any], str]:
        """
        Send a chat message to an AI model
        
        This method supports both string messages and message arrays.
        
        Args:
            message: The message to send (string or message array)
            model: The model to use (e.g. "gpt-4", "claude-3-5-sonnet")
            provider: The provider to use (e.g. "openai", "anthropic")
            **kwargs: Additional options for the chat request
            
        Returns:
            Union[Dict[str, Any], str]: The chat response
        """
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            raise Exception("Authentication failed")
        
        # Determine provider and model
        provider = (provider or get_default_provider()).lower()
        
        if model:
            # Normalize the model name if provided
            model = normalize_model_name(model)
        else:
            # Use default model for the provider
            model = get_default_model(provider)
        
        # If provider wasn't specified but model was, infer provider from model
        if not provider and model:
            provider = get_provider_for_model(model)
        
        # Convert string message to message array if needed
        messages = []
        if isinstance(message, str):
            messages = [{"role": "user", "content": message}]
        elif isinstance(message, list):
            messages = message
        else:
            raise ValueError("Message must be a string or a list of message objects")
        
        # Prepare request payload
        payload = {
            "model": model,
            "messages": messages,
            "provider": provider,  # Explicitly include provider
            **kwargs
        }
        
        # Debug log the full payload
        self.logger.debug(f"Chat request payload: {payload}")
        
        # Make the request
        url = self._get_url("/api/v1/chat/completions")
        headers = self._get_headers()
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Format response based on configuration
                # Debug log raw result
                self.logger.debug(f"Raw API response: {result}")
                
                if self.config["return_content_only"]:
                    # Try to extract content from different response formats
                    # 1. Check standard OpenAI format
                    if "choices" in result and len(result["choices"]) > 0:
                        message = result["choices"][0].get("message", {})
                        content = message.get("content", "")
                        if content:
                            return content
                    
                    # 2. Check for direct content field (server might be normalizing responses)
                    if "content" in result:
                        return result["content"]
                        
                    # 3. Try format used by some providers
                    if "message" in result:
                        return result["message"].get("content", "")
                    
                    # If we can't find content in any recognized format, return empty string
                    self.logger.warning(f"Could not extract content from response: {result}")
                    return ""
                else:
                    # Return the full response
                    return result
            else:
                # Create clear error messages
                status_code = response.status_code
                error_msg = f"Chat request failed: {status_code}"
                
                # Log the error
                self.logger.error(f"Request to {url} failed with status {status_code}")
                
                # Try to get more details from the response
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg = f"{error_msg} - {error_data['error'].get('message', '')}"
                        self.logger.error(f"Error details: {error_data['error']}")
                except:
                    pass
                    
                # Raise exception with helpful message
                raise Exception(error_msg)
                
        except requests.RequestException as e:
            self.logger.error(f"Request error: {str(e)}")
            raise Exception(f"Request failed: {str(e)}")
    
    def stream_chat(
        self, 
        message: Union[str, List[Dict[str, str]]], 
        model: Optional[str] = None, 
        provider: Optional[str] = None,
        **kwargs
    ):
        """
        Stream a chat response from an AI model
        
        This method returns a generator that yields response chunks as they arrive.
        
        Args:
            message: The message to send (string or message array)
            model: The model to use (e.g. "gpt-4", "claude-3-5-sonnet")
            provider: The provider to use (e.g. "openai", "anthropic")
            **kwargs: Additional options for the chat request
            
        Yields:
            str: Response chunks as they arrive
        """
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            raise Exception("Authentication failed")
        
        # Determine provider and model
        provider = (provider or get_default_provider()).lower()
        
        if model:
            # Normalize the model name if provided
            model = normalize_model_name(model)
        else:
            # Use default model for the provider
            model = get_default_model(provider)
        
        # If provider wasn't specified but model was, infer provider from model
        if not provider and model:
            provider = get_provider_for_model(model)
        
        # Convert string message to message array if needed
        messages = []
        if isinstance(message, str):
            messages = [{"role": "user", "content": message}]
        elif isinstance(message, list):
            messages = message
        else:
            raise ValueError("Message must be a string or a list of message objects")
        
        # Prepare request payload
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            **kwargs
        }
        
        # Make the request
        url = self._get_url("/api/v1/chat/completions")
        headers = self._get_headers()
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                stream=True
            )
            
            if response.status_code == 200:
                # Process the stream
                content = ""
                for line in response.iter_lines():
                    if line:
                        # Remove "data: " prefix if present
                        line_text = line.decode('utf-8')
                        if line_text.startswith("data: "):
                            line_text = line_text[6:]
                        
                        # Skip any non-JSON lines
                        if not line_text or line_text == "[DONE]":
                            continue
                        
                        try:
                            data = json.loads(line_text)
                            
                            # Extract content from response
                            if "choices" in data and len(data["choices"]) > 0:
                                chunk = data["choices"][0]
                                if "delta" in chunk and "content" in chunk["delta"]:
                                    content_chunk = chunk["delta"]["content"]
                                    content += content_chunk
                                    yield content_chunk
                        except json.JSONDecodeError:
                            # Skip invalid JSON
                            pass
            else:
                error_msg = f"Stream chat request failed: {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = f"{error_msg} - {error_data.get('error', {}).get('message', '')}"
                except:
                    pass
                
                raise Exception(error_msg)
                
        except requests.RequestException as e:
            raise Exception(f"Stream request failed: {str(e)}")