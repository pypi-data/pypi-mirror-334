from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union, Dict
import os
import requests
import base64
import git
from enum import Enum
from .custom_exceptions import GitOperationError

class SyncType(Enum):
    GIT = 'git'
    GITHUB = 'github'
    BITBUCKET = 'bitbucket'
    GIST = 'gist'

class CloudSync(ABC):
    """Base class for cloud synchronization implementations."""
    
    @abstractmethod
    def sync_to_cloud(self, file_path: Path, message: str) -> bool:
        """Sync file to cloud storage."""
        pass
    
    @abstractmethod
    def rollback(self) -> None:
        """Rollback changes if sync fails."""
        pass

    @staticmethod
    def get_env_var(var_name: str, default: str = None) -> str:
        """Get environment variable with global fallback."""
        return os.getenv(f'SYNC_{var_name}', os.getenv(var_name, default))

class GitSync(CloudSync):
    """Git-based cloud sync implementation."""
    
    def __init__(self, repo_path: Path, repo_url: str, ssh_key_path: Path):
        self.repo_path = repo_path
        self.repo_url = repo_url
        self.ssh_key_path = ssh_key_path
        self._last_commit_hash = None
        self._repo = None

    def _setup_repo(self) -> None:
        """Initialize or clone repository."""
        try:
            if not (self.repo_path / '.git').exists():
                git.Repo.clone_from(
                    self.repo_url,
                    self.repo_path,
                    env={'GIT_SSH_COMMAND': f'ssh -i {self.ssh_key_path}'}
                )
                self._repo = git.Repo(self.repo_path)
            elif not self._repo:
                self._repo = git.Repo(self.repo_path)
                
            self._last_commit_hash = self._repo.head.commit.hexsha
            
        except Exception as e:
            raise GitOperationError(f"Failed to setup git repository: {str(e)}")

    def sync_to_cloud(self, file_path: Path, message: str) -> bool:
        """
        Sync file to git repository.
        
        Args:
            file_path: Path to file (absolute or relative to repo)
            message: Commit message
        """
        try:
            if not self._repo:
                raise GitOperationError("Repository not initialized. Call _setup_repo first.")
                
            self._setup_repo()
            
            # Convert to relative path if absolute
            relative_path = file_path.relative_to(self.repo_path) if file_path.is_absolute() else file_path
            
            # Stage and commit
            self._repo.index.add([str(relative_path)])
            self._repo.index.commit(message)
            
            # Push to remote
            origin = self._repo.remote('origin')
            push_info = origin.push()[0]
            
            if push_info.flags & push_info.ERROR:
                self.rollback()
                return False
                
            return True
            
        except Exception as e:
            self.rollback()
            raise GitOperationError(f"Git sync failed: {str(e)}")

    def rollback(self) -> None:
        """Rollback to last sknown good state."""
        if self._last_commit_hash and self._repo:
            self._repo.head.reset(self._last_commit_hash, index=True, working_tree=True)

