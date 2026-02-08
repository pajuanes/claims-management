from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import hvac
import os
from typing import Optional


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Claims Manager"
    
    # Security
    SECRET_KEY: Optional[str] = None
    
    # Vault Configuration
    VAULT_URL: str = "http://localhost:8200"
    VAULT_TOKEN: Optional[str] = None
    VAULT_SECRET_PATH: str = "secret/data/fastapi"
    
    # Database
    MONGO_URI: str = "mongodb://127.0.0.1:27017/claims_manager"
    
    def get_secret_key(self) -> str:
        """Retrieve SECRET_KEY from Vault or fallback to environment variable"""
        if self.SECRET_KEY:
            return self.SECRET_KEY
            
        try:
            client = hvac.Client(url=self.VAULT_URL, token=self.VAULT_TOKEN)
            if client.is_authenticated():
                response = client.secrets.kv.v2.read_secret_version(path="fastapi")
                return response['data']['data']['SECRET_KEY']
        except Exception:
            pass
            
        # Fallback to environment variable
        return os.getenv("SECRET_KEY", "fallback-secret-key-change-in-production")
    
    model_config = ConfigDict(env_file=".env")
    

settings = Settings()