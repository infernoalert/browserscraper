"""
Command-line interface for browser scraper
"""

import argparse
import sys
import json
from typing import Dict, List, Optional

# Try different import paths
try:
    from ..core.browser_manager import BrowserManager
    from ..core.scraper import WebScraper
    from ..core.config import config_manager
    from ..utils.logger import get_logger, get_session_logger
    from ..utils.file_utils import FileHandler, DataExporter
    from ..utils.exceptions import BrowserScraperException
except ImportError:
    # Try absolute imports
    try:
        from core.browser_manager import BrowserManager
        from core.scraper import WebScraper
        from core.config import config_manager
        from utils.logger import get_logger, get_session_logger
        from utils.file_utils import FileHandler, DataExporter
        from utils.exceptions import BrowserScraperException
    except ImportError:
        # Try with src prefix
        try:
            from src.core.browser_manager import BrowserManager
            from src.core.scraper import WebScraper
            from src.core.config import config_manager
            from src.utils.logger import get_logger, get_session_logger
            from src.utils.file_utils import FileHandler, DataExporter
            from src.utils.exceptions import BrowserScraperException
        except ImportError as e:
            print(f"Failed to import required modules: {e}")
            print("Please ensure all dependencies are installed:")
            print("pip install -r requirements.txt")
            sys.exit(1)


