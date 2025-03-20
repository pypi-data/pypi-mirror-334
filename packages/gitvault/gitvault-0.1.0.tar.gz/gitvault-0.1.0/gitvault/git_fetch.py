import git
import base64
import urllib3
import requests

from enum import Enum
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from .custom_exceptions import GitOperationError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FetchType(Enum):
    GIT = 'git'
    GITHUB = 'github'
    BITBUCKET = 'bitbucket'
    GIST = 'gist'

class GitFetch(ABC):
    """Abstract base class for various Git fetch implementations.

    Attributes:
        auth_token: Optional string for token-based authentication.
        api_url: Optional override or complete API endpoint URL.
        api_base: Optional base URL for the Git provider.
        repo_path: Local filesystem path where repository is cloned or located.
        repo_url: Remote Git repository URL.
        ssh_key_path: Path to SSH key file for authenticated cloning/pulling.
        _last_response: Stores the last HTTP or Git response object from fetch calls.
        _repo: Reference to the local git.Repo instance once initialized.
    """

    def __init__(self, auth_token: Optional[str] = None, api_url: Optional[str] = None,
                 repo_path: Optional[str] = None, repo_url: Optional[str] = None, 
                 api_base: Optional[str] = None, ssh_key_path: Optional[str] = None):
        self.auth_token = auth_token  # Used for token-based auth in HTTP requests
        self.api_url = api_url        # Allows overriding or specifying full endpoint
        self.api_base = api_base      # Used to store the base API URL if not default
        self.repo_path = Path(repo_path) if repo_path else None  # Local repo path
        self.repo_url = repo_url      # Remote repository URL (HTTPS/SSH)
        self.ssh_key_path = Path(ssh_key_path) if ssh_key_path else None  # SSH key file path
        self._last_response = None    # For storing the last response (HTTP or Git)
        self._repo = None             # For storing a reference to git.Repo instance

    def setup_repo(self) -> None:
        """Initialize or clone repository if repo_path and repo_url are provided."""
        if not all([self.repo_path, self.repo_url]):
            return

        try:
            if not (self.repo_path / '.git').exists():
                git_env = {'GIT_SSH_COMMAND': f'ssh -i {self.ssh_key_path}'} if self.ssh_key_path else None
                git.Repo.clone_from(self.repo_url, self.repo_path, env=git_env)
                self._repo = git.Repo(self.repo_path)
            elif not self._repo:
                self._repo = git.Repo(self.repo_path)
        except Exception as e:
            raise GitOperationError(f"Failed to setup git repository: {str(e)}")

    @abstractmethod
    def fetch_data(self, path: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Fetch data from the given path with optional parameters."""
        pass

class GitRepoFetch(GitFetch):
    """Git repository-based fetch implementation."""
    
    def __init__(self, auth_token: Optional[str] = None, repo_path: Optional[str] = None,
                 repo_url: Optional[str] = None, ssh_key_path: Optional[str] = None):
        super().__init__(auth_token=auth_token, repo_path=repo_path,
                        repo_url=repo_url, ssh_key_path=ssh_key_path)

    def fetch_data(self, path: str, params: Optional[Dict[str, Any]] = None) -> str:
        try:
            self.setup_repo()
            file_path = self.repo_path / path
            if not file_path.exists():
                raise GitOperationError(f"File not found: {path}")
            return file_path.read_text().strip()
        except Exception as e:
            raise GitOperationError(f"Git fetch failed: {str(e)}")

class GithubFetch(GitFetch):
    def __init__(self, repo_owner: str, repo_name: str, auth_token: Optional[str] = None,
                 api_base: Optional[str] = "https://api.github.com", api_url: Optional[str] = None):
        super().__init__(auth_token=auth_token, api_url=api_url, api_base=api_base)
        self.repo_owner = repo_owner
        self.repo_name = repo_name

    def fetch_data(self, path: str, params: Optional[Dict[str, Any]] = None) -> str:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            'Authorization': f'token {self.auth_token}'
        }
        
        url = self.api_url or f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/contents/{path}"
        
        try:
            response = requests.get(url, headers=headers, params=params)
            self._last_response = response
            
            if response.status_code != 200:
                raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")
            
            content = response.json().get('content', '')
            return base64.b64decode(content).decode('utf-8').strip()
        except Exception as e:
            raise Exception(f"GitHub fetch failed: {str(e)}")

class BitbucketFetch(GitFetch):
    def __init__(self, workspace: str, repo_slug: str, auth_token: Optional[str] = None,
                 api_base: Optional[str] = "https://api.bitbucket.org/2.0", api_url: Optional[str] = None):
        super().__init__(auth_token=auth_token, api_url=api_url, api_base=api_base)
        self.workspace = workspace
        self.repo_slug = repo_slug

    def fetch_data(self, path: str, params: Optional[Dict[str, Any]] = None) -> str:
        headers = {
            "Accept": "application/json",
            'Authorization': f'Bearer {self.auth_token}'
        }
        
        url = self.api_url or f"{self.api_base}/repositories/{self.workspace}/{self.repo_slug}/src/master/{path}"
        
        try:
            response = requests.get(url, verify=False, headers=headers, params=params)
            self._last_response = response
            
            if response.status_code != 200:
                raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")
            
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Bitbucket fetch failed: {str(e)}")

class GistFetch(GitFetch):
    def __init__(self, gist_id: str, auth_token: Optional[str] = None,
                 api_base: Optional[str] = "https://api.github.com", api_url: Optional[str] = None):
        super().__init__(auth_token=auth_token, api_url=api_url, api_base=api_base)
        self.gist_id = gist_id

    def fetch_data(self, path: str, params: Optional[Dict[str, Any]] = None) -> str:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            'Authorization': f'token {self.auth_token}'
        }
        
        url = self.api_url or f"{self.api_base}/gists/{self.gist_id}"
        
        try:
            response = requests.get(url, headers=headers, params=params)
            self._last_response = response
            
            if response.status_code != 200:
                raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")
            
            files = response.json().get('files', {})
            if path in files:
                return files[path]['content'].strip()
            raise Exception(f"File {path} not found in gist")
        except Exception as e:
            raise Exception(f"Gist fetch failed: {str(e)}")
