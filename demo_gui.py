#!/usr/bin/env python3
"""
GUI Demonstration Script for Browser Scraper
This script demonstrates the GUI features and provides usage examples
"""

import sys
import os
from pathlib import Path

def show_demo_info():
    """Show demonstration information"""
    print("🌐 Browser Scraper GUI Demonstration")
    print("=" * 50)
    print()
    print("Features:")
    print("✅ Browser Control - Start/stop Chrome/Firefox")
    print("✅ URL Navigation - Navigate to any website")
    print("✅ CSS Selectors - Extract data using CSS selectors")
    print("✅ Multiple Formats - Export to JSON, CSV, XML, TXT")
    print("✅ Real-time Logging - See scraping progress")
    print("✅ File Management - Choose output directories")
    print("✅ Preview Mode - See page elements before scraping")
    print()
    print("Example Usage:")
    print("1. Launch GUI: python run_gui.py")
    print("2. Enter URL: https://example.com")
    print("3. Set CSS selectors: {'title': 'h1', 'content': 'p'}")
    print("4. Choose output format: JSON")
    print("5. Click 'Start Browser' then 'Start Scraping'")
    print()
    print("Sample CSS Selectors:")
    print("- {'title': 'h1'} - Extract page title")
    print("- {'price': '.price'} - Extract price elements")
    print("- {'links': 'a'} - Extract all links")
    print("- {'images': 'img'} - Extract all images")
    print()
    print("Output Formats:")
    print("- JSON: Structured data with field names")
    print("- CSV: Spreadsheet-friendly format")
    print("- XML: Hierarchical data structure")
    print("- TXT: Plain text output")
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    missing_deps = []
    
    try:
        import tkinter
        print("✅ tkinter - GUI framework")
    except ImportError:
        missing_deps.append("tkinter")
        print("❌ tkinter - Not available")
    
    try:
        import selenium
        print("✅ selenium - Browser automation")
    except ImportError:
        missing_deps.append("selenium")
        print("❌ selenium - Not installed")
    
    try:
        import pandas
        print("✅ pandas - Data processing")
    except ImportError:
        missing_deps.append("pandas")
        print("❌ pandas - Not installed")
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Install with: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies available")
        return True

def check_chromedriver():
    """Check if ChromeDriver is available"""
    print("\n🔍 Checking ChromeDriver...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        driver.quit()
        print("✅ ChromeDriver is working")
        return True
    except Exception as e:
        print(f"❌ ChromeDriver issue: {e}")
        print("\nTo fix ChromeDriver:")
        print("1. Download ChromeDriver from: https://chromedriver.chromium.org/")
        print("2. Place chromedriver.exe in the project directory")
        print("3. Or install webdriver-manager: pip install webdriver-manager")
        return False

def main():
    """Main demonstration function"""
    print("🚀 Browser Scraper GUI Demo")
    print("=" * 50)
    print()
    
    # Show demo information
    show_demo_info()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot run GUI - missing dependencies")
        return
    
    # Check ChromeDriver
    if not check_chromedriver():
        print("\n⚠️ ChromeDriver not working - GUI may not function properly")
    
    print("\n🎯 Ready to launch GUI!")
    print("Run: python run_gui.py")
    print()
    
    # Ask if user wants to launch GUI
    try:
        response = input("Launch GUI now? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            print("\n🚀 Launching GUI...")
            
            # Add src to path
            sys.path.insert(0, str(Path(__file__).parent / "src"))
            
            # Import and run GUI
            from ui.gui_simple import SimpleScraperGUI
            app = SimpleScraperGUI()
            app.run()
        else:
            print("\n👋 Demo completed. Run 'python run_gui.py' when ready!")
    except KeyboardInterrupt:
        print("\n\n👋 Demo cancelled")
    except Exception as e:
        print(f"\n❌ Error launching GUI: {e}")
        print("Try running: python run_gui.py")

if __name__ == '__main__':
    main() 