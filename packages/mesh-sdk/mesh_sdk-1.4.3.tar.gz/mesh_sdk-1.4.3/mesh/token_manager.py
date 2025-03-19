"""
Token Manager for Mesh SDK

This module handles secure storage and retrieval of authentication tokens
using the system keychain or secure storage.
"""

import os
import json
import time
import logging
import keyring
from pathlib import Path

# Configure logging
logger = logging.getLogger("mesh.token_manager")

# Constants for token storage
SERVICE_NAME = "mesh-sdk"
USERNAME = "default"
TOKEN_FILE_PATH = os.path.join(str(Path.home()), ".mesh", "token.json")

def _ensure_dir_exists(file_path: str) -> None:
    """Ensure the directory for a file exists"""
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def store_token(token_data: dict) -> bool:
    """Store token data securely
    
    Args:
        token_data: Token data including access_token, expires_at, etc.
        
    Returns:
        bool: True if token was stored successfully
    """
    try:
        # First try to store in system keychain
        token_json = json.dumps(token_data)
        try:
            keyring.set_password(SERVICE_NAME, USERNAME, token_json)
            logger.debug("Token stored in system keychain")
            return True
        except Exception as e:
            logger.warning(f"Could not store token in keychain: {str(e)}")
            
            # Fall back to file storage with best-effort security
            _ensure_dir_exists(TOKEN_FILE_PATH)
            with open(TOKEN_FILE_PATH, "w") as f:
                json.dump(token_data, f)
            # Set proper permissions on the file
            try:
                os.chmod(TOKEN_FILE_PATH, 0o600)  # Read/write only for the owner
            except Exception:
                pass  # Best effort
            logger.debug("Token stored in file")
            return True
    except Exception as e:
        logger.error(f"Failed to store token: {str(e)}")
        return False

def get_token() -> dict:
    """Retrieve token data
    
    Returns:
        dict: Token data or None if not found
    """
    # First try system keychain
    try:
        token_json = keyring.get_password(SERVICE_NAME, USERNAME)
        if token_json:
            return json.loads(token_json)
    except Exception as e:
        logger.warning(f"Could not retrieve token from keychain: {str(e)}")
    
    # Fall back to file storage
    try:
        if os.path.exists(TOKEN_FILE_PATH):
            with open(TOKEN_FILE_PATH, "r") as f:
                return json.load(f)
    except Exception as e:
        logger.warning(f"Could not read token from file: {str(e)}")
    
    return None

# Alias for get_token for consistency with naming in other parts of the code
def load_token() -> dict:
    """Alias for get_token() - Retrieve token data
    
    Returns:
        dict: Token data or None if not found
    """
    return get_token()

def clear_token() -> bool:
    """Clear stored token
    
    Returns:
        bool: True if token was cleared successfully
    """
    success = True
    
    # Clear from keychain
    try:
        keyring.delete_password(SERVICE_NAME, USERNAME)
        logger.debug("Token cleared from keychain")
    except Exception as e:
        logger.warning(f"Could not clear token from keychain: {str(e)}")
        success = False
    
    # Clear from file
    if os.path.exists(TOKEN_FILE_PATH):
        try:
            os.remove(TOKEN_FILE_PATH)
            logger.debug("Token cleared from file")
        except Exception as e:
            logger.warning(f"Could not clear token from file: {str(e)}")
            success = False
    
    return success

def is_token_valid(token_data: dict) -> bool:
    """Check if token is still valid
    
    Args:
        token_data: Token data including expires_at
        
    Returns:
        bool: True if token is valid, False otherwise
    """
    if not token_data:
        return False
    
    # Check for access token
    if "access_token" not in token_data:
        return False
    
    # Check for expiration
    expires_at = token_data.get("expires_at", 0)
    
    # Add buffer time to avoid edge cases
    buffer_seconds = 300  # 5 minutes
    return time.time() < expires_at - buffer_seconds