class CLI:
    """Command-line interface for browser scraper"""
    
    def __init__(self):
        self.config = config_manager.get_config()
        self.logger = get_logger(log_level=self.config.log_level, log_file=self.config.log_file)
        self.session_logger = get_session_logger(self.logger)
        self.browser_manager = None
        self.scraper = None
        
    def setup_parser(self) -> argparse.ArgumentParser:
        """Setup command-line argument parser"""
        parser = argparse.ArgumentParser(
            description="Browser Scraper - Extract data from websites using Selenium",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s scrape-page https://example.com --selectors "{'title': 'h1', 'content': 'p'}"
  %(prog)s scrape-table https://example.com/table --table-selector "table.data"
  %(prog)s scrape-links https://example.com --output csv
  %(prog)s scrape-images https://example.com --output json
  %(prog)s scrape-forms https://example.com
  %(prog)s scrape-pattern https://example.com --patterns "{'email': r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b'}"
  %(prog)s gui  # Launch GUI interface
  %(prog)s config  # Show current configuration
            """
        )
        
        # Global options
        parser.add_argument('--config', type=str, help='Path to configuration file')
        parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
        parser.add_argument('--browser', choices=['chrome', 'firefox'], default='chrome', 
                          help='Browser to use (default: chrome)')
        parser.add_argument('--output', choices=['json', 'csv', 'xml', 'txt'], default='json',
                          help='Output format (default: json)')
        parser.add_argument('--output-dir', type=str, default='output',
                          help='Output directory (default: output)')
        parser.add_argument('--filename', type=str, help='Output filename prefix')
        parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
        parser.add_argument('--quiet', '-q', action='store_true', help='Enable quiet mode')
        
        # Subcommands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Scrape page command
        scrape_page = subparsers.add_parser('scrape-page', help='Scrape a single page with CSS selectors')
        scrape_page.add_argument('url', help='URL to scrape')
        scrape_page.add_argument('--selectors', type=str, required=True,
                               help='JSON string of field_name -> CSS_selector mappings')
        scrape_page.add_argument('--multiple', action='store_true',
                               help='Extract multiple items instead of single item')
        
        # Scrape table command
        scrape_table = subparsers.add_parser('scrape-table', help='Scrape HTML table data')
        scrape_table.add_argument('url', help='URL containing the table')
        scrape_table.add_argument('--table-selector', default='table',
                                help='CSS selector for the table (default: table)')
        
        # Scrape links command
        scrape_links = subparsers.add_parser('scrape-links', help='Scrape all links from a page')
        scrape_links.add_argument('url', help='URL to scrape')
        scrape_links.add_argument('--link-selector', default='a',
                                help='CSS selector for links (default: a)')
        
        # Scrape images command
        scrape_images = subparsers.add_parser('scrape-images', help='Scrape all images from a page')
        scrape_images.add_argument('url', help='URL to scrape')
        scrape_images.add_argument('--img-selector', default='img',
                                 help='CSS selector for images (default: img)')
        
        # Scrape forms command
        scrape_forms = subparsers.add_parser('scrape-forms', help='Scrape form information from a page')
        scrape_forms.add_argument('url', help='URL to scrape')
        scrape_forms.add_argument('--form-selector', default='form',
                                help='CSS selector for forms (default: form)')
        
        # Scrape custom pattern command
        scrape_pattern = subparsers.add_parser('scrape-pattern', help='Scrape data using regex patterns')
        scrape_pattern.add_argument('url', help='URL to scrape')
        scrape_pattern.add_argument('--patterns', type=str, required=True,
                                  help='JSON string of field_name -> regex_pattern mappings')
        
        # GUI command
        gui = subparsers.add_parser('gui', help='Launch GUI interface')
        
        # Config command
        config = subparsers.add_parser('config', help='Show or manage configuration')
        config.add_argument('--show', action='store_true', help='Show current configuration')
        config.add_argument('--create-default', action='store_true', help='Create default configuration file')
        
        return parser
    
    def apply_args(self, args):
        """Apply command-line arguments to configuration"""
        if args.config:
            # Load custom config file
            config_manager.config_file = args.config
            config_manager.config = config_manager._load_config()
        
        if args.headless:
            self.config.browser.headless = True
        
        if args.browser:
            self.config.browser.browser_type = args.browser
        
        if args.output_dir:
            self.config.output.output_dir = args.output_dir
        
        if args.output:
            self.config.output.output_format = args.output
        
        if args.filename:
            self.config.output.filename_prefix = args.filename
        
        if args.verbose:
            self.config.log_level = 'DEBUG'
        
        if args.quiet:
            self.config.log_level = 'WARNING'
        
        # Update logger with new log level
        self.logger = get_logger(log_level=self.config.log_level, log_file=self.config.log_file)
        self.session_logger = get_session_logger(self.logger)
    
    def setup_scraper(self):
        """Setup browser manager and scraper"""
        try:
            # Create browser manager
            self.browser_manager = BrowserManager(self.config.browser, self.logger)
            self.browser_manager.start_browser()
            
            # Create file handler and data exporter
            file_handler = FileHandler(self.config.output.output_dir, self.logger)
            data_exporter = DataExporter(file_handler, self.logger)
            
            # Create scraper
            self.scraper = WebScraper(
                self.browser_manager, 
                self.config.scraping, 
                self.session_logger,
                data_exporter
            )
            
            self.logger.info("Scraper setup completed successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to setup scraper: {str(e)}")
            raise BrowserScraperException(f"Failed to setup scraper: {str(e)}")
    
    def cleanup(self):
        """Cleanup resources"""
        if self.browser_manager:
            self.browser_manager.close_browser()
        
        if self.session_logger:
            self.session_logger.end_session()
    
    def run_scrape_page(self, args):
        """Run scrape-page command"""
        try:
            if not self.scraper:
                self.logger.error("Scraper not initialized")
                return None
                
            # Parse selectors
            selectors = json.loads(args.selectors)
            
            # Scrape page
            data = self.scraper.scrape_page(args.url, selectors, args.multiple)
            
            # Save data
            filepath = self.scraper.save_data(
                self.config.output.output_format,
                self.config.output.filename_prefix or "scraped_page"
            )
            
            # Display results
            self.logger.info(f"Scraped {len(data)} items from {args.url}")
            self.logger.info(f"Data saved to: {filepath}")
            
            return data
            
        except json.JSONDecodeError:
            self.logger.error("Invalid JSON format for selectors")
            return None
        except Exception as e:
            self.logger.error(f"Failed to scrape page: {str(e)}")
            return None
    
    def run_scrape_table(self, args):
        """Run scrape-table command"""
        try:
            if not self.scraper:
                self.logger.error("Scraper not initialized")
                return None
                
            # Scrape table
            data = self.scraper.scrape_table(args.url, args.table_selector)
            
            # Save data
            filepath = self.scraper.save_data(
                self.config.output.output_format,
                self.config.output.filename_prefix or "scraped_table"
            )
            
            # Display results
            self.logger.info(f"Scraped {len(data)} rows from table at {args.url}")
            self.logger.info(f"Data saved to: {filepath}")
            
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to scrape table: {str(e)}")
            return None
    
    def run_scrape_links(self, args):
        """Run scrape-links command"""
        try:
            if not self.scraper:
                self.logger.error("Scraper not initialized")
                return None
                
            # Scrape links
            data = self.scraper.scrape_links(args.url, args.link_selector)
            
            # Save data
            filepath = self.scraper.save_data(
                self.config.output.output_format,
                self.config.output.filename_prefix or "scraped_links"
            )
            
            # Display results
            self.logger.info(f"Scraped {len(data)} links from {args.url}")
            self.logger.info(f"Data saved to: {filepath}")
            
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to scrape links: {str(e)}")
            return None
    
    def run_scrape_images(self, args):
        """Run scrape-images command"""
        try:
            if not self.scraper:
                self.logger.error("Scraper not initialized")
                return None
                
            # Scrape images
            data = self.scraper.scrape_images(args.url, args.img_selector)
            
            # Save data
            filepath = self.scraper.save_data(
                self.config.output.output_format,
                self.config.output.filename_prefix or "scraped_images"
            )
            
            # Display results
            self.logger.info(f"Scraped {len(data)} images from {args.url}")
            self.logger.info(f"Data saved to: {filepath}")
            
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to scrape images: {str(e)}")
            return None
    
    def run_scrape_forms(self, args):
        """Run scrape-forms command"""
        try:
            if not self.scraper:
                self.logger.error("Scraper not initialized")
                return None
                
            # Scrape forms
            data = self.scraper.scrape_forms(args.url, args.form_selector)
            
            # Save data
            filepath = self.scraper.save_data(
                self.config.output.output_format,
                self.config.output.filename_prefix or "scraped_forms"
            )
            
            # Display results
            self.logger.info(f"Scraped {len(data)} forms from {args.url}")
            self.logger.info(f"Data saved to: {filepath}")
            
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to scrape forms: {str(e)}")
            return None
    
    def run_scrape_pattern(self, args):
        """Run scrape-pattern command"""
        try:
            if not self.scraper:
                self.logger.error("Scraper not initialized")
                return None
                
            # Parse patterns
            patterns = json.loads(args.patterns)
            
            # Scrape with patterns
            data = self.scraper.scrape_custom_pattern(args.url, patterns)
            
            # Save data
            filepath = self.scraper.save_data(
                self.config.output.output_format,
                self.config.output.filename_prefix or "scraped_patterns"
            )
            
            # Display results
            self.logger.info(f"Scraped {len(data)} pattern matches from {args.url}")
            self.logger.info(f"Data saved to: {filepath}")
            
            return data
            
        except json.JSONDecodeError:
            self.logger.error("Invalid JSON format for patterns")
            return None
        except Exception as e:
            self.logger.error(f"Failed to scrape patterns: {str(e)}")
            return None
    
    def run_gui(self, args):
        """Run GUI command"""
        try:
            # Import GUI module - try different options
            try:
                from .gui_simple import SimpleScraperGUI
                self.logger.info("Starting Simple GUI interface...")
                app = SimpleScraperGUI()
                app.run()
            except ImportError:
                try:
                    from .gui import AdvancedScraperGUI
                    self.logger.info("Starting Advanced GUI interface...")
                    app = AdvancedScraperGUI()
                    app.run()
                except ImportError:
                    self.logger.error("GUI modules not available")
                    print("GUI not available. Try running: python gui_standalone.py")
            
        except Exception as e:
            self.logger.error(f"Failed to start GUI: {str(e)}")
            print(f"GUI error: {str(e)}")
            print("Try running: python gui_standalone.py")
    
    def run_config(self, args):
        """Run config command"""
        try:
            if args.show:
                # Show current configuration
                import json
                config_dict = {
                    'browser': {
                        'browser_type': self.config.browser.browser_type,
                        'headless': self.config.browser.headless,
                        'window_size': self.config.browser.window_size,
                        'implicit_wait': self.config.browser.implicit_wait,
                        'page_load_timeout': self.config.browser.page_load_timeout
                    },
                    'scraping': {
                        'default_delay': self.config.scraping.default_delay,
                        'retry_attempts': self.config.scraping.retry_attempts,
                        'retry_delay': self.config.scraping.retry_delay
                    },
                    'output': {
                        'output_dir': self.config.output.output_dir,
                        'output_format': self.config.output.output_format,
                        'filename_prefix': self.config.output.filename_prefix
                    },
                    'log_level': self.config.log_level,
                    'log_file': self.config.log_file
                }
                
                print(json.dumps(config_dict, indent=2))
                
            elif args.create_default:
                # Create default configuration file
                config_manager.create_default_config_file()
                print("Default configuration file created successfully")
                
            else:
                print("Use --show to display current configuration or --create-default to create config file")
                
        except Exception as e:
            self.logger.error(f"Failed to handle config command: {str(e)}")
    
    def run(self):
        """Main entry point"""
        try:
            # Setup parser
            parser = self.setup_parser()
            
            # Parse arguments
            args = parser.parse_args()
            
            # Show help if no command provided
            if not args.command:
                parser.print_help()
                return
            
            # Apply arguments
            self.apply_args(args)
            
            # Handle config command without setting up scraper
            if args.command == 'config':
                self.run_config(args)
                return
            
            # Handle GUI command
            if args.command == 'gui':
                self.run_gui(args)
                return
            
            # Setup scraper for other commands
            self.setup_scraper()
            
            # Run command
            if args.command == 'scrape-page':
                self.run_scrape_page(args)
            elif args.command == 'scrape-table':
                self.run_scrape_table(args)
            elif args.command == 'scrape-links':
                self.run_scrape_links(args)
            elif args.command == 'scrape-images':
                self.run_scrape_images(args)
            elif args.command == 'scrape-forms':
                self.run_scrape_forms(args)
            elif args.command == 'scrape-pattern':
                self.run_scrape_pattern(args)
            
        except KeyboardInterrupt:
            self.logger.info("Operation cancelled by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            sys.exit(1)
        finally:
            self.cleanup()


def main():
    """Main entry point for CLI"""
    cli = CLI()
    cli.run()


if __name__ == '__main__':
    main() 