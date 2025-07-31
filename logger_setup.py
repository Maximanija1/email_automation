import logging
import os
from datetime import datetime

def setup_logger(name="email_automation"):
    """
    Set up a professional logger that writes to both console and file

    Args:
        name (str, optional): Name of the logger. Defaults to "email_automation".

    Returns:
        logging.Logger: Configured logger instance
    """

    # Create logger 
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) # Capture all levels

    # Prevent duplicate logs if logger already exists
    if logger.handlers:
        return logger
    
    # Create logs directory if it doesn't exists
    os.makedirs("logs", exist_ok=True)

    # Create lof filename with current date
    log_filename = f"logs/automation_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"\
    
    # Create formatters for different output types
    detailed_formatted = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s', 
        datefmt = '%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )

    # File handler - saves everything to file
    file_handler = logging.FileHandler(log_filename, encoding= 'utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatted)

    # Console handler - shows important stuff on screen
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Log the logger setup
    logger.info("Logger initialized successfully")
    logger.debug(f"Log file created: {log_filename}")

    return logger
