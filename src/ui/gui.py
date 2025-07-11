"""
GUI interface for browser scraper (moved from original selenium_auto_extractor.py)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

class InteractiveSeleniumController:
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("Interactive Selenium Browser Controller")
        
        # Make window full-size and properly resizable
        self.window.state('zoomed')  # Maximize window on Windows
        self.window.resizable(True, True)
        
        # Configure root window grid to expand
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        # Selenium driver
        self.driver = None
        
        # Website options for the dropdown
        self.websites = {
            "Google": "https://www.google.com",
            "LinkedIn": "https://www.linkedin.com",
            "LinkedIn Login": "https://www.linkedin.com/login",
            "GitHub": "https://www.github.com",
            "Stack Overflow": "https://stackoverflow.com",
            "YouTube": "https://www.youtube.com",
            "Facebook": "https://www.facebook.com",
            "Twitter": "https://www.twitter.com",
            "Wikipedia": "https://www.wikipedia.org",
            "Reddit": "https://www.reddit.com"
        }
        
        self.setup_gui()
        self.start_browser()
        
    def setup_gui(self):
        """Create the GUI elements"""
        # Main frame with more padding for full-screen layout
        main_frame = ttk.Frame(self.window, padding="40")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure main frame to expand
        main_frame.grid_rowconfigure(2, weight=1)  # Website selection frame
        main_frame.grid_rowconfigure(3, weight=1)  # Control buttons frame
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🌐 Interactive Selenium Browser Controller", 
                               font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Starting browser...", 
                                     font=("Arial", 12))
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Website selection frame
        selection_frame = ttk.LabelFrame(main_frame, text="Website Selection", padding="20")
        selection_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 30), ipady=10)
        
        # Dropdown label
        ttk.Label(selection_frame, text="Choose a website:", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Dropdown (Combobox)
        self.website_var = tk.StringVar()
        self.website_dropdown = ttk.Combobox(selection_frame, textvariable=self.website_var, 
                                           values=list(self.websites.keys()), 
                                           state="readonly", width=40, font=("Arial", 11))
        self.website_dropdown.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.website_dropdown.set("Google")  # Default selection
        
        # Go button
        self.go_button = ttk.Button(selection_frame, text="🚀 Go to Website", 
                                   command=self.go_to_website, state="disabled")
        self.go_button.grid(row=2, column=0, pady=(0, 15), ipadx=20, ipady=5)
        
        # Current URL display
        self.url_label = ttk.Label(selection_frame, text="Current URL: Not loaded", 
                                  font=("Arial", 10), foreground="blue")
        self.url_label.grid(row=3, column=0, sticky="w", pady=(10, 0))
        
        # Control buttons frame
        control_frame = ttk.LabelFrame(main_frame, text="Browser Controls", padding="20")
        control_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 30), ipady=10)
        
        # Configure control frame for even spacing
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)
        control_frame.grid_columnconfigure(2, weight=1)
        
        # Refresh button
        self.refresh_button = ttk.Button(control_frame, text="🔄 Refresh Page", 
                                        command=self.refresh_page, state="disabled")
        self.refresh_button.grid(row=0, column=0, padx=20, pady=10, ipadx=15, ipady=5)
        
        # Back button
        self.back_button = ttk.Button(control_frame, text="⬅️ Go Back", 
                                     command=self.go_back, state="disabled")
        self.back_button.grid(row=0, column=1, padx=20, pady=10, ipadx=15, ipady=5)
        
        # Forward button
        self.forward_button = ttk.Button(control_frame, text="➡️ Go Forward", 
                                        command=self.go_forward, state="disabled")
        self.forward_button.grid(row=0, column=2, padx=20, pady=10, ipadx=15, ipady=5)
        
        # Finish button frame
        finish_frame = ttk.Frame(main_frame)
        finish_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        self.finish_button = ttk.Button(finish_frame, text="🏁 Finish & Close Browser", 
                                       command=self.finish, style="Accent.TButton")
        self.finish_button.grid(row=0, column=0, ipadx=30, ipady=10)
        
        # Instructions
        instructions = """
Instructions:
1. Select a website from the dropdown
2. Click 'Go to Website' to navigate
3. Use browser controls as needed
4. Click 'Finish' when done to close everything
        """
        instruction_label = ttk.Label(main_frame, text=instructions, 
                                     font=("Arial", 11), foreground="gray")
        instruction_label.grid(row=5, column=0, columnspan=2, pady=(30, 0))
        
        # Configure column weight for resizing
        selection_frame.columnconfigure(0, weight=1)
        
    def start_browser(self):
        """Start the Selenium browser in a separate thread"""
        def start_browser_thread():
            try:
                self.status_label.config(text="Starting Chrome browser...")
                
                # Set up Chrome options
                chrome_options = Options()
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--window-size=1200,800')
                # Don't use headless mode so user can see the browser
                
                # Start Chrome
                self.driver = webdriver.Chrome(options=chrome_options)
                self.driver.implicitly_wait(10)
                
                # Update GUI in main thread
                self.window.after(0, self.browser_started)
                
            except WebDriverException as e:
                error_msg = f"Failed to start browser: {str(e)}"
                self.window.after(0, lambda: self.browser_error(error_msg))
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                self.window.after(0, lambda: self.browser_error(error_msg))
        
        # Start browser in background thread
        browser_thread = threading.Thread(target=start_browser_thread, daemon=True)
        browser_thread.start()
    
    def browser_started(self):
        """Called when browser successfully starts"""
        self.status_label.config(text="✅ Browser ready! Select a website and click 'Go'")
        self.go_button.config(state="normal")
        self.refresh_button.config(state="normal")
        self.back_button.config(state="normal")
        self.forward_button.config(state="normal")
        
    def browser_error(self, error_msg):
        """Called when browser fails to start"""
        self.status_label.config(text="❌ Failed to start browser")
        messagebox.showerror("Browser Error", 
                           f"{error_msg}\n\nMake sure ChromeDriver is installed and matches your Chrome version.")
        
    def go_to_website(self):
        """Navigate to the selected website"""
        if not self.driver:
            messagebox.showerror("Error", "Browser not available")
            return
            
        selected_site = self.website_var.get()
        if not selected_site:
            messagebox.showwarning("Warning", "Please select a website first")
            return
            
        url = self.websites[selected_site]
        
        try:
            self.status_label.config(text=f"🌐 Navigating to {selected_site}...")
            self.driver.get(url)
            
            # Update URL display
            current_url = self.driver.current_url
            display_url = current_url if len(current_url) <= 60 else current_url[:57] + "..."
            self.url_label.config(text=f"Current URL: {display_url}")
            
            self.status_label.config(text=f"✅ Successfully loaded {selected_site}")
            
        except Exception as e:
            self.status_label.config(text="❌ Failed to navigate")
            messagebox.showerror("Navigation Error", f"Failed to navigate to {url}\n\nError: {str(e)}")
    
    def refresh_page(self):
        """Refresh the current page"""
        if not self.driver:
            return
        try:
            self.driver.refresh()
            self.status_label.config(text="🔄 Page refreshed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh page: {str(e)}")
    
    def go_back(self):
        """Go back to previous page"""
        if not self.driver:
            return
        try:
            self.driver.back()
            current_url = self.driver.current_url
            display_url = current_url if len(current_url) <= 60 else current_url[:57] + "..."
            self.url_label.config(text=f"Current URL: {display_url}")
            self.status_label.config(text="⬅️ Went back")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to go back: {str(e)}")
    
    def go_forward(self):
        """Go forward to next page"""
        if not self.driver:
            return
        try:
            self.driver.forward()
            current_url = self.driver.current_url
            display_url = current_url if len(current_url) <= 60 else current_url[:57] + "..."
            self.url_label.config(text=f"Current URL: {display_url}")
            self.status_label.config(text="➡️ Went forward")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to go forward: {str(e)}")
    
    def finish(self):
        """Close browser and exit application"""
        try:
            if self.driver:
                self.driver.quit()
                self.status_label.config(text="Browser closed")
        except:
            pass  # Ignore errors when closing
        
        self.window.destroy()
    
    def run(self):
        """Start the GUI application"""
        # Handle window close button
        self.window.protocol("WM_DELETE_WINDOW", self.finish)
        
        # Start the GUI main loop
        self.window.mainloop()


def main():
    """Main function to start the interactive controller"""
    print("🚀 Starting Interactive Selenium Browser Controller...")
    print("📋 Make sure ChromeDriver is installed and matches your Chrome version!")
    
    try:
        app = InteractiveSeleniumController()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        input("Press Enter to exit...")


if __name__ == '__main__':
    main() 