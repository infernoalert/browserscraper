#!/usr/bin/env python3
"""
Test script for the Auto Loop functionality
This script tests the new auto loop feature that was added to web_explorer.py
"""

import sys
import os

def test_auto_loop_imports():
    """Test that the auto loop functionality can be imported"""
    print("Testing Auto Loop functionality...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from web_explorer import WebExplorer
        print("✓ WebExplorer imported successfully")
        
        # Create QApplication for testing
        app = QApplication([])
        
        # Test that the auto loop methods exist
        explorer = WebExplorer()
        
        # Check if auto loop methods exist
        if hasattr(explorer, 'start_auto_loop'):
            print("✓ start_auto_loop method exists")
        else:
            print("✗ start_auto_loop method missing")
            return False
            
        if hasattr(explorer, 'stop_auto_loop'):
            print("✓ stop_auto_loop method exists")
        else:
            print("✗ stop_auto_loop method missing")
            return False
            
        if hasattr(explorer, 'auto_loop_step'):
            print("✓ auto_loop_step method exists")
        else:
            print("✗ auto_loop_step method missing")
            return False
            
        if hasattr(explorer, 'iterations_spinbox'):
            print("✓ iterations_spinbox exists")
        else:
            print("✗ iterations_spinbox missing")
            return False
            
        if hasattr(explorer, 'auto_button'):
            print("✓ auto_button exists")
        else:
            print("✗ auto_button missing")
            return False
            
        if hasattr(explorer, 'auto_progress_bar'):
            print("✓ auto_progress_bar exists")
        else:
            print("✗ auto_progress_bar missing")
            return False
            
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        return False

def main():
    """Run the auto loop test"""
    print("Auto Loop Functionality Test")
    print("=" * 40)
    
    success = test_auto_loop_imports()
    
    print("\n" + "=" * 40)
    if success:
        print("✓ Auto loop functionality test passed!")
        print("\nNew features added:")
        print("  - Auto Loop section with iterations input (1-100)")
        print("  - Start Auto Loop button")
        print("  - Progress bar and status display")
        print("  - Automatic text extraction and saving")
        print("  - Automatic navigation to next page")
        print("\nTo use the auto loop:")
        print("  1. Navigate to a website")
        print("  2. Set the number of iterations (1-100)")
        print("  3. Enter the button text to click for next page")
        print("  4. Click 'Start Auto Loop'")
        print("  5. The app will automatically:")
        print("     - Extract text from current page")
        print("     - Save it to a file")
        print("     - Click the next page button")
        print("     - Repeat for the specified number of iterations")
    else:
        print("✗ Auto loop functionality test failed!")
        print("Please check the implementation and try again.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 