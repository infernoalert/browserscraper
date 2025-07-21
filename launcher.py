#!/usr/bin/env python3
"""
Browser Scraper Launcher
A simple launcher that handles import issues and provides multiple entry points
"""

import sys
import os
from pathlib import Path

def setup_paths():
    """Setup Python paths for imports"""
    # Add current directory and src to path
    current_dir = Path(__file__).parent
    src_dir = current_dir / "src"
    
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []
    
    try:
        import tkinter
    except ImportError:
        missing_deps.append("tkinter")
    
    try:
        import selenium
    except ImportError:
        missing_deps.append("selenium")
    
    try:
        import pandas
    except ImportError:
        missing_deps.append("pandas")
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True

def launch_gui():
    """Launch the GUI interface"""
    print("🚀 Launching Browser Scraper GUI...")
    
    # Try different GUI options
    gui_options = [
        ("Standalone GUI", "gui_standalone.py"),
        ("Simple GUI", "src/ui/gui_simple.py"),
        ("Advanced GUI", "src/ui/gui.py"),
    ]
    
    for name, path in gui_options:
        try:
            print(f"Trying {name}...")
            if path.endswith('.py'):
                # Run as script
                os.system(f"python {path}")
                return True
            else:
                # Import and run
                module_path = path.replace('/', '.').replace('.py', '')
                module = __import__(module_path, fromlist=['main'])
                if hasattr(module, 'main'):
                    module.main()
                    return True
        except Exception as e:
            print(f"Failed to launch {name}: {e}")
            continue
    
    print("❌ All GUI options failed")
    return False

def launch_cli():
    """Launch the CLI interface"""
    print("🚀 Launching Browser Scraper CLI...")
    
    try:
        # Try to run the main module
        os.system("python -m src.main cli")
        return True
    except Exception as e:
        print(f"Failed to launch CLI: {e}")
        return False

def show_help():
    """Show help information"""
    print("🌐 Browser Scraper Launcher")
    print("=" * 40)
    print()
    print("Usage:")
    print("  python launcher.py gui     - Launch GUI")
    print("  python launcher.py cli     - Launch CLI")
    print("  python launcher.py test    - Run tests")
    print("  python launcher.py help    - Show this help")
    print()
    print("Alternative launchers:")
    print("  python gui_standalone.py   - Standalone GUI")
    print("  python run_gui.py          - Modular GUI")
    print("  python demo_gui.py         - Demo with checks")
    print("  python -m src.main gui     - Main module GUI")
    print("  python -m src.main cli     - Main module CLI")
    print()

def run_tests():
    """Run basic tests"""
    print("🧪 Running tests...")
    
    setup_paths()
    
    if not check_dependencies():
        return False
    
    try:
        # Test basic imports
        from src.core.config import ConfigManager
        config = ConfigManager().get_config()
        print(f"✅ Configuration loaded: {config.browser.browser_type}")
        
        from src.utils.logger import get_logger
        logger = get_logger("test")
        logger.info("Test log message")
        print("✅ Logger working")
        
        print("✅ Basic tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main launcher function"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        show_help()
    elif command == "gui":
        setup_paths()
        if check_dependencies():
            launch_gui()
        else:
            print("❌ Cannot launch GUI - missing dependencies")
    elif command == "cli":
        setup_paths()
        if check_dependencies():
            launch_cli()
        else:
            print("❌ Cannot launch CLI - missing dependencies")
    elif command == "test":
        if run_tests():
            print("🎉 Tests passed!")
        else:
            print("❌ Tests failed")
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == '__main__':
    main() 