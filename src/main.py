#!/usr/bin/env python3
"""
Main entry point for Browser Scraper
Supports both CLI and GUI interfaces
"""

import sys
import argparse
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from ui.cli import CLI
    from ui.gui_simple import SimpleScraperGUI
except ImportError as e:
    print(f"Import error: {e}")
    print("Trying alternative import paths...")
    
    # Try alternative import paths
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from src.ui.cli import CLI
        from src.ui.gui_simple import SimpleScraperGUI
    except ImportError:
        print("Failed to import modules. Please check the installation.")
        sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Browser Scraper - Web scraping tool with CLI and GUI interfaces",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start GUI
  python -m src.main gui
  
  # CLI scraping
  python -m src.main scrape-page https://example.com --selectors '{"title": "h1"}'
  
  # Show help
  python -m src.main --help
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        default='gui',
        choices=['gui', 'cli', 'scrape-page', 'scrape-table', 'scrape-links', 
                'scrape-images', 'scrape-forms', 'scrape-pattern', 'config'],
        help='Command to run (default: gui)'
    )
    
    # Add other arguments for CLI commands
    parser.add_argument('url', nargs='?', help='URL to scrape')
    parser.add_argument('--selectors', help='CSS selectors in JSON format')
    parser.add_argument('--output', choices=['json', 'csv', 'xml', 'txt'], default='json', help='Output format')
    parser.add_argument('--filename', help='Output filename')
    parser.add_argument('--output-dir', default='output', help='Output directory')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    parser.add_argument('--browser', choices=['chrome', 'firefox'], default='chrome', help='Browser to use')
    parser.add_argument('--verbose', action='store_true', help='Verbose logging')
    parser.add_argument('--config', help='Configuration file path')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'gui':
            print("🚀 Starting Browser Scraper GUI...")
            app = SimpleScraperGUI()
            app.run()
        elif args.command == 'cli':
            print("🚀 Starting Browser Scraper CLI...")
            cli = CLI()
            cli.run()
        else:
            # Handle CLI scraping commands
            if not args.url:
                print("❌ Error: URL is required for scraping commands")
                parser.print_help()
                return
            
            cli = CLI()
            
            # Create a mock args object for the CLI methods
            class MockArgs:
                def __init__(self, **kwargs):
                    for key, value in kwargs.items():
                        setattr(self, key, value)
            
            if args.command == 'scrape-page':
                mock_args = MockArgs(
                    url=args.url,
                    selectors=args.selectors or '{}',
                    multiple=False
                )
                cli.run_scrape_page(mock_args)
            elif args.command == 'scrape-table':
                mock_args = MockArgs(
                    url=args.url,
                    table_selector='table'
                )
                cli.run_scrape_table(mock_args)
            elif args.command == 'scrape-links':
                mock_args = MockArgs(
                    url=args.url,
                    link_selector='a'
                )
                cli.run_scrape_links(mock_args)
            elif args.command == 'scrape-images':
                mock_args = MockArgs(
                    url=args.url,
                    img_selector='img'
                )
                cli.run_scrape_images(mock_args)
            elif args.command == 'scrape-forms':
                mock_args = MockArgs(
                    url=args.url,
                    form_selector='form'
                )
                cli.run_scrape_forms(mock_args)
            elif args.command == 'scrape-pattern':
                mock_args = MockArgs(
                    url=args.url,
                    patterns=args.selectors or '{}'
                )
                cli.run_scrape_pattern(mock_args)
            elif args.command == 'config':
                mock_args = MockArgs()
                cli.run_config(mock_args)
    
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    main() 