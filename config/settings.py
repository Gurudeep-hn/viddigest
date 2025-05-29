"""
Application configuration settings - Railway compatible
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # API Keys
    GROQ_API_KEY: str = os.getenv('GROQ_API_KEY', '')
    YOUTUBE_API_KEY: str = os.getenv('YOUTUBE_API_KEY', '')
    
    # AI Configuration
    GROQ_MODEL: str = os.getenv('GROQ_MODEL', 'llama3-8b-8192')
    MAX_TOKENS: int = int(os.getenv('MAX_TOKENS', '512'))
    TEMPERATURE: float = float(os.getenv('TEMPERATURE', '0.3'))
    
    # Server Configuration
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '8000'))
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Application Limits
    MAX_TRANSCRIPT_LENGTH: int = int(os.getenv('MAX_TRANSCRIPT_LENGTH', '10000'))

# Create global settings instance
_settings = None

def get_settings() -> Settings:
    """Get cached settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings