"""
Browser management for web scraping
"""

import os
import time
from typing import Optional, Dict, Any, List, Union
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException

from ..utils.logger import ScraperLogger
from ..utils.exceptions import BrowserStartupException, NavigationException, TimeoutException as CustomTimeoutException
from ..core.config import BrowserConfig


class BrowserManager:
    """Manages browser instance and common operations"""
    
    def __init__(self, config: BrowserConfig, logger: ScraperLogger):
        self.config = config
        self.logger = logger
        self.driver: Optional[Union[webdriver.Chrome, webdriver.Firefox]] = None
        self.wait: Optional[WebDriverWait] = None
        
    def start_browser(self) -> Union[webdriver.Chrome, webdriver.Firefox]:
        """Start browser with configured options"""
        try:
            self.logger.info(f"Starting {self.config.browser_type} browser...")
            
            if self.config.browser_type.lower() == "chrome":
                self.driver = self._start_chrome()
            elif self.config.browser_type.lower() == "firefox":
                self.driver = self._start_firefox()
            else:
                raise BrowserStartupException(f"Unsupported browser type: {self.config.browser_type}")
            
            # Set up wait
            if self.driver:
                self.wait = WebDriverWait(self.driver, self.config.implicit_wait)
                
                # Configure timeouts
                self.driver.set_page_load_timeout(self.config.page_load_timeout)
                self.driver.implicitly_wait(self.config.implicit_wait)
            
            self.logger.info(f"Browser started successfully")
            return self.driver
            
        except WebDriverException as e:
            raise BrowserStartupException(f"Failed to start browser: {str(e)}")
        except Exception as e:
            raise BrowserStartupException(f"Unexpected error starting browser: {str(e)}")
    
    def _start_chrome(self) -> webdriver.Chrome:
        """Start Chrome browser with options"""
        options = ChromeOptions()
        
        # Configure window size
        options.add_argument(f'--window-size={self.config.window_size[0]},{self.config.window_size[1]}')
        
        # Configure headless mode
        if self.config.headless:
            options.add_argument('--headless')
        
        # Configure GPU usage
        if self.config.disable_gpu:
            options.add_argument('--disable-gpu')
        
        # Configure image loading
        if self.config.disable_images:
            options.add_argument('--disable-images')
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)
        
        # Configure user agent
        if self.config.user_agent:
            options.add_argument(f'--user-agent={self.config.user_agent}')
        
        # Additional stability options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        return webdriver.Chrome(options=options)
    
    def _start_firefox(self) -> webdriver.Firefox:
        """Start Firefox browser with options"""
        options = FirefoxOptions()
        
        # Configure headless mode
        if self.config.headless:
            options.add_argument('--headless')
        
        # Configure window size
        options.add_argument(f'--width={self.config.window_size[0]}')
        options.add_argument(f'--height={self.config.window_size[1]}')
        
        # Configure user agent
        if self.config.user_agent:
            options.set_preference("general.useragent.override", self.config.user_agent)
        
        # Configure image loading
        if self.config.disable_images:
            options.set_preference("permissions.default.image", 2)
        
        return webdriver.Firefox(options=options)
    
    def navigate_to(self, url: str) -> None:
        """Navigate to a URL"""
        if not self.driver:
            raise NavigationException("Browser not started")
        
        try:
            self.logger.info(f"Navigating to: {url}")
            self.driver.get(url)
            time.sleep(1)  # Brief pause for page stability
            self.logger.info(f"Successfully navigated to: {url}")
        except Exception as e:
            raise NavigationException(f"Failed to navigate to {url}: {str(e)}")
    
    def wait_for_element(self, locator: tuple, timeout: Optional[int] = None) -> Any:
        """Wait for element to be present"""
        if not self.wait:
            raise CustomTimeoutException("WebDriverWait not initialized")
        
        try:
            wait_time = timeout or self.config.implicit_wait
            if self.driver:
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located(locator)
                )
                return element
            else:
                raise CustomTimeoutException("Driver not initialized")
        except TimeoutException:
            raise CustomTimeoutException(f"Element not found within {wait_time} seconds: {locator}")
    
    def wait_for_clickable(self, locator: tuple, timeout: Optional[int] = None) -> Any:
        """Wait for element to be clickable"""
        if not self.wait:
            raise CustomTimeoutException("WebDriverWait not initialized")
        
        try:
            wait_time = timeout or self.config.implicit_wait
            if self.driver:
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.element_to_be_clickable(locator)
                )
                return element
            else:
                raise CustomTimeoutException("Driver not initialized")
        except TimeoutException:
            raise CustomTimeoutException(f"Element not clickable within {wait_time} seconds: {locator}")
    
    def scroll_to_element(self, element) -> None:
        """Scroll to element"""
        if not self.driver:
            raise NavigationException("Browser not started")
        
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Brief pause for scroll
    
    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page"""
        if not self.driver:
            raise NavigationException("Browser not started")
        
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Brief pause for scroll
    
    def take_screenshot(self, filename: str) -> None:
        """Take screenshot"""
        if not self.driver:
            raise NavigationException("Browser not started")
        
        try:
            self.driver.save_screenshot(filename)
            self.logger.info(f"Screenshot saved: {filename}")
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
    
    def get_page_source(self) -> str:
        """Get page source"""
        if not self.driver:
            raise NavigationException("Browser not started")
        
        return self.driver.page_source
    
    def get_current_url(self) -> str:
        """Get current URL"""
        if not self.driver:
            raise NavigationException("Browser not started")
        
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Get page title"""
        if not self.driver:
            raise NavigationException("Browser not started")
        
        return self.driver.title
    
    def refresh_page(self) -> None:
        """Refresh current page"""
        if not self.driver:
            raise NavigationException("Browser not started")
        
        self.driver.refresh()
        time.sleep(2)  # Wait for page to reload
    
    def go_back(self) -> None:
        """Go back in browser history"""
        if not self.driver:
            raise NavigationException("Browser not started")
        
        self.driver.back()
        time.sleep(1)  # Brief pause
    
    def go_forward(self) -> None:
        """Go forward in browser history"""
        if not self.driver:
            raise NavigationException("Browser not started")
        
        self.driver.forward()
        time.sleep(1)  # Brief pause
    
    def close_browser(self) -> None:
        """Close browser"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("Browser closed successfully")
            except Exception as e:
                self.logger.error(f"Error closing browser: {str(e)}")
            finally:
                self.driver = None
                self.wait = None
    
    def get_cookies(self) -> List[Dict[str, Any]]:
        """Get all cookies"""
        if not self.driver:
            raise NavigationException("Browser not started")
        
        return self.driver.get_cookies()
    
    def add_cookie(self, cookie_dict: Dict[str, Any]) -> None:
        """Add cookie"""
        if not self.driver:
            raise NavigationException("Browser not started")
        
        self.driver.add_cookie(cookie_dict)
    
    def clear_cookies(self) -> None:
        """Clear all cookies"""
        if not self.driver:
            raise NavigationException("Browser not started")
        
        self.driver.delete_all_cookies()
    
    def execute_script(self, script: str, *args) -> Any:
        """Execute JavaScript"""
        if not self.driver:
            raise NavigationException("Browser not started")
        
        return self.driver.execute_script(script, *args)
    
    def is_element_present(self, locator: tuple) -> bool:
        """Check if element is present"""
        if not self.driver:
            return False
        
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_browser() 