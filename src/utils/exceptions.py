"""
Custom exceptions for browser scraper
"""


class BrowserScraperException(Exception):
    """Base exception for browser scraper"""
    pass


class BrowserStartupException(BrowserScraperException):
    """Exception raised when browser fails to start"""
    pass


class NavigationException(BrowserScraperException):
    """Exception raised when navigation fails"""
    pass


class ElementNotFoundException(BrowserScraperException):
    """Exception raised when element is not found"""
    pass


class ScrapingException(BrowserScraperException):
    """Exception raised during scraping operations"""
    pass


class ConfigurationException(BrowserScraperException):
    """Exception raised for configuration errors"""
    pass


class OutputException(BrowserScraperException):
    """Exception raised when output operations fail"""
    pass


class TimeoutException(BrowserScraperException):
    """Exception raised when operations timeout"""
    pass


class AuthenticationException(BrowserScraperException):
    """Exception raised for authentication issues"""
    pass 