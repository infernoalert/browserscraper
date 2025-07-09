#!/usr/bin/env python3
"""
Test script to verify Web Explorer setup
Run this before starting development to ensure everything is working
"""

import sys
import os

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    try:
        import PyQt5
        print("✓ PyQt5 imported successfully")
    except ImportError as e:
        print(f"✗ PyQt5 import failed: {e}")
        return False
    
    try:
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        print("✓ PyQtWebEngine imported successfully")
    except ImportError as e:
        print(f"✗ PyQtWebEngine import failed: {e}")
        print("  Please install with: pip install PyQtWebEngine")
        return False
    
    try:
        import requests
        print("✓ requests imported successfully")
    except ImportError as e:
        print(f"✗ requests import failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✓ beautifulsoup4 imported successfully")
    except ImportError as e:
        print(f"✗ beautifulsoup4 import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        import json
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✓ config.json loaded successfully")
        return True
    except FileNotFoundError:
        print("✗ config.json not found")
        return False
    except json.JSONDecodeError as e:
        print(f"✗ config.json is invalid: {e}")
        return False

def test_modules():
    """Test custom modules"""
    print("\nTesting custom modules...")
    
    try:
        from web_explorer import WebExplorer
        print("✓ web_explorer module imported successfully")
    except ImportError as e:
        print(f"✗ web_explorer import failed: {e}")
        return False
    
    try:
        from advanced_navigation import AdvancedNavigator
        print("✓ advanced_navigation module imported successfully")
    except ImportError as e:
        print(f"✗ advanced_navigation import failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("Web Explorer Setup Test")
    print("=" * 30)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test configuration
    if not test_config():
        all_passed = False
    
    # Test modules
    if not test_modules():
        all_passed = False
    
    print("\n" + "=" * 30)
    if all_passed:
        print("✓ All tests passed! You're ready to start coding.")
        print("\nTo run the application:")
        print("  python web_explorer.py")
        print("  or")
        print("  run_app.bat")
    else:
        print("✗ Some tests failed. Please fix the issues above before continuing.")
        print("\nCommon solutions:")
        print("  1. Install missing packages: pip install -r requirements.txt")
        print("  2. Check that all files are in the correct directory")
        print("  3. Ensure Python 3.7+ is installed")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 