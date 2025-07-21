#!/usr/bin/env python3
"""
Test script to verify imports and basic functionality
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test all imports"""
    print("🔍 Testing imports...")
    
    # Add src to path
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    
    try:
        # Test core imports
        print("Testing core imports...")
        from core.config import ConfigManager
        from core.browser_manager import BrowserManager
        from core.scraper import WebScraper
        print("✅ Core imports successful")
        
        # Test utils imports
        print("Testing utils imports...")
        from utils.logger import get_logger, get_session_logger
        from utils.file_utils import FileHandler, DataExporter
        from utils.exceptions import BrowserScraperException
        print("✅ Utils imports successful")
        
        # Test UI imports
        print("Testing UI imports...")
        from ui.cli import CLI
        from ui.gui_simple import SimpleScraperGUI
        print("✅ UI imports successful")
        
        # Test main module
        print("Testing main module...")
        from main import main
        print("✅ Main module import successful")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from core.config import ConfigManager
        config_manager = ConfigManager()
        config = config_manager.get_config()
        
        print(f"✅ Browser type: {config.browser.browser_type}")
        print(f"✅ Output directory: {config.output.output_dir}")
        print(f"✅ Log level: {config.log_level}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_logger():
    """Test logger functionality"""
    print("\n📝 Testing logger...")
    
    try:
        from utils.logger import get_logger
        logger = get_logger("test", "INFO")
        logger.info("Test log message")
        print("✅ Logger test successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Logger error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Browser Scraper Import Test")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Config Test", test_config),
        ("Logger Test", test_logger),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The codebase is working correctly.")
        print("\nYou can now run:")
        print("  python -m src.main gui")
        print("  python gui_standalone.py")
        print("  python run_gui.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 