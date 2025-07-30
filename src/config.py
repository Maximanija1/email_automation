"""
Configuration module for Email Automation System.

This module centralizes all configuration settings, making the application
more maintainable and following professional Python development practices.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class EmailConfig:
    """Configuration settings for email operations."""
    
    # Gmail IMAP Settings
    GMAIL_IMAP_SERVER: str = 'imap.gmail.com'
    GMAIL_IMAP_PORT: int = 993
    
    # Credentials (from environment variables)
    EMAIL_ADDRESS: Optional[str] = os.getenv('GMAIL_EMAIL')
    APP_PASSWORD: Optional[str] = os.getenv('GMAIL_APP_PASSWORD')
    
    # Email Search Settings
    DEFAULT_SEARCH_KEYWORD: str = "Mediafill"
    
    @classmethod
    def validate_credentials(cls) -> bool:
        """Validate that required credentials are available."""
        return bool(cls.EMAIL_ADDRESS and cls.APP_PASSWORD)


class FileConfig:
    """Configuration settings for file operations."""
    
    # Directory Settings
    DOWNLOADS_FOLDER: str = "downloads"
    LOGS_FOLDER: str = "logs"
    
    # File Naming
    TIMESTAMP_FORMAT: str = "%Y-%m-%d_%H-%M-%S"
    
    # Supported File Types
    SUPPORTED_PDF_EXTENSIONS: tuple = ('.pdf',)


class PDFConfig:
    """Configuration settings for PDF processing."""
    
    # Table Detection Settings
    TABLE_DETECTION_STRATEGY: str = "lattice"  # or "stream"
    MIN_TABLE_CONFIDENCE: float = 0.5
    
    # Search Settings
    CASE_SENSITIVE_SEARCH: bool = False
    
    # Processing Settings
    MAX_PAGES_TO_PROCESS: Optional[int] = None  # None = all pages


class LoggingConfig:
    """Configuration settings for logging."""
    
    # Log Levels
    DEFAULT_LOG_LEVEL: str = "INFO"
    FILE_LOG_LEVEL: str = "DEBUG"
    CONSOLE_LOG_LEVEL: str = "INFO"
    
    # Log Format
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    
    # Log Files
    LOG_FILE: str = os.path.join(FileConfig.LOGS_FOLDER, "email_automation.log")
    ERROR_LOG_FILE: str = os.path.join(FileConfig.LOGS_FOLDER, "errors.log")


# Application-wide settings
class AppConfig:
    """Main application configuration."""
    
    APP_NAME: str = "Email PDF Automation"
    VERSION: str = "1.0.0"
    AUTHOR: str = "Matas"
    
    # Feature Flags
    ENABLE_PDF_PROCESSING: bool = True
    ENABLE_FILE_ORGANIZATION: bool = True
    ENABLE_DETAILED_LOGGING: bool = True


# Validation function
def validate_configuration() -> tuple[bool, list[str]]:
    """
    Validate all configuration settings.
    
    Returns:
        tuple: (is_valid, list_of_errors)
    """
    errors = []
    
    # Check email credentials
    if not EmailConfig.validate_credentials():
        errors.append("Missing email credentials in environment variables")
    
    # Check required directories exist or can be created
    for folder in [FileConfig.DOWNLOADS_FOLDER, FileConfig.LOGS_FOLDER]:
        try:
            os.makedirs(folder, exist_ok=True)
        except Exception as e:
            errors.append(f"Cannot create directory {folder}: {e}")
    
    return len(errors) == 0, errors


if __name__ == "__main__":
    # Test configuration when run directly
    is_valid, errors = validate_configuration()
    
    if is_valid:
        print(f"✅ {AppConfig.APP_NAME} v{AppConfig.VERSION} - Configuration Valid")
        print(f"📧 Email: {EmailConfig.EMAIL_ADDRESS}")
        print(f"📁 Downloads: {FileConfig.DOWNLOADS_FOLDER}")
        print(f"📋 Logs: {FileConfig.LOGS_FOLDER}")
    else:
        print("❌ Configuration Errors:")
        for error in errors:
            print(f"  - {error}")