class APISync(CloudSync):
    """API-based cloud sync implementation."""
    
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self._last_version = None

    def sync_to_cloud(self, file_path: Path, message: str) -> bool:
        """
        Sync file using REST API.
        
        Args:
            file_path: Path to file to sync
            message: Update message/description
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'X-Update-Message': message
                }
                
                response = requests.post(
                    f"{self.api_url}/upload",
                    files=files,
                    headers=headers
                )
                
                if response.status_code == 200:
                    self._last_version = response.json().get('version')
                    return True
                    
                return False
                
        except Exception as e:
            self.rollback()
            raise Exception(f"API sync failed: {str(e)}")

    def rollback(self) -> None:
        """Request version rollback via API if needed."""
        if self._last_version:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            requests.post(
                f"{self.api_url}/rollback",
                json={'version': self._last_version},
                headers=headers
            )

class GitHubAPISync(CloudSync):
    """GitHub API-based sync implementation."""
    
    def __init__(self, repo_owner: str, repo_name: str, auth_token: Optional[str] = None, 
                 api_url: Optional[str] = None, custom_file_url: Optional[str] = None):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.auth_token = auth_token or self.get_env_var('GITHUB_TOKEN')
        self.api_base = api_url or "https://api.github.com"
        self.custom_file_url = custom_file_url
        self._last_sha = None

    def sync_to_cloud(self, file_path: Path, message: str) -> bool:
        try:
            headers = {
                'Authorization': f'token {self.auth_token}',
                'Accept': 'application/vnd.github.v3+json'
            }

            # Use custom URL directly if provided
            file_url = self.custom_file_url or f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path.name}"

            response = requests.get(file_url, headers=headers)
            
            content = base64.b64encode(file_path.read_bytes()).decode('utf-8')
            data = {
                'message': message,
                'content': content,
            }

            if response.status_code == 200:
                # Update existing file
                self._last_sha = response.json()['sha']
                data['sha'] = self._last_sha
                response = requests.put(file_url, headers=headers, json=data)
            else:
                # Create new file
                response = requests.put(file_url, headers=headers, json=data)

            return response.status_code in (200, 201)

        except Exception as e:
            self.rollback()
            raise Exception(f"GitHub API sync failed: {str(e)}")

    def rollback(self) -> None:
        if self._last_sha:
            # Could implement version rollback via GitHub API if needed
            pass

class BitbucketAPISync(CloudSync):
    """Bitbucket API-based sync implementation."""
    
    def __init__(self, workspace: str, repo_slug: str, auth_token: Optional[str] = None, 
                 api_url: Optional[str] = None, custom_file_url: Optional[str] = None):
        self.workspace = workspace
        self.repo_slug = repo_slug
        self.auth_token = auth_token or self.get_env_var('BITBUCKET_TOKEN')
        self.api_base = api_url or "https://api.bitbucket.org/2.0"
        self.custom_file_url = custom_file_url
        self._last_commit = None

    def sync_to_cloud(self, file_path: Path, message: str) -> bool:
        try:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/json'
            }

            content = base64.b64encode(file_path.read_bytes()).decode('utf-8')
            
            # Use custom URL directly if provided
            url = self.custom_file_url or f"{self.api_base}/repositories/{self.workspace}/{self.repo_slug}/src"
            
            files = {file_path.name: content}
            
            response = requests.post(
                url,
                headers=headers,
                data={
                    'message': message,
                    'branch': 'master',
                    **files
                }
            )

            if response.status_code in (200, 201):
                self._last_commit = response.json().get('hash')
                return True
            return False

        except Exception as e:
            self.rollback()
            raise Exception(f"Bitbucket API sync failed: {str(e)}")

    def rollback(self) -> None:
        if self._last_commit:
            # Could implement version rollback via Bitbucket API if needed
            pass

class GistAPISync(CloudSync):
    """GitHub Gist API-based sync implementation."""
    
    def __init__(self, gist_id: Optional[str] = None, auth_token: Optional[str] = None, 
                 api_url: Optional[str] = None, custom_file_url: Optional[str] = None):
        self.gist_id = gist_id
        self.auth_token = auth_token or self.get_env_var('GITHUB_TOKEN')
        self.api_base = api_url or "https://api.github.com"
        self.custom_file_url = custom_file_url
        self._last_version = None

    def sync_to_cloud(self, file_path: Path, message: str) -> bool:
        try:
            headers = {
                'Authorization': f'token {self.auth_token}',
                'Accept': 'application/vnd.github.v3+json'
            }

            content = file_path.read_text()
            files = {file_path.name: {'content': content}}

            # Use custom URL directly if provided
            url = self.custom_file_url or (
                f"{self.api_base}/gists/{self.gist_id}" if self.gist_id 
                else f"{self.api_base}/gists"
            )

            if self.gist_id:
                # Update existing gist
                response = requests.patch(url, headers=headers, json={'files': files})
            else:
                # Create new gist
                data = {
                    'description': message,
                    'public': False,
                    'files': files
                }
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 201:
                    self.gist_id = response.json()['id']

            if response.status_code in (200, 201):
                self._last_version = response.json()['history'][0]['version']
                return True
            return False

        except Exception as e:
            self.rollback()
            raise Exception(f"Gist API sync failed: {str(e)}")

    def rollback(self) -> None:
        if self._last_version and self.gist_id:
            # Could implement version rollback via Gist API if needed
            pass
