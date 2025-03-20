import pytest
import base64
from gitvault.decrypt_data import DataDecryptor, FetchType
from gitvault.custom_exceptions import PrivateKeyNotFoundError, InvalidURLError

def test_decryptor_init_valid(sample_private_key_path):
    decryptor = DataDecryptor(
        key_url="https://example.com/encrypted",
        auth_token="dummy-token",
        private_key_path=str(sample_private_key_path),
        fetch_type=FetchType.GITREPO,
        fetcher_options={"repo_path": ".", "file_path": "encrypted.txt"}
    )
    assert decryptor is not None

def test_decryptor_init_missing_key_url(sample_private_key_path):
    with pytest.raises(InvalidURLError):
        DataDecryptor(
            key_url="",
            auth_token="dummy-token",
            private_key_path=str(sample_private_key_path),
            fetch_type=FetchType.GITREPO,
            fetcher_options={"repo_path": ".", "file_path": "encrypted.txt"}
        )

def test_private_key_not_found():
    with pytest.raises(PrivateKeyNotFoundError):
        DataDecryptor(
            key_url="http://example.com/secret.enc",
            auth_token="dummy-token",
            private_key_path="invalid/path/to/key.pem",
            fetch_type=FetchType.GITREPO,
            fetcher_options={"repo_path": ".", "file_path": "secret.enc"}
        )

def test_fetch_and_decrypt_error_handling(mocker, sample_private_key_path):
    # Mock fetcher to return invalid base64
    mocker.patch(
        "gitvault.git_fetch.GitRepoFetch.fetch_data",
        return_value="!!!not-base64!!!"
    )
    decryptor = DataDecryptor(
        key_url="http://example.com/secret.enc",
        auth_token="dummy-token",
        private_key_path=str(sample_private_key_path),
        fetch_type=FetchType.GITREPO,
        fetcher_options={"repo_path": ".", "file_path": "secret.enc"}
    )
    result = decryptor.fetch_and_decrypt()
    assert result.success is False
    assert "Invalid base64" in result.error
