#!/usr/bin/env python3
"""
Browser Scraper - Main Entry Point
A comprehensive web scraping tool with both CLI and GUI interfaces
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

def main():
    """Main entry point - route to CLI or GUI based on arguments"""
    
    # Check if GUI is requested or no arguments provided
    if len(sys.argv) == 1:
        # No arguments - show help for CLI
        print("🌐 Browser Scraper - Web Data Extraction Tool")
        print("=" * 50)
        print()
        print("Usage:")
        print("  python -m src.main <command> [options]")
        print("  python -m src.main gui                    # Launch GUI interface")
        print("  python -m src.main scrape-page <url>      # Scrape a page")
        print("  python -m src.main scrape-table <url>     # Scrape table data")
        print("  python -m src.main scrape-links <url>     # Scrape all links")
        print("  python -m src.main scrape-images <url>    # Scrape all images")
        print("  python -m src.main config --show          # Show configuration")
        print()
        print("For detailed help:")
        print("  python -m src.main --help")
        print()
        print("Quick start with GUI:")
        print("  python -m src.main gui")
        
        return
    
    # Check if GUI is specifically requested
    if len(sys.argv) > 1 and sys.argv[1] == 'gui':
        # Launch GUI
        try:
            from src.ui.gui import InteractiveSeleniumController
            print("🚀 Starting GUI interface...")
            app = InteractiveSeleniumController()
            app.run()
        except Exception as e:
            print(f"❌ Failed to start GUI: {e}")
            sys.exit(1)
    else:
        # Launch CLI
        try:
            from src.ui.cli import CLI
            cli = CLI()
            cli.run()
        except Exception as e:
            print(f"❌ Failed to start CLI: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main() 