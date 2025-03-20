"""Custom exceptions for the password sync module.

This module contains custom exceptions used throughout the password sync
package to provide more specific error handling capabilities.
"""

class PrivateKeyNotFoundError(Exception):
    """🔑 Missing private key! 🔑
    
    This exception indicates issues with private key file availability or
    permissions. Check file path and permissions when this error occurs.
    """
    pass

class DataFetchError(Exception):
    """🚀 Data retrieval hit a cosmic snag! 🚀
    
    This exception indicates issues with network connectivity, remote server
    availability, or data access permissions. Check network connection and
    server status when this error occurs.
    """
    pass

class DecryptionError(Exception):
    """🔐 Decryption got jumbled! 🔐
    
    This exception indicates issues with the decryption process, such as
    incorrect keys or corrupted data. Verify the decryption key and data
    integrity when this error occurs.
    """
    pass

class EncryptionError(Exception):
    """🔏 Encryption meltdown! 🔏
    
    This exception indicates issues with the encryption process, such as
    invalid key format or data encoding issues.
    """
    pass

class GitOperationError(Exception):
    """🐙 Git hiccup detected! 🐙
    
    This exception indicates issues with git operations such as push, pull,
    or repository initialization failures.
    """
    pass

class ConfigurationError(Exception):
    """⚙️ Configuration mismatch! ⚙️
    
    This exception indicates missing or invalid configuration parameters
    such as missing paths or invalid URLs.
    """
    pass

class SyncConfigurationError(Exception):
    """☁️ Sync config confusion! ☁️
    
    This exception indicates missing or invalid configuration parameters
    such as missing paths or invalid URLs.
    """
    pass

class DataDecryptorError(Exception):
    """🔎 DataDecryptor had a puzzle! 🔎
    
    This exception indicates issues with the decryption process, such as
    incorrect keys or corrupted data. Verify the decryption key and data
    integrity when this error occurs.
    """
    pass

class InvalidURLError(DataDecryptorError):
    """🌐 URL went off track! 🌐
    
    This exception indicates issues with the decryption process, such as
    incorrect keys or corrupted data. Verify the decryption key and data
    integrity when this error occurs.
    """
    pass

class InvalidOptionError(DataDecryptorError):
    """⚠️ Invalid option found! ⚠️
    
    This exception indicates issues with the decryption process, such as
    incorrect keys or corrupted data. Verify the decryption key and data
    integrity when this error occurs.
    """
    pass
