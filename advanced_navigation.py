"""
Advanced Navigation Module for Web Explorer
Provides enhanced navigation capabilities including automatic pagination,
link following, and custom navigation patterns.
"""

import re
from typing import List, Dict, Optional, Callable
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView

class NavigationPattern:
    """Defines a navigation pattern for automatic page traversal"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.conditions = []
        self.actions = []
        
    def add_condition(self, condition: Callable):
        """Add a condition that must be met for navigation"""
        self.conditions.append(condition)
        
    def add_action(self, action: Callable):
        """Add an action to perform during navigation"""
        self.actions.append(action)

class AdvancedNavigator(QObject):
    """Handles advanced navigation patterns and automatic page traversal"""
    
    # Signals
    page_loaded = pyqtSignal(str)  # Emitted when a page is loaded
    navigation_complete = pyqtSignal()  # Emitted when navigation is complete
    error_occurred = pyqtSignal(str)  # Emitted when an error occurs
    
    def __init__(self, web_view: QWebEngineView):
        super().__init__()
        self.web_view = web_view
        self.navigation_patterns = {}
        self.current_pattern = None
        self.visited_urls = set()
        self.max_pages = 100  # Maximum pages to visit
        self.delay_between_pages = 3000  # 3 seconds
        
        # Common navigation patterns
        self._setup_common_patterns()
        
    def _setup_common_patterns(self):
        """Setup common navigation patterns"""
        
        # Next page pattern
        next_page_pattern = NavigationPattern("next_page", "Follow 'Next' or 'Page X' links")
        next_page_pattern.add_condition(self._has_next_page_link)
        next_page_pattern.add_action(self._click_next_page_link)
        self.navigation_patterns["next_page"] = next_page_pattern
        
        # Pagination pattern
        pagination_pattern = NavigationPattern("pagination", "Follow pagination links")
        pagination_pattern.add_condition(self._has_pagination_links)
        pagination_pattern.add_action(self._click_pagination_link)
        self.navigation_patterns["pagination"] = pagination_pattern
        
        # Article list pattern
        article_list_pattern = NavigationPattern("article_list", "Follow article links in a list")
        article_list_pattern.add_condition(self._has_article_links)
        article_list_pattern.add_action(self._click_article_link)
        self.navigation_patterns["article_list"] = article_list_pattern
        
    def set_navigation_pattern(self, pattern_name: str):
        """Set the current navigation pattern"""
        if pattern_name in self.navigation_patterns:
            self.current_pattern = self.navigation_patterns[pattern_name]
        else:
            raise ValueError(f"Unknown navigation pattern: {pattern_name}")
            
    def start_auto_navigation(self, start_url: str, max_pages: int = 100):
        """Start automatic navigation from a given URL"""
        self.max_pages = max_pages
        self.visited_urls.clear()
        self.visited_urls.add(start_url)
        
        # Load the start URL
        self.web_view.load(start_url)
        
    def _has_next_page_link(self) -> bool:
        """Check if the current page has a 'Next' link"""
        js_code = """
        function hasNextPageLink() {
            const nextSelectors = [
                'a[href*="next"]',
                'a:contains("Next")',
                'a:contains("next")',
                'a[rel="next"]',
                'a.next',
                'a[class*="next"]',
                'a[title*="Next"]',
                'a[aria-label*="Next"]'
            ];
            
            for (let selector of nextSelectors) {
                if (document.querySelector(selector)) {
                    return true;
                }
            }
            
            // Check for text content
            const links = document.querySelectorAll('a');
            for (let link of links) {
                const text = link.textContent.toLowerCase();
                if (text.includes('next') || text.includes('>') || text.includes('forward')) {
                    return true;
                }
            }
            
            return false;
        }
        hasNextPageLink();
        """
        
        # This would need to be implemented with proper JavaScript execution
        # For now, return a placeholder - you'll need to implement this
        return True  # Placeholder
        
    def _click_next_page_link(self):
        """Click the next page link"""
        js_code = """
        function clickNextPageLink() {
            const nextSelectors = [
                'a[href*="next"]',
                'a:contains("Next")',
                'a:contains("next")',
                'a[rel="next"]',
                'a.next',
                'a[class*="next"]',
                'a[title*="Next"]',
                'a[aria-label*="Next"]'
            ];
            
            for (let selector of nextSelectors) {
                const link = document.querySelector(selector);
                if (link) {
                    link.click();
                    return true;
                }
            }
            
            // Check for text content
            const links = document.querySelectorAll('a');
            for (let link of links) {
                const text = link.textContent.toLowerCase();
                if (text.includes('next') || text.includes('>') || text.includes('forward')) {
                    link.click();
                    return true;
                }
            }
            
            return false;
        }
        clickNextPageLink();
        """
        
        # This would need to be implemented with proper JavaScript execution
        pass
        
    def _has_pagination_links(self) -> bool:
        """Check if the current page has pagination links"""
        js_code = """
        function hasPaginationLinks() {
            const paginationSelectors = [
                '.pagination',
                '.pager',
                '[class*="pagination"]',
                '[class*="pager"]',
                'nav[aria-label*="pagination"]',
                'nav[aria-label*="pager"]'
            ];
            
            for (let selector of paginationSelectors) {
                if (document.querySelector(selector)) {
                    return true;
                }
            }
            
            return false;
        }
        hasPaginationLinks();
        """
        
        return True  # Placeholder
        
    def _click_pagination_link(self):
        """Click the next pagination link"""
        js_code = """
        function clickPaginationLink() {
            const paginationSelectors = [
                '.pagination a',
                '.pager a',
                '[class*="pagination"] a',
                '[class*="pager"] a'
            ];
            
            for (let selector of paginationSelectors) {
                const links = document.querySelectorAll(selector);
                for (let link of links) {
                    const text = link.textContent.toLowerCase();
                    if (text.includes('next') || text.includes('>') || text.includes('forward')) {
                        link.click();
                        return true;
                    }
                }
            }
            
            return false;
        }
        clickPaginationLink();
        """
        
        pass
        
    def _has_article_links(self) -> bool:
        """Check if the current page has article links"""
        js_code = """
        function hasArticleLinks() {
            const articleSelectors = [
                'article a',
                '.article a',
                '.post a',
                '.entry a',
                'h1 a',
                'h2 a',
                'h3 a'
            ];
            
            for (let selector of articleSelectors) {
                if (document.querySelectorAll(selector).length > 0) {
                    return true;
                }
            }
            
            return false;
        }
        hasArticleLinks();
        """
        
        return True  # Placeholder
        
    def _click_article_link(self):
        """Click the first unvisited article link"""
        js_code = """
        function clickArticleLink() {
            const articleSelectors = [
                'article a',
                '.article a',
                '.post a',
                '.entry a',
                'h1 a',
                'h2 a',
                'h3 a'
            ];
            
            for (let selector of articleSelectors) {
                const links = document.querySelectorAll(selector);
                for (let link of links) {
                    if (link.href && !link.href.includes('#')) {
                        link.click();
                        return true;
                    }
                }
            }
            
            return false;
        }
        clickArticleLink();
        """
        
        pass

class URLManager:
    """Manages URLs for batch processing"""
    
    def __init__(self):
        self.url_list = []
        self.current_index = 0
        self.visited_urls = set()
        
    def add_url(self, url: str):
        """Add a URL to the list"""
        if url not in self.url_list:
            self.url_list.append(url)
            
    def add_urls_from_file(self, filename: str):
        """Add URLs from a text file (one URL per line)"""
        try:
            with open(filename, 'r') as f:
                for line in f:
                    url = line.strip()
                    if url and not url.startswith('#'):
                        self.add_url(url)
        except FileNotFoundError:
            raise FileNotFoundError(f"URL file not found: {filename}")
            
    def get_next_url(self) -> Optional[str]:
        """Get the next unvisited URL"""
        while self.current_index < len(self.url_list):
            url = self.url_list[self.current_index]
            self.current_index += 1
            if url not in self.visited_urls:
                self.visited_urls.add(url)
                return url
        return None
        
    def mark_url_visited(self, url: str):
        """Mark a URL as visited"""
        self.visited_urls.add(url)
        
    def reset(self):
        """Reset the URL manager"""
        self.current_index = 0
        self.visited_urls.clear()
        
    def get_progress(self) -> Dict:
        """Get progress information"""
        total = len(self.url_list)
        visited = len(self.visited_urls)
        remaining = total - visited
        
        return {
            'total': total,
            'visited': visited,
            'remaining': remaining,
            'current_index': self.current_index
        }

class NavigationConfig:
    """Configuration for navigation behavior"""
    
    def __init__(self):
        self.delay_between_pages = 3000  # milliseconds
        self.max_pages_per_session = 100
        self.extract_text_on_each_page = True
        self.save_after_each_page = False
        self.follow_redirects = True
        self.respect_robots_txt = True
        self.user_agent = "Web Explorer Bot/1.0"
        
    def set_delay(self, seconds: int):
        """Set delay between pages in seconds"""
        self.delay_between_pages = seconds * 1000
        
    def set_max_pages(self, max_pages: int):
        """Set maximum pages to visit per session"""
        self.max_pages_per_session = max_pages
        
    def enable_text_extraction(self, enable: bool = True):
        """Enable or disable text extraction on each page"""
        self.extract_text_on_each_page = enable
        
    def enable_auto_save(self, enable: bool = True):
        """Enable or disable automatic saving after each page"""
        self.save_after_each_page = enable 