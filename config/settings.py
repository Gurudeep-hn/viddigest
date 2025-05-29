"""
Application configuration settings
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    GROQ_API_KEY: str = ""
    YOUTUBE_API_KEY: str = ""
    
    # AI Configuration
    GROQ_MODEL: str = "llama3-8b-8192"
    MAX_TOKENS: int = 512
    TEMPERATURE: float = 0.3
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Application Limits
    MAX_TRANSCRIPT_LENGTH: int = 10000
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()