"""
GitVault secure data decryption module for encrypted content retrieval from Git providers.

This module provides a robust implementation for fetching and decrypting data
from various Git providers using RSA encryption. It supports different Git
platforms through a plugin-based architecture and handles common encryption
operations securely.

Typical usage example:
    decryptor = DataDecryptor(
        key_url="https://api.git.com/key",
        auth_token="your-token",
        private_key_path="path/to/key.pem",
        fetch_type=FetchType.GITHUB,
        fetcher_options={
            "api_version": "v3",
            "org_name": "my-org",
            "repo_name": "my-repo"
        }
    )
    result = decryptor.fetch_and_decrypt()
    if result.success:
        print(result.data)
"""

import os
import base64
import logging
import binascii

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend

from enum import Enum, auto
from functools import lru_cache
from dataclasses import dataclass
from urllib.parse import urlparse
from gitvault.decorators import handle_exceptions
from typing import Optional, Union, Dict, Any, NoReturn
from gitvault.git_fetch import GitFetch, GithubFetch, BitbucketFetch, GistFetch, GitRepoFetch
from gitvault.custom_exceptions import PrivateKeyNotFoundError, InvalidURLError, InvalidOptionError

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = lambda: None  # provide a no-op function if module is not installed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
load_dotenv()

@dataclass
class DecryptionResult:
    """Container for decryption operation results.
    
    Attributes:
        success: Boolean indicating if the operation was successful.
        data: Decrypted data string if successful, None otherwise.
        error: Error message string if operation failed, None otherwise.
    """
    success: bool
    data: Optional[str] = None
    error: Optional[str] = None

class FetchType(Enum):
    """Supported Git provider types.
    
    This enum defines the supported Git provider types for fetching encrypted data.
    Each type corresponds to a specific implementation of the GitFetch interface.

    Available types:
        GITREPO: For standard Git repositories
        GITHUB: For GitHub repositories and enterprise instances
        BITBUCKET: For Bitbucket Cloud and Server
        GLIST: For GitHub Gist
    """
    GITREPO = auto()
    GITHUB = auto()
    BITBUCKET = auto()
    GLIST = auto()

