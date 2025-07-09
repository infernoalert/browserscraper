#!/usr/bin/env python3
"""
Example usage of the Web Explorer application
Demonstrates how to use the embedded browser with login and text extraction
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from web_explorer import WebExplorer

def main():
    """Main function to run the example"""
    print("Web Explorer - Text Extractor")
    print("=" * 40)
    print()
    print("This application provides:")
    print("1. Embedded web browser")
    print("2. Automatic login form handling")
    print("3. Text extraction from web pages")
    print("4. Batch text saving")
    print("5. Auto navigation capabilities")
    print()
    
    # Create the application
    app = QApplication(sys.argv)
    
    # Create and show the main window
    explorer = WebExplorer()
    explorer.show()
    
    # Example: Set up some default URLs for testing
    print("Example URLs you can try:")
    print("- https://example.com")
    print("- https://httpbin.org/forms/post")
    print("- https://quotes.toscrape.com")
    print("- https://books.toscrape.com")
    print()
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 