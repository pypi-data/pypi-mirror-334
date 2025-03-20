# GitVault

## Overview
GitVault enables encryption and decryption of sensitive data, plus optional sync with cloud providers (Git, GitHub, Bitbucket, or Gist). It leverages RSA and custom exceptions for robust error handling.

## Installation
1. Install Python 3.7+ and pip.
2. Clone or download this repository.
3. (Optional) Create and activate a virtual environment.
4. Install dependencies:  
   ```
   pip install -r requirements.txt
   ```

## Main Components
- **DataEncryption**: Encrypts data, saves it locally, and optionally pushes changes to a remote repository.  
- **DataDecryptor**: Fetches and decrypts data from supported Git providers.  
- **CloudSync Implementations**:  
  - **GitSync**: Sync via a traditional Git repository using SSH.  
  - **GitHubAPISync**: Sync through GitHub's REST API.  
  - **BitbucketAPISync**: Sync using Bitbucket Cloud or Bitbucket Server API.  
  - **GistAPISync**: Sync through GitHub Gist.  

## Usage Example
1. Set environment variables for paths and tokens:
   ```bash
   PRIVATE_KEY_PATH=/path/to/private_key.pem
   REPO_PATH=/path/to/local/repo
   GITHUB_TOKEN=your_github_token
   ```

2. Encrypt data:
   ```python
   # 🚀 Let's import DataEncryption
   from gitvault.encrypt_data import DataEncryption
   
   # Basic local encryption
   encrypter = DataEncryption(
       private_key_path="/path/to/private.pem",
       repo_path="/path/to/local/repo"
   )
   encrypter.encrypt_and_store("super-secret-password")  # 🔒 store secret
   
   # With GitHub sync
   encrypter = DataEncryption(
       private_key_path="/path/to/private.pem",
       sync_type="github",
       fetcher_options={
           "repo_owner": "your-username",
           "repo_name": "your-repo",
           "auth_token": "your-github-token"
       }
   )
   encrypter.encrypt_and_store("database-password")      # 🤫 hush hush
   ```

3. Decrypt data:
   ```python
   # 🔓 Time to decrypt
   from gitvault.decrypt_data import DataDecryptor, FetchType
   
   # Decrypt from GitHub
   decryptor = DataDecryptor(
       key_url="path/to/encrypted/file",
       auth_token="your-github-token",
       private_key_path="/path/to/private.pem",
       fetch_type=FetchType.GITHUB,
       fetcher_options={
           "repo_owner": "your-username",
           "repo_name": "your-repo"
       }
   )
   
   # Fetch and decrypt
   result = decryptor.fetch_and_decrypt()
   if result.success:
       print("Decrypted:", result.data)  # 🎉 success
   else:
       print("Error:", result.error)     # 😞 handle error
   ```

## Detailed Cloud Sync Options
Below is an overview of how each cloud sync implementation can be configured.

### GitSync
- Relies on a local git environment and SSH key for authentication.
- Environment Variables (if paths or URLs not passed in):  
  - `REPO_PATH`: Local path to repository  
  - `GIT_REPO_URL`: Remote repository URL  
  - `SSH_KEY_PATH`: Path to SSH key  
- Class reference: `GitSync(repo_path, repo_url, ssh_key_path)`

### GitHubAPISync
- Uses GitHub’s REST API; requires a GitHub personal access token.
- Environment Variables (if not passed in):  
  - `GITHUB_TOKEN`: Token for authentication  
  - `GITHUB_OWNER`: Repository owner/organization  
  - `GITHUB_REPO`: Target repository name  
- Class reference: `GitHubAPISync(repo_owner, repo_name, auth_token, api_url, custom_file_url)`

### BitbucketAPISync
- Syncs via Bitbucket’s API; requires the Bitbucket workspace and repo info.
- Environment Variables:  
  - `BITBUCKET_WORKSPACE`: Identifier for the Bitbucket workspace  
  - `BITBUCKET_REPO`: Identifier for the repository  
- Class reference: `BitbucketAPISync(workspace, repo, api_url, custom_file_url)`

### GistAPISync
- Publishes encrypted data as a GitHub Gist.
- Environment Variables:
  - `GIST_ID`: Target Gist identifier  
- Class reference: `GistAPISync(gist_id, api_url, custom_file_url)`

## Class and Method Reference

### DataEncryption
Main class for encrypting sensitive data with optional cloud sync support.

**Common Usage Examples:**
```python
# Local encryption only
encrypter = DataEncryption(
    private_key_path="/path/to/private.pem",
    repo_path="/path/to/local/repo"
)

# With GitHub API sync
encrypter = DataEncryption(
    private_key_path="/path/to/private.pem",
    sync_type="github",
    fetcher_options={
        "repo_owner": "username",
        "repo_name": "repo",
        "auth_token": "github-token"
    }
)

# With Bitbucket sync
encrypter = DataEncryption(
    private_key_path="/path/to/private.pem",
    sync_type="bitbucket",
    fetcher_options={
        "workspace": "workspace-id",
        "repo_slug": "repo-name",
        "auth_token": "bitbucket-token"
    }
)
```

### DataDecryptor
Handles fetching and decrypting data with support for multiple Git providers.

