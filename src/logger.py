"""
Logging module for Email Automation System.

This module sets up professional logging configuration following Python best practices.
Junior developers should always use logging instead of print statements in production code.
"""

import logging
import logging.handlers
import os
from typing import Optional

from .config import LoggingConfig, FileConfig


class EmailAutomationLogger:
    """
    Professional logging setup for the Email Automation System.
    
    This class demonstrates proper logging practices that junior developers
    should use in production applications.
    """
    
    _instance: Optional['EmailAutomationLogger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> 'EmailAutomationLogger':
        """Singleton pattern - ensures only one logger instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the logger if not already done."""
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Set up the logging configuration."""
        # Create logs directory if it doesn't exist
        os.makedirs(FileConfig.LOGS_FOLDER, exist_ok=True)
        
        # Create main logger
        self._logger = logging.getLogger('EmailAutomation')
        self._logger.setLevel(getattr(logging, LoggingConfig.DEFAULT_LOG_LEVEL))
        
        # Prevent duplicate handlers if logger already configured
        if self._logger.handlers:
            return
        
        # Create formatter
        formatter = logging.Formatter(
            LoggingConfig.LOG_FORMAT,
            datefmt=LoggingConfig.DATE_FORMAT
        )
        
        # Console Handler (for development)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, LoggingConfig.CONSOLE_LOG_LEVEL))
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
        
        # File Handler (for production logs)
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                LoggingConfig.LOG_FILE,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(getattr(logging, LoggingConfig.FILE_LOG_LEVEL))
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)
        except Exception as e:
            self._logger.warning(f"Could not set up file logging: {e}")
        
        # Error File Handler (separate file for errors)
        try:
            error_handler = logging.handlers.RotatingFileHandler(
                LoggingConfig.ERROR_LOG_FILE,
                maxBytes=5*1024*1024,  # 5MB
                backupCount=3
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            self._logger.addHandler(error_handler)
        except Exception as e:
            self._logger.warning(f"Could not set up error file logging: {e}")
    
    @property
    def logger(self) -> logging.Logger:
        """Get the configured logger instance."""
        return self._logger
    
    def log_function_entry(self, function_name: str, **kwargs) -> None:
        """Log function entry with parameters (useful for debugging)."""
        params = ', '.join(f"{k}={v}" for k, v in kwargs.items())
        self._logger.debug(f"Entering {function_name}({params})")
    
    def log_function_exit(self, function_name: str, result=None) -> None:
        """Log function exit with result (useful for debugging)."""
        if result is not None:
            self._logger.debug(f"Exiting {function_name} with result: {result}")
        else:
            self._logger.debug(f"Exiting {function_name}")
    
    def log_email_operation(self, operation: str, details: str) -> None:
        """Log email-specific operations."""
        self._logger.info(f"EMAIL: {operation} - {details}")
    
    def log_pdf_operation(self, operation: str, filename: str, details: str = "") -> None:
        """Log PDF-specific operations."""
        self._logger.info(f"PDF: {operation} - {filename} - {details}")
    
    def log_file_operation(self, operation: str, filepath: str, details: str = "") -> None:
        """Log file-specific operations."""
        self._logger.info(f"FILE: {operation} - {filepath} - {details}")


# Global logger instance (following Python best practices)
_logger_instance = EmailAutomationLogger()
logger = _logger_instance.logger

# Convenience functions for easy logging
def log_info(message: str) -> None:
    """Log an info message."""
    logger.info(message)

def log_warning(message: str) -> None:
    """Log a warning message."""
    logger.warning(message)

def log_error(message: str, exc_info: bool = False) -> None:
    """Log an error message."""
    logger.error(message, exc_info=exc_info)

def log_debug(message: str) -> None:
    """Log a debug message."""
    logger.debug(message)

def log_success(message: str) -> None:
    """Log a success message (as info with SUCCESS prefix)."""
    logger.info(f"SUCCESS: {message}")


# Decorator for automatic function logging
def log_function_calls(func):
    """
    Decorator to automatically log function entry and exit.
    
    This is a professional practice that junior developers should learn.
    """
    def wrapper(*args, **kwargs):
        function_name = func.__name__
        _logger_instance.log_function_entry(function_name, **kwargs)
        
        try:
            result = func(*args, **kwargs)
            _logger_instance.log_function_exit(function_name, result)
            return result
        except Exception as e:
            logger.error(f"Error in {function_name}: {e}", exc_info=True)
            raise
    
    return wrapper


if __name__ == "__main__":
    # Test the logging system
    log_info("Testing Email Automation Logger")
    log_debug("This is a debug message")
    log_warning("This is a warning message")
    log_error("This is an error message")
    log_success("Logger setup completed successfully")
    
    # Test function logging
    @log_function_calls
    def test_function(param1: str, param2: int = 42):
        return f"Processed {param1} with {param2}"
    
    result = test_function("test_data", param2=100)
    log_info(f"Test function result: {result}")