class DataDecryptor:
    """Handles secure fetching and decryption of encrypted data from Git providers.
    
    This class provides a secure way to fetch encrypted data from Git providers
    and decrypt it using RSA private key encryption. It supports different Git
    platforms through a plugin-based fetcher system.
    
    Attributes:
        private_key_path: Path to the RSA private key file.
        key_url: URL to fetch the encrypted data from.
        auth_token: Authentication token for Git provider API.
        timeout: Request timeout in seconds.
        fetcher: Instance of GitFetch implementation for specific Git provider.
        fetcher_options: Optional[Dict[str, Any]]
            Additional configuration parameters for the GitFetch instance
            appropriate to the chosen fetch_type.
    
    Fetcher Options by Type:
        GITREPO:
            - repo_path: str - Local repository path or remote URL
            - branch: str - Branch name (default: 'main')
            - file_path: str - Path to encrypted file in repository
            - ssh_key: Optional[str] - Path to SSH key if required
            - api_url: Optional[str] - Override API endpoint URL
            - api_base: Optional[str] - Base API URL if not default
            - repo_url: Optional[str] - Remote repository URL
            
        GITHUB:
            - api_version: str - GitHub API version (default: 'v3')
            - org_name: Optional[str] - GitHub organization name
            - repo_name: str - Repository name
            - branch: Optional[str] - Branch name (default: 'main')
            - enterprise_url: Optional[str] - GitHub Enterprise URL if applicable
            - api_url: Optional[str] - Override API endpoint URL
            - api_base: Optional[str] - Base API URL if not default
            - repo_url: Optional[str] - Remote repository URL
            
        BITBUCKET:
            - workspace: str - Bitbucket workspace ID
            - repo_slug: str - Repository slug
            - api_version: str - API version (default: '2.0')
            - server_url: Optional[str] - Bitbucket Server URL if applicable
            - project_key: Optional[str] - Project key for Bitbucket Server
            - api_url: Optional[str] - Override API endpoint URL
            - api_base: Optional[str] - Base API URL if not default
            - repo_url: Optional[str] - Remote repository URL
            
        GLIST:
            - gist_id: str - GitHub Gist ID
            - filename: str - Name of the file in the gist
            - raw: bool - Whether to fetch raw content (default: True)
            - api_url: Optional[str] - Override API endpoint URL
            - api_base: Optional[str] - Base API URL if not default
            - repo_url: Optional[str] - Remote repository URL
    
    Raises:
        PrivateKeyNotFoundError: If private key file is not found or not readable.
        InvalidURLError: If provided URL is invalid.
        InvalidOptionError: If fetcher options are invalid or missing required fields.
        ValueError: If required parameters are missing or invalid.
    """
    
    _FETCHER_MAP = {
        FetchType.GITREPO: GitRepoFetch,
        FetchType.GITHUB: GithubFetch,
        FetchType.BITBUCKET: BitbucketFetch,
        FetchType.GLIST: GistFetch
    }
    
    def __init__(
        self, 
        key_url: str,
        auth_token: str,
        private_key_path: str,
        fetch_type: FetchType,
        fetcher_options: Optional[Dict[str, Any]] = None,
        timeout: int = 30
    ):
        """Initialize DataDecryptor with enhanced validation.
        
        Args:
            key_url (str): URL to fetch the encrypted data from.
            auth_token (str): Authentication token for Git provider API.
            private_key_path (str): Path to the RSA private key file.
            fetch_type (FetchType): Type of Git provider to fetch from.
            fetcher_options (Optional[Dict[str, Any]]): Additional
                configuration parameters for the GitFetch instance.
                This can include repository details, authentication
                settings, or any plugin-based arguments.
            timeout (int): Request timeout in seconds (default: 30).
        """
        if not isinstance(key_url, str) or not key_url.strip():
            raise InvalidURLError("key_url must be a non-empty string")
        if not isinstance(auth_token, str) or not auth_token.strip():
            raise ValueError("auth_token must be a non-empty string")
        if not isinstance(private_key_path, str):
            raise ValueError("private_key_path must be a string")
        if not isinstance(fetch_type, FetchType):
            raise ValueError("fetch_type must be a FetchType enum")

        self._validate_url(key_url)
        self.timeout = timeout
        self.private_key_path = private_key_path
        self.key_url = key_url or os.environ.get('KEY_URL', None)
        self.auth_token = auth_token or os.environ.get('AUTH_TOKEN', None)
        self.fetcher = self._create_fetcher(fetch_type, fetcher_options or {})
        
        self._validate_init()

    def _validate_url(self, url: str) -> None:
        """Validate URL format and scheme."""
        try:
            parsed = urlparse(url)
            if not all([parsed.scheme in ['http', 'https'], parsed.netloc]):
                raise InvalidURLError("Invalid URL scheme or format")
        except Exception as e:
            raise InvalidURLError(f"Invalid URL: {str(e)}")

    def _validate_fetcher_options(self, fetch_type: FetchType, options: Dict[str, Any]) -> None:
        """Validate required options for each fetcher type."""
        required_options = {
            FetchType.GITREPO: ['repo_path', 'file_path'],
            FetchType.GITHUB: ['repo_name'],
            FetchType.BITBUCKET: ['workspace', 'repo_slug'],
            FetchType.GLIST: ['gist_id']
        }

        missing = [opt for opt in required_options[fetch_type] if opt not in options]
        if missing:
            raise InvalidOptionError(f"Missing required options for {fetch_type.name}: {', '.join(missing)}")

    def _create_fetcher(self, fetch_type: FetchType, options: Dict[str, Any]) -> GitFetch:
        """Create fetcher with enhanced validation."""
        if not isinstance(options, dict):
            raise InvalidOptionError("fetcher_options must be a dictionary")

        self._validate_fetcher_options(fetch_type, options)
        options['timeout'] = self.timeout  # Add timeout to fetcher options

        fetcher_class = self._FETCHER_MAP.get(fetch_type)
        if not fetcher_class:
            raise ValueError(f"Unsupported fetch type: {fetch_type}")
        
        try:
            return fetcher_class(**options)
        except InvalidOptionError as e:  # Handle InvalidOptionError
            logger.error(f"Invalid options for fetcher: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize fetcher: {e}")
            raise ValueError(f"Failed to initialize {fetch_type.name} fetcher: {str(e)}")

    def _validate_init(self) -> None:
        """Enhanced initialization validation."""
        if not os.path.exists(self.private_key_path):
            raise PrivateKeyNotFoundError(f"Private key not found: {self.private_key_path}")
        if not os.path.isfile(self.private_key_path):
            raise PrivateKeyNotFoundError(f"Private key path is not a file: {self.private_key_path}")
        if not os.access(self.private_key_path, os.R_OK):
            raise PrivateKeyNotFoundError(f"Private key file is not readable: {self.private_key_path}")
        if not isinstance(self.fetcher, GitFetch):
            raise ValueError("Fetcher must be an instance of GitFetch")
        if not self.key_url or not self.auth_token:
            raise ValueError("key_url and auth_token are required")

    @lru_cache(maxsize=1)
    def _load_private_key(self) -> rsa.RSAPrivateKey:
        """Loads and caches the RSA private key from file.
        
        Returns:
            RSAPrivateKey: Loaded private key object.
            
        Raises:
            PrivateKeyNotFoundError: If key file cannot be loaded.
        """
        try:
            with open(self.private_key_path, 'rb') as f:
                return serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )
        except Exception as e:
            logger.error(f"Failed to load private key: {e}")
            raise PrivateKeyNotFoundError(f"Failed to load private key: {str(e)}")

    @handle_exceptions(logger)
    def decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypts the provided encrypted data using RSA private key.
        
        Args:
            encrypted_data: Bytes object containing the encrypted data.
            
        Returns:
            str: Decrypted data as UTF-8 string.
            
        Raises:
            DecryptionError: If decryption fails.
        """
        private_key = self._load_private_key()
        decrypted = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode('utf-8')

    @handle_exceptions(logger)
    def fetch_and_decrypt(self, url: Optional[str] = None, auth_token: Optional[str] = None) -> DecryptionResult:
        """Enhanced fetch and decrypt with better error handling."""
        try:
            _url = url or self.key_url
            _auth_token = auth_token or self.auth_token

            if url:  # Validate custom URL if provided
                self._validate_url(url)

            encrypted_text = self.fetcher.fetch_data(_url, _auth_token)
            if not encrypted_text:
                return DecryptionResult(success=False, error="No data received from fetcher")

            try:
                encrypted_data = base64.b64decode(encrypted_text)
            except binascii.Error as e:
                return DecryptionResult(success=False, error=f"Invalid base64 data: {str(e)}")

            if not encrypted_data:
                return DecryptionResult(success=False, error="Decoded data is empty")

            try:
                decrypted_data = self.decrypt_data(encrypted_data)
                if not decrypted_data:
                    return DecryptionResult(success=False, error="Decryption produced empty result")
                return DecryptionResult(success=True, data=decrypted_data)
            except Exception as e:
                return DecryptionResult(success=False, error=f"Decryption failed: {str(e)}")

        except Exception as e:
            logger.error(f"Fetch and decrypt failed: {str(e)}")
            return DecryptionResult(success=False, error=str(e))

    def __repr__(self) -> str:
        return f"DataDecryptor(key_path='{self.private_key_path}', fetcher={self.fetcher.__class__.__name__})"
