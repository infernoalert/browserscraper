"""
Logging utilities for browser scraper
"""

import logging
import os
from datetime import datetime
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log messages"""
    
    # Color codes for different log levels
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Add color to the log level name
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
        
        return super().format(record)


class ScraperLogger:
    """Main logger for the scraper application"""
    
    def __init__(self, name: str = "BrowserScraper", log_level: str = "INFO", log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler with colors
        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler if log_file is specified
        if log_file:
            self._setup_file_handler(log_file)
    
    def _setup_file_handler(self, log_file: str):
        """Setup file handler for logging"""
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str, *args, **kwargs):
        """Log debug message"""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """Log info message"""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """Log warning message"""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """Log error message"""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """Log critical message"""
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs):
        """Log exception with traceback"""
        self.logger.exception(message, *args, **kwargs)


class SessionLogger:
    """Session-specific logger that tracks scraping sessions"""
    
    def __init__(self, base_logger: ScraperLogger, session_id: Optional[str] = None):
        self.base_logger = base_logger
        self.session_id = session_id or self._generate_session_id()
        self.start_time = datetime.now()
        
        self.info(f"Session started: {self.session_id}")
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _format_message(self, message: str) -> str:
        """Format message with session ID"""
        return f"[{self.session_id}] {message}"
    
    def debug(self, message: str, *args, **kwargs):
        """Log debug message with session ID"""
        self.base_logger.debug(self._format_message(message), *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """Log info message with session ID"""
        self.base_logger.info(self._format_message(message), *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """Log warning message with session ID"""
        self.base_logger.warning(self._format_message(message), *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """Log error message with session ID"""
        self.base_logger.error(self._format_message(message), *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """Log critical message with session ID"""
        self.base_logger.critical(self._format_message(message), *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs):
        """Log exception with session ID"""
        self.base_logger.exception(self._format_message(message), *args, **kwargs)
    
    def log_page_visited(self, url: str, status: str = "success"):
        """Log when a page is visited"""
        self.info(f"Page visited: {url} - Status: {status}")
    
    def log_data_extracted(self, data_type: str, count: int):
        """Log when data is extracted"""
        self.info(f"Data extracted: {data_type} - Count: {count}")
    
    def log_session_stats(self, pages_visited: int, items_extracted: int):
        """Log session statistics"""
        duration = datetime.now() - self.start_time
        self.info(f"Session stats - Pages: {pages_visited}, Items: {items_extracted}, Duration: {duration}")
    
    def end_session(self):
        """End the session and log final stats"""
        duration = datetime.now() - self.start_time
        self.info(f"Session ended: {self.session_id} - Duration: {duration}")


# Global logger instance
logger = ScraperLogger()


def get_logger(name: str = "BrowserScraper", log_level: str = "INFO", log_file: Optional[str] = None) -> ScraperLogger:
    """Get a logger instance"""
    return ScraperLogger(name, log_level, log_file)


def get_session_logger(base_logger: Optional[ScraperLogger] = None, session_id: Optional[str] = None) -> SessionLogger:
    """Get a session logger instance"""
    if base_logger is None:
        base_logger = logger
    return SessionLogger(base_logger, session_id) 