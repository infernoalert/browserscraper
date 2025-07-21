#!/usr/bin/env python3
"""
Simple GUI Launcher for Browser Scraper
This script launches the GUI interface for the browser scraper
"""

import sys
import os

def main():
    """Launch the GUI"""
    print("🚀 Starting Browser Scraper GUI...")
    print("📋 Make sure ChromeDriver is installed and matches your Chrome version!")
    
    try:
        # Try to import and run the standalone GUI first
        print("Trying standalone GUI...")
        from gui_standalone import main as standalone_main
        standalone_main()
        
    except ImportError:
        print("❌ Standalone GUI not found, trying modular GUI...")
        
        try:
            # Add the src directory to the Python path
            import os
            src_path = os.path.join(os.path.dirname(__file__), "src")
            sys.path.insert(0, src_path)
            
            # Import and run the simple GUI
            from ui.gui_simple import SimpleScraperGUI
            app = SimpleScraperGUI()
            app.run()
            
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("Make sure all dependencies are installed:")
            print("  pip install -r requirements.txt")
            print("\nTrying fallback GUI...")
            
            try:
                # Create a simple fallback GUI
                import tkinter as tk
                from tkinter import ttk, messagebox
                
                class FallbackGUI:
                    def __init__(self):
                        self.window = tk.Tk()
                        self.window.title("🌐 Browser Scraper - Fallback")
                        self.window.geometry("600x400")
                        
                        # Create interface
                        title_label = tk.Label(self.window, text="Browser Scraper GUI", font=("Arial", 16, "bold"))
                        title_label.pack(pady=20)
                        
                        info_label = tk.Label(self.window, text="GUI is starting...", font=("Arial", 12))
                        info_label.pack(pady=10)
                        
                        # Instructions
                        instructions = """
                        If you're seeing this, the main GUI couldn't load.
                        
                        Please try:
                        1. python gui_standalone.py
                        2. pip install selenium webdriver-manager
                        3. Check ChromeDriver installation
                        """
                        
                        info_text = tk.Text(self.window, height=8, width=60)
                        info_text.pack(pady=10, padx=20)
                        info_text.insert("1.0", instructions)
                        info_text.config(state="disabled")
                        
                        # Close button
                        close_btn = tk.Button(self.window, text="Close", command=self.window.destroy)
                        close_btn.pack(pady=20)
                        
                    def run(self):
                        self.window.mainloop()
                
                app = FallbackGUI()
                app.run()
                
            except Exception as e2:
                print(f"❌ Fallback GUI also failed: {e2}")
                print("\nPlease try:")
                print("1. python gui_standalone.py")
                print("2. pip install selenium webdriver-manager")
                print("3. Check your Python installation")
    
    except Exception as e:
        print(f"❌ Failed to start GUI: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure ChromeDriver is installed")
        print("2. Check that all dependencies are installed")
        print("3. Try running: pip install selenium webdriver-manager")
        print("4. Try the standalone GUI: python gui_standalone.py")
    
    input("\nPress Enter to exit...")

if __name__ == '__main__':
    main() 