import pytest
import os
from unittest.mock import Mock, patch
from app.core.config import Settings


def test_get_secret_key_from_settings():
    """Test SECRET_KEY is returned when already set in settings"""
    settings = Settings(SECRET_KEY="my-secret-key")
    assert settings.get_secret_key() == "my-secret-key"


def test_get_secret_key_from_vault(monkeypatch):
    """Test SECRET_KEY is retrieved from Vault when authenticated"""
    settings = Settings(VAULT_TOKEN="test-token")
    
    mock_client = Mock()
    mock_client.is_authenticated.return_value = True
    mock_client.secrets.kv.v2.read_secret_version.return_value = {
        'data': {'data': {'SECRET_KEY': 'vault-secret-key'}}
    }
    
    with patch('app.core.config.hvac.Client', return_value=mock_client):
        result = settings.get_secret_key()
    
    assert result == "vault-secret-key"


def test_get_secret_key_vault_not_authenticated(monkeypatch):
    """Test fallback when Vault is not authenticated"""
    settings = Settings(VAULT_TOKEN="invalid-token")
    
    mock_client = Mock()
    mock_client.is_authenticated.return_value = False
    
    monkeypatch.setenv("SECRET_KEY", "env-secret-key")
    
    with patch('app.core.config.hvac.Client', return_value=mock_client):
        result = settings.get_secret_key()
    
    assert result == "env-secret-key"


def test_get_secret_key_vault_exception(monkeypatch):
    """Test fallback when Vault raises exception"""
    settings = Settings(VAULT_TOKEN="test-token")
    
    with patch('app.core.config.hvac.Client', side_effect=Exception("Connection error")):
        monkeypatch.setenv("SECRET_KEY", "env-secret-key")
        result = settings.get_secret_key()
    
    assert result == "env-secret-key"


def test_get_secret_key_fallback_default():
    """Test fallback to default when no SECRET_KEY in environment"""
    settings = Settings()
    
    # Ensure SECRET_KEY is not in environment
    if "SECRET_KEY" in os.environ:
        del os.environ["SECRET_KEY"]
    
    with patch('app.core.config.hvac.Client', side_effect=Exception("No vault")):
        result = settings.get_secret_key()
    
    assert result == "fallback-secret-key-change-in-production"
