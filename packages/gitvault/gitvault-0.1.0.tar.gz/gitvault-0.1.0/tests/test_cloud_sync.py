import pytest
import tempfile
from pathlib import Path
from gitvault.cloud_sync import GitSync, GitHubAPISync, BitbucketAPISync
from gitvault.custom_exceptions import GitOperationError

def test_git_sync_init():
    sync = GitSync(repo_path=Path("."), repo_url="git@github.com:repo.git", ssh_key_path=Path("~/.ssh/id_rsa"))
    assert sync is not None

def test_git_sync_failure(mocker):
    mocker.patch("git.Repo.clone_from", side_effect=Exception("Clone failed"))
    with pytest.raises(GitOperationError):
        sync = GitSync(repo_path=Path("./newrepo"), repo_url="invalid-url", ssh_key_path=Path("~/.ssh/id_rsa"))
        sync._setup_repo()

def test_github_sync_init():
    sync = GitHubAPISync(repo_owner="someone", repo_name="myrepo", auth_token="ghp_dummy")
    assert sync is not None

def test_bitbucket_sync_init():
    sync = BitbucketAPISync(workspace="my-workspace", repo_slug="my-repo", auth_token="bb_dummy")
    assert sync is not None

@pytest.mark.parametrize("SyncClass", [GitHubAPISync, BitbucketAPISync])
def test_api_sync_methods(SyncClass, mocker):
    sync = SyncClass("owner-or-workspace", "repo", auth_token="test_token")
    mocker.patch("requests.post", return_value=mocker.Mock(status_code=201, json=lambda: {"id": "123"}))
    file_path = Path(tempfile.gettempdir()) / "dummy_file.txt"
    file_path.write_text("dummy content")
    assert sync.sync_to_cloud(file_path, "Test commit") is True
