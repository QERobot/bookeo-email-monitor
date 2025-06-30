"""
Logging configuration for the email monitoring agent
"""

import logging
import logging.handlers
import os
from datetime import datetime

def setup_logger(name="EmailMonitor", log_level="INFO", log_file="email_monitor.log"):
    """Setup and configure logger with both file and console handlers"""
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Create file handler with rotation
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.error(f"Failed to setup file logging: {str(e)}")
    
    # Log startup information
    logger.info("=" * 50)
    logger.info("Email Monitoring Agent Logger Initialized")
    logger.info(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Log Level: {log_level.upper()}")
    logger.info(f"Log File: {log_file}")
    logger.info("=" * 50)
    
    return logger

def get_logger(name="EmailMonitor"):
    """Get existing logger instance"""
    return logging.getLogger(name)
