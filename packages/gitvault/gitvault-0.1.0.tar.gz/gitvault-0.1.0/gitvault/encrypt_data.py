import os
import git
import base64
import logging

from git import Repo
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Union

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from gitvault.custom_exceptions import (
    PrivateKeyNotFoundError,
    EncryptionError,
    GitOperationError,
    ConfigurationError,
    SyncConfigurationError
)
from gitvault.cloud_sync import CloudSync, GitSync, SyncType, GitHubAPISync, BitbucketAPISync, GistAPISync

class DataEncryption:
    """
    A class to handle data encryption and Git repository management.
    
    This class provides functionality to encrypt sensitive data using RSA encryption
    and manage the storage of encrypted data in a Git repository.
    
    Attributes:
        repo_path (Path): Path to the Git repository
        private_key_path (Path): Path to the private key file
        ssh_key_path (Path): Path to the SSH key file for Git operations
        git_repo_url (str): URL of the Git repository
        encrypted_file_name (str): Name of the file storing encrypted data
    """
    
    def __init__(
        self,
        repo_path: Optional[Union[str, Path]] = None,
        private_key_path: Optional[Union[str, Path]] = None,
        ssh_key_path: Optional[Union[str, Path]] = None,
        encrypted_file_path: Optional[Union[str, Path]] = None,
        git_repo_url: Optional[str] = None,
        cloud_sync: Optional[CloudSync] = None,
        sync_type: Union[str, SyncType] = SyncType.GIT,  # Updated type hint
        api_url: Optional[str] = None,
        custom_file_url: Optional[str] = None  # New parameter
    ) -> None:
        """
        Initialize the DataEncryption instance.
        
        Args:
            repo_path: Full path to the Git repository
            private_key_path: Path to the private key file
            ssh_key_path: Path to the SSH key file
            encrypted_file_path: Path to the encrypted data file
            git_repo_url: Git repository URL
        """
        # Load environment variables
        load_dotenv()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize and validate paths
        try:
            self.repo_path = Path(repo_path) if repo_path else Path(os.getenv('REPO_PATH'))
            self.private_key_path = Path(private_key_path) if private_key_path else Path(os.getenv('PRIVATE_KEY_PATH'))
            self.ssh_key_path = Path(ssh_key_path) if ssh_key_path else Path(os.getenv('SSH_KEY_PATH'))
            
            # Handle encrypted_file_path as relative or absolute
            raw_key_path = Path(encrypted_file_path) if encrypted_file_path else Path(os.getenv('ENCRYPTED_FILE_PATH'))
            self.key_path = (
                raw_key_path if raw_key_path.is_absolute()
                else self.repo_path / raw_key_path
            )
        except TypeError as e:
            raise ConfigurationError("Missing required path configuration. All paths must be provided either through parameters or environment variables.")
        
        # Set Git repository URL
        self.git_repo_url = git_repo_url or os.getenv('GIT_REPO_URL')
        
        # Validate all required configurations
        missing_configs = []
        if not self.repo_path:
            missing_configs.append("Repository path")
        if not self.private_key_path:
            missing_configs.append("Private key path")
        if not self.ssh_key_path:
            missing_configs.append("SSH key path")
        if not self.key_path:
            missing_configs.append("Encrypted file path")
        if not self.git_repo_url:
            missing_configs.append("Git repository URL")
            
        if missing_configs:
            raise ConfigurationError(
                "Missing required configurations: " + 
                ", ".join(missing_configs) +
                ". Please provide values either through parameters or environment variables."
            )
        
        # Ensure repository directory exists
        self.repo_path.mkdir(parents=True, exist_ok=True)
        
        # Validate key files exist
        if not self.private_key_path.is_file():
            raise PrivateKeyNotFoundError(f"Private key file not found at: {self.private_key_path}")
        if not self.ssh_key_path.is_file():
            raise ConfigurationError(f"SSH key file not found at: {self.ssh_key_path}")

        # Initialize cloud sync based on type if not provided
        if not cloud_sync:
            # Convert string to enum if needed
            if isinstance(sync_type, str):
                try:
                    sync_type = SyncType(sync_type.lower())
                except ValueError:
                    raise SyncConfigurationError(f"Invalid sync type: {sync_type}")

            if sync_type == SyncType.GITHUB:
                owner = os.getenv('GITHUB_OWNER')
                repo = os.getenv('GITHUB_REPO')
                if not (owner and repo):
                    raise SyncConfigurationError("GitHub owner and repo must be set")
                self.cloud_sync = GitHubAPISync(owner, repo, api_url=api_url, 
                                              custom_file_url=custom_file_url)
                
            elif sync_type == SyncType.BITBUCKET:
                workspace = os.getenv('BITBUCKET_WORKSPACE')
                repo = os.getenv('BITBUCKET_REPO')
                if not (workspace and repo):
                    raise SyncConfigurationError("Bitbucket workspace and repo must be set")
                self.cloud_sync = BitbucketAPISync(workspace, repo, api_url=api_url,
                                                 custom_file_url=custom_file_url)
                
            elif sync_type == SyncType.GIST:
                self.cloud_sync = GistAPISync(
                    os.getenv('GIST_ID'),
                    api_url=api_url,
                    custom_file_url=custom_file_url
                )
            elif sync_type == SyncType.GIT:
                if not all([self.repo_path, self.git_repo_url, self.ssh_key_path]):
                    raise SyncConfigurationError("Git sync requires repo path, URL and SSH key")
                self.cloud_sync = GitSync(
                    self.repo_path,
                    self.git_repo_url,
                    self.ssh_key_path
                )
            else:
                raise SyncConfigurationError(f"Unsupported sync type: {sync_type}")
        else:
            self.cloud_sync = cloud_sync

    def load_private_key(self) -> RSAPrivateKey:
        """
        Load the private key from file.
        
        Returns:
            RSAPrivateKey: The loaded private key object
            
        Raises:
            PrivateKeyNotFoundError: If private key file doesn't exist
            EncryptionError: If private key is invalid
        """
        try:
            with open(self.private_key_path, 'rb') as f:
                return serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )
        except FileNotFoundError:
            self.logger.error(f"Private key file not found at {self.private_key_path}")
            raise PrivateKeyNotFoundError(f"Private key file not found at {self.private_key_path}")
        except ValueError as e:
            self.logger.error("Invalid private key format")
            raise EncryptionError(f"Invalid private key format: {str(e)}")

    def encrypt_string(self, message: str, private_key: RSAPrivateKey) -> bytes:
        """
        Encrypt a string using RSA encryption.
        
        Args:
            message: The string to encrypt
            private_key: RSA private key object
            
        Returns:
            bytes: Encrypted data
            
        Raises:
            EncryptionError: If encryption fails
        """
        try:
            public_key = private_key.public_key()
            return public_key.encrypt(
                message.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except Exception as e:
            raise EncryptionError(f"Encryption failed: {str(e)}")

    def save_encrypted_data(self, encrypted_data: bytes) -> None:
        """
        Save encrypted data to file in base64 format.
        
        Args:
            encrypted_data: The encrypted bytes to save
        """
        base64_data = base64.b64encode(encrypted_data)
        self.key_path.write_text(base64_data.decode('utf-8'))
        self.logger.info(f"Encrypted data saved to {self.key_path}")

    def git_push_changes(self) -> None:
        """
        Push encrypted data to cloud storage.
        
        Raises:
            GitOperationError: If cloud sync operations fail
        """
        try:
            # Repository is already initialized in encrypt_and_store
            success = self.cloud_sync.sync_to_cloud(
                self.key_path,
                "Updated encrypted data"
            )
            
            if not success:
                raise GitOperationError("Failed to sync changes to cloud")
                
            self.logger.info("Successfully pushed changes to cloud")
            
        except Exception as e:
            self.logger.error(f"Error in cloud sync: {str(e)}")
            raise GitOperationError(f"Cloud sync failed: {str(e)}")

    def encrypt_and_store(self, secret_data: str) -> None:
        """
        Main method to encrypt data and store it in the cloud.
        """
        try:
            # Create parent directories if needed
            if isinstance(self.cloud_sync, GitSync):
                self.cloud_sync._setup_repo()
            if not self.key_path.parent.exists():
                self.key_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Encrypt and save data
            private_key = self.load_private_key()
            encrypted_data = self.encrypt_string(secret_data, private_key)
            self.save_encrypted_data(encrypted_data)
            
            # Sync to cloud
            self.git_push_changes()
            
        except (PrivateKeyNotFoundError, EncryptionError, GitOperationError) as e:
            self.logger.error(f"Operation failed: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise
