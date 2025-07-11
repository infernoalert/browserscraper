"""
Web scraper with data extraction capabilities
"""

import time
import re
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urljoin, urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from .browser_manager import BrowserManager
from .config import ScrapingConfig
from ..utils.logger import SessionLogger
from ..utils.exceptions import ScrapingException, ElementNotFoundException
from ..utils.file_utils import DataExporter


class WebScraper:
    """Main web scraper class with data extraction capabilities"""
    
    def __init__(self, browser_manager: BrowserManager, config: ScrapingConfig, 
                 logger: SessionLogger, data_exporter: DataExporter):
        self.browser = browser_manager
        self.config = config
        self.logger = logger
        self.data_exporter = data_exporter
        self.scraped_data = []
        self.session_stats = {
            'pages_visited': 0,
            'items_extracted': 0,
            'errors': 0,
            'start_time': time.time()
        }
    
    def scrape_page(self, url: str, selectors: Dict[str, str], 
                   extract_multiple: bool = False) -> List[Dict[str, Any]]:
        """
        Scrape a single page with specified selectors
        
        Args:
            url: URL to scrape
            selectors: Dictionary of field_name -> CSS_selector
            extract_multiple: Whether to extract multiple items or just one
        
        Returns:
            List of extracted data dictionaries
        """
        try:
            self.browser.navigate_to(url)
            self.session_stats['pages_visited'] += 1
            self.logger.log_page_visited(url)
            
            # Wait for page to load
            time.sleep(self.config.default_delay)
            
            # Extract data
            if extract_multiple:
                data = self._extract_multiple_items(selectors)
            else:
                data = [self._extract_single_item(selectors)]
            
            # Filter out empty results
            data = [item for item in data if item and any(item.values())]
            
            self.session_stats['items_extracted'] += len(data)
            self.logger.log_data_extracted("page_items", len(data))
            
            # Add to scraped data
            self.scraped_data.extend(data)
            
            return data
            
        except Exception as e:
            self.session_stats['errors'] += 1
            self.logger.error(f"Failed to scrape page {url}: {str(e)}")
            raise ScrapingException(f"Failed to scrape page {url}: {str(e)}")
    
    def _extract_single_item(self, selectors: Dict[str, str]) -> Dict[str, Any]:
        """Extract a single item using selectors"""
        extracted_data = {}
        
        for field_name, selector in selectors.items():
            try:
                element = self.browser.driver.find_element(By.CSS_SELECTOR, selector)
                extracted_data[field_name] = self._extract_element_data(element)
            except NoSuchElementException:
                extracted_data[field_name] = None
                self.logger.warning(f"Element not found for {field_name}: {selector}")
        
        return extracted_data
    
    def _extract_multiple_items(self, selectors: Dict[str, str]) -> List[Dict[str, Any]]:
        """Extract multiple items using selectors"""
        extracted_data = []
        
        # Find the container selector (first selector in the dict)
        container_selector = list(selectors.values())[0]
        
        try:
            # Find all container elements
            containers = self.browser.driver.find_elements(By.CSS_SELECTOR, container_selector)
            
            for container in containers:
                item_data = {}
                
                for field_name, selector in selectors.items():
                    try:
                        # Try to find element within the container
                        element = container.find_element(By.CSS_SELECTOR, selector)
                        item_data[field_name] = self._extract_element_data(element)
                    except NoSuchElementException:
                        # If not found in container, try global selector
                        try:
                            element = self.browser.driver.find_element(By.CSS_SELECTOR, selector)
                            item_data[field_name] = self._extract_element_data(element)
                        except NoSuchElementException:
                            item_data[field_name] = None
                
                if item_data:
                    extracted_data.append(item_data)
            
        except NoSuchElementException:
            self.logger.warning(f"Container not found: {container_selector}")
        
        return extracted_data
    
    def _extract_element_data(self, element: WebElement) -> str:
        """Extract data from a web element"""
        try:
            # Try different extraction methods
            text = element.text.strip()
            if text:
                return text
            
            # Try getting attribute values
            for attr in ['value', 'href', 'src', 'alt', 'title']:
                value = element.get_attribute(attr)
                if value:
                    return value.strip()
            
            # Try inner HTML
            innerHTML = element.get_attribute('innerHTML')
            if innerHTML:
                # Clean HTML tags
                clean_text = re.sub(r'<[^>]+>', '', innerHTML).strip()
                if clean_text:
                    return clean_text
            
            return ""
            
        except Exception as e:
            self.logger.warning(f"Failed to extract element data: {str(e)}")
            return ""
    
    def scrape_table(self, url: str, table_selector: str = "table") -> List[Dict[str, Any]]:
        """
        Scrape HTML table data
        
        Args:
            url: URL containing the table
            table_selector: CSS selector for the table
        
        Returns:
            List of row dictionaries
        """
        try:
            self.browser.navigate_to(url)
            self.session_stats['pages_visited'] += 1
            self.logger.log_page_visited(url)
            
            # Wait for table to load
            time.sleep(self.config.default_delay)
            
            # Find table
            table = self.browser.driver.find_element(By.CSS_SELECTOR, table_selector)
            
            # Extract headers
            headers = []
            try:
                header_row = table.find_element(By.CSS_SELECTOR, "thead tr, tr:first-child")
                header_cells = header_row.find_elements(By.CSS_SELECTOR, "th, td")
                headers = [cell.text.strip() for cell in header_cells]
            except NoSuchElementException:
                self.logger.warning("Table headers not found")
            
            # Extract rows
            rows = []
            tbody = table.find_element(By.CSS_SELECTOR, "tbody") if table.find_elements(By.CSS_SELECTOR, "tbody") else table
            row_elements = tbody.find_elements(By.CSS_SELECTOR, "tr")
            
            for row in row_elements:
                cells = row.find_elements(By.CSS_SELECTOR, "td, th")
                if cells:
                    row_data = {}
                    for i, cell in enumerate(cells):
                        header = headers[i] if i < len(headers) else f"column_{i}"
                        row_data[header] = self._extract_element_data(cell)
                    rows.append(row_data)
            
            self.session_stats['items_extracted'] += len(rows)
            self.logger.log_data_extracted("table_rows", len(rows))
            
            # Add to scraped data
            self.scraped_data.extend(rows)
            
            return rows
            
        except Exception as e:
            self.session_stats['errors'] += 1
            self.logger.error(f"Failed to scrape table from {url}: {str(e)}")
            raise ScrapingException(f"Failed to scrape table from {url}: {str(e)}")
    
    def scrape_links(self, url: str, link_selector: str = "a") -> List[Dict[str, str]]:
        """
        Scrape all links from a page
        
        Args:
            url: URL to scrape
            link_selector: CSS selector for links
        
        Returns:
            List of link dictionaries with text and href
        """
        try:
            self.browser.navigate_to(url)
            self.session_stats['pages_visited'] += 1
            self.logger.log_page_visited(url)
            
            # Wait for links to load
            time.sleep(self.config.default_delay)
            
            # Find all links
            links = self.browser.driver.find_elements(By.CSS_SELECTOR, link_selector)
            
            extracted_links = []
            for link in links:
                try:
                    text = link.text.strip()
                    href = link.get_attribute('href')
                    
                    if href:
                        # Convert relative URLs to absolute
                        absolute_url = urljoin(url, href)
                        extracted_links.append({
                            'text': text,
                            'href': absolute_url,
                            'domain': urlparse(absolute_url).netloc
                        })
                except Exception as e:
                    self.logger.warning(f"Failed to extract link: {str(e)}")
            
            self.session_stats['items_extracted'] += len(extracted_links)
            self.logger.log_data_extracted("links", len(extracted_links))
            
            # Add to scraped data
            self.scraped_data.extend(extracted_links)
            
            return extracted_links
            
        except Exception as e:
            self.session_stats['errors'] += 1
            self.logger.error(f"Failed to scrape links from {url}: {str(e)}")
            raise ScrapingException(f"Failed to scrape links from {url}: {str(e)}")
    
    def scrape_images(self, url: str, img_selector: str = "img") -> List[Dict[str, str]]:
        """
        Scrape all images from a page
        
        Args:
            url: URL to scrape
            img_selector: CSS selector for images
        
        Returns:
            List of image dictionaries with src, alt, and other attributes
        """
        try:
            self.browser.navigate_to(url)
            self.session_stats['pages_visited'] += 1
            self.logger.log_page_visited(url)
            
            # Wait for images to load
            time.sleep(self.config.default_delay)
            
            # Find all images
            images = self.browser.driver.find_elements(By.CSS_SELECTOR, img_selector)
            
            extracted_images = []
            for img in images:
                try:
                    src = img.get_attribute('src')
                    if src:
                        # Convert relative URLs to absolute
                        absolute_url = urljoin(url, src)
                        extracted_images.append({
                            'src': absolute_url,
                            'alt': img.get_attribute('alt') or '',
                            'title': img.get_attribute('title') or '',
                            'width': img.get_attribute('width') or '',
                            'height': img.get_attribute('height') or ''
                        })
                except Exception as e:
                    self.logger.warning(f"Failed to extract image: {str(e)}")
            
            self.session_stats['items_extracted'] += len(extracted_images)
            self.logger.log_data_extracted("images", len(extracted_images))
            
            # Add to scraped data
            self.scraped_data.extend(extracted_images)
            
            return extracted_images
            
        except Exception as e:
            self.session_stats['errors'] += 1
            self.logger.error(f"Failed to scrape images from {url}: {str(e)}")
            raise ScrapingException(f"Failed to scrape images from {url}: {str(e)}")
    
    def scrape_forms(self, url: str, form_selector: str = "form") -> List[Dict[str, Any]]:
        """
        Scrape form information from a page
        
        Args:
            url: URL to scrape
            form_selector: CSS selector for forms
        
        Returns:
            List of form dictionaries with inputs and attributes
        """
        try:
            self.browser.navigate_to(url)
            self.session_stats['pages_visited'] += 1
            self.logger.log_page_visited(url)
            
            # Wait for forms to load
            time.sleep(self.config.default_delay)
            
            # Find all forms
            forms = self.browser.driver.find_elements(By.CSS_SELECTOR, form_selector)
            
            extracted_forms = []
            for form in forms:
                try:
                    form_data = {
                        'action': form.get_attribute('action') or '',
                        'method': form.get_attribute('method') or 'GET',
                        'name': form.get_attribute('name') or '',
                        'id': form.get_attribute('id') or '',
                        'inputs': []
                    }
                    
                    # Extract form inputs
                    inputs = form.find_elements(By.CSS_SELECTOR, "input, textarea, select")
                    for input_elem in inputs:
                        input_data = {
                            'type': input_elem.get_attribute('type') or 'text',
                            'name': input_elem.get_attribute('name') or '',
                            'id': input_elem.get_attribute('id') or '',
                            'placeholder': input_elem.get_attribute('placeholder') or '',
                            'value': input_elem.get_attribute('value') or '',
                            'required': input_elem.get_attribute('required') is not None
                        }
                        form_data['inputs'].append(input_data)
                    
                    extracted_forms.append(form_data)
                    
                except Exception as e:
                    self.logger.warning(f"Failed to extract form: {str(e)}")
            
            self.session_stats['items_extracted'] += len(extracted_forms)
            self.logger.log_data_extracted("forms", len(extracted_forms))
            
            # Add to scraped data
            self.scraped_data.extend(extracted_forms)
            
            return extracted_forms
            
        except Exception as e:
            self.session_stats['errors'] += 1
            self.logger.error(f"Failed to scrape forms from {url}: {str(e)}")
            raise ScrapingException(f"Failed to scrape forms from {url}: {str(e)}")
    
    def scrape_custom_pattern(self, url: str, patterns: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Scrape data using custom regex patterns
        
        Args:
            url: URL to scrape
            patterns: Dictionary of field_name -> regex_pattern
        
        Returns:
            List of extracted data dictionaries
        """
        try:
            self.browser.navigate_to(url)
            self.session_stats['pages_visited'] += 1
            self.logger.log_page_visited(url)
            
            # Wait for page to load
            time.sleep(self.config.default_delay)
            
            # Get page source
            page_source = self.browser.get_page_source()
            
            extracted_data = []
            
            for field_name, pattern in patterns.items():
                try:
                    matches = re.findall(pattern, page_source, re.DOTALL | re.IGNORECASE)
                    if matches:
                        for match in matches:
                            # Handle tuple matches (from groups)
                            if isinstance(match, tuple):
                                data = {f"{field_name}_{i}": m for i, m in enumerate(match)}
                            else:
                                data = {field_name: match}
                            extracted_data.append(data)
                except Exception as e:
                    self.logger.warning(f"Failed to extract pattern {field_name}: {str(e)}")
            
            self.session_stats['items_extracted'] += len(extracted_data)
            self.logger.log_data_extracted("pattern_matches", len(extracted_data))
            
            # Add to scraped data
            self.scraped_data.extend(extracted_data)
            
            return extracted_data
            
        except Exception as e:
            self.session_stats['errors'] += 1
            self.logger.error(f"Failed to scrape patterns from {url}: {str(e)}")
            raise ScrapingException(f"Failed to scrape patterns from {url}: {str(e)}")
    
    def get_scraped_data(self) -> List[Dict[str, Any]]:
        """Get all scraped data"""
        return self.scraped_data
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        current_stats = self.session_stats.copy()
        current_stats['duration'] = time.time() - current_stats['start_time']
        return current_stats
    
    def save_data(self, format_type: str = "json", filename_prefix: str = "scraped_data") -> str:
        """Save scraped data to file"""
        try:
            if not self.scraped_data:
                self.logger.warning("No data to save")
                return ""
            
            # Export data
            filepath = self.data_exporter.export_data(
                self.scraped_data, 
                format_type, 
                filename_prefix
            )
            
            # Export summary
            stats = self.get_session_stats()
            summary_path = self.data_exporter.export_summary(
                self.scraped_data, 
                stats, 
                f"{filename_prefix}_summary"
            )
            
            self.logger.info(f"Data saved to: {filepath}")
            self.logger.info(f"Summary saved to: {summary_path}")
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"Failed to save data: {str(e)}")
            raise ScrapingException(f"Failed to save data: {str(e)}")
    
    def clear_data(self):
        """Clear scraped data"""
        self.scraped_data.clear()
        self.logger.info("Scraped data cleared")
    
    def retry_operation(self, operation, max_retries: int = None, delay: float = None):
        """Retry an operation with exponential backoff"""
        max_retries = max_retries or self.config.retry_attempts
        delay = delay or self.config.retry_delay
        
        for attempt in range(max_retries):
            try:
                return operation()
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = delay * (2 ** attempt)  # Exponential backoff
                    self.logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {str(e)}")
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"All {max_retries} attempts failed: {str(e)}")
                    raise e 