**Common Usage Examples:**
```python
# Decrypt from GitHub repository
decryptor = DataDecryptor(
    key_url="path/to/secret.enc",
    auth_token="github-token",
    private_key_path="/path/to/private.pem",
    fetch_type=FetchType.GITHUB,
    fetcher_options={
        "repo_owner": "username",
        "repo_name": "repo"
    }
)

# Decrypt from Gist
decryptor = DataDecryptor(
    key_url="path/to/secret.enc",
    auth_token="github-token",
    private_key_path="/path/to/private.pem",
    fetch_type=FetchType.GIST,
    fetcher_options={
        "gist_id": "gist-id"
    }
)
```

### Error Handling Examples
```python
try:
    encrypter = DataEncryption()
    encrypter.encrypt_and_store("secret")
except ConfigurationError:
    print("Check your environment variables or parameters")
except PrivateKeyNotFoundError:
    print("Ensure your private key exists at the specified path")
except EncryptionError:
    print("Something went wrong during encryption")
except GitOperationError as e:
    print(f"Git sync failed: {e}")
```

Common error scenarios:
- **ConfigurationError**: Missing required environment variables
- **SyncConfigurationError**: Invalid GitHub token or repository details
- **PrivateKeyNotFoundError**: RSA private key file not found
- **EncryptionError/DecryptionError**: Data corruption or key mismatch
- **GitOperationError**: Network issues or repository access problems

## Common Usage Patterns

### 1. Basic Password Storage
Store passwords or secrets locally with encryption:
```python
# 💾 Storing secrets
from gitvault.encrypt_data import DataEncryption

# Setup basic encryption
encrypter = DataEncryption(
    private_key_path="/path/to/private.pem",
    repo_path="./secrets"
)

# Store multiple secrets
encrypter.encrypt_and_store("database-password-123")  # 🗝️ keep safe
```

### 2. Team Password Management
Share encrypted secrets with your team using GitHub:
```python
# 👥 Let's share secrets safely
from gitvault.encrypt_data import DataEncryption
from gitvault.decrypt_data import DataDecryptor, FetchType

# Team lead: Encrypt and store
encrypter = DataEncryption(
    private_key_path="keys/private.pem",
    sync_type="github",
    fetcher_options={
        "repo_owner": "my-org",
        "repo_name": "team-secrets",
        "auth_token": "github-token"
    }
)
encrypter.encrypt_and_store("prod-api-key-456")  # 🚀 store for the team

# Team member: Retrieve and decrypt
decryptor = DataDecryptor(
    key_url="secrets/prod-api.enc",
    auth_token="github-token",
    private_key_path="keys/private.pem",
    fetch_type=FetchType.GITHUB,
    fetcher_options={
        "repo_owner": "my-org",
        "repo_name": "team-secrets"
    }
)
result = decryptor.fetch_and_decrypt()           # 🤫 retrieving secrets
```

### 3. CI/CD Pipeline Integration
Store deployment secrets in Bitbucket:
```python
# 🏗️ Automate all the things
# Store deployment credentials
encrypter = DataEncryption(
    private_key_path="/ci/keys/private.pem",
    sync_type="bitbucket",
    fetcher_options={
        "workspace": "company-name",
        "repo_slug": "deploy-secrets",
        "auth_token": "bitbucket-token"
    }
)
encrypter.encrypt_and_store("aws-secret-key")    # 🛠️ building trust

# In CI/CD pipeline
decryptor = DataDecryptor(
    key_url="secrets/aws-creds.enc",
    auth_token="pipeline-token",
    private_key_path="/ci/keys/private.pem",
    fetch_type=FetchType.BITBUCKET,
    fetcher_options={
        "workspace": "company-name",
        "repo_slug": "deploy-secrets"
    }
)
aws_creds = decryptor.fetch_and_decrypt()        # 🤖 for the pipeline
```

### 4. Quick Note Sharing
Share encrypted notes via GitHub Gist:
```python
# 📝 Share ephemeral notes
# Share encrypted note
encrypter = DataEncryption(
    private_key_path="keys/private.pem",
    sync_type="gist",
    fetcher_options={
        "auth_token": "github-token"
    }
)
encrypter.encrypt_and_store("Meeting notes with credentials")  # 💡

# Retrieve shared note
decryptor = DataDecryptor(
    key_url="note.enc",
    auth_token="github-token",
    private_key_path="keys/private.pem",
    fetch_type=FetchType.GIST,
    fetcher_options={
        "gist_id": "abc123def456"
    }
)
notes = decryptor.fetch_and_decrypt()                          # 🔍 reveal
```

### Error Handling Best Practices
```python
# 💢 Watch out for errors
from gitvault.custom_exceptions import (
    ConfigurationError, 
    PrivateKeyNotFoundError,
    EncryptionError,
    GitOperationError
)

try:
    encrypter = DataEncryption(...)
    encrypter.encrypt_and_store("secret")
except ConfigurationError:
    print("💥 Missing configuration. Check your paths and tokens.")
except PrivateKeyNotFoundError:
    print("🔑 Private key not found or invalid.")
except EncryptionError:
    print("🔒 Encryption failed. Verify your key and data.")
except GitOperationError as e:
    print(f"📡 Sync failed: {e}. Check your connection and permissions.")
```

## Notes & Troubleshooting
- Missing paths or tokens raise configuration errors early.
- RSA keys must be valid PEM files.  
- Logging is handled via built-in `logging` at INFO level.  
- Ensure your SSH and private keys exist if Git-based sync is used.
- For API-based sync, make sure tokens and repository info are valid.
- Ensure you have correct permissions on the remote service (GitHub, Bitbucket, etc.).

## Contributing
Contributions are welcome. Fork the repo, create a branch, and submit a pull request with changes.
