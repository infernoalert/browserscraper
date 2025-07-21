#!/usr/bin/env python3
"""
Standalone Browser Scraper GUI
A simple GUI that works without complex module dependencies
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import json
import os
import time
from datetime import datetime
from pathlib import Path
import webbrowser

# Try to import selenium, but don't fail if not available
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import WebDriverException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️ Selenium not available - browser automation disabled")


class StandaloneScraperGUI:
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("🌐 Browser Scraper GUI")
        self.window.geometry("1200x800")
        self.window.minsize(1000, 600)
        
        # Configure window
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        
        # Initialize components
        self.driver = None
        
        # Initialize GUI
        self.setup_gui()
        self.setup_styles()
        
    def setup_styles(self):
        """Configure custom styles for the GUI"""
        style = ttk.Style()
        
        # Configure styles
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        style.configure("Subtitle.TLabel", font=("Arial", 12, "bold"))
        style.configure("Status.TLabel", font=("Arial", 10))
        style.configure("Success.TLabel", foreground="green")
        style.configure("Error.TLabel", foreground="red")
        style.configure("Warning.TLabel", foreground="orange")
        
        # Button styles
        style.configure("Primary.TButton", font=("Arial", 10, "bold"))
        style.configure("Secondary.TButton", font=("Arial", 9))
        style.configure("Danger.TButton", font=("Arial", 9), foreground="red")
        
    def setup_gui(self):
        """Create the main GUI layout"""
        # Create main container
        main_container = ttk.Frame(self.window)
        main_container.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        
        # Title
        title_frame = ttk.Frame(main_container)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="🌐 Browser Scraper GUI", 
                               style="Title.TLabel")
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Simple Web Scraping Tool", 
                                  style="Subtitle.TLabel", foreground="gray")
        subtitle_label.pack()
        
        # Create left panel (controls)
        self.create_left_panel(main_container)
        
        # Create right panel (output and browser info)
        self.create_right_panel(main_container)
        
        # Create bottom panel (status and logs)
        self.create_bottom_panel(main_container)
        
    def create_left_panel(self, parent):
        """Create the left control panel"""
        left_frame = ttk.LabelFrame(parent, text="🎛️ Scraping Controls", padding="10")
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        left_frame.grid_rowconfigure(6, weight=1)
        
        # URL Input
        url_frame = ttk.Frame(left_frame)
        url_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        ttk.Label(url_frame, text="Target URL:", style="Subtitle.TLabel").grid(row=0, column=0, sticky="w")
        self.url_var = tk.StringVar(value="https://example.com")
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=40)
        url_entry.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        
        # Browser Controls
        browser_frame = ttk.LabelFrame(left_frame, text="🌐 Browser Settings", padding="10")
        browser_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Browser type
        ttk.Label(browser_frame, text="Browser:").grid(row=0, column=0, sticky="w")
        self.browser_var = tk.StringVar(value="chrome")
        browser_combo = ttk.Combobox(browser_frame, textvariable=self.browser_var, 
                                    values=["chrome", "firefox"], state="readonly", width=15)
        browser_combo.grid(row=1, column=0, sticky="w", pady=(5, 10))
        
        # Headless mode
        self.headless_var = tk.BooleanVar(value=False)
        headless_check = ttk.Checkbutton(browser_frame, text="Headless Mode", 
                                       variable=self.headless_var)
        headless_check.grid(row=2, column=0, sticky="w", pady=(0, 10))
        
        # Browser control buttons
        browser_btn_frame = ttk.Frame(browser_frame)
        browser_btn_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        
        self.start_browser_btn = ttk.Button(browser_btn_frame, text="🚀 Start Browser", 
                                           command=self.start_browser, style="Primary.TButton")
        self.start_browser_btn.pack(side="left", padx=(0, 5))
        
        self.stop_browser_btn = ttk.Button(browser_btn_frame, text="⏹️ Stop Browser", 
                                          command=self.stop_browser, style="Danger.TButton", state="disabled")
        self.stop_browser_btn.pack(side="left")
        
        # Scraping Options
        scraping_frame = ttk.LabelFrame(left_frame, text="🔍 Scraping Options", padding="10")
        scraping_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        # CSS Selectors
        ttk.Label(scraping_frame, text="CSS Selectors (JSON):", style="Subtitle.TLabel").pack(anchor="w")
        self.selectors_text = scrolledtext.ScrolledText(scraping_frame, height=6, width=40)
        self.selectors_text.pack(fill="x", pady=(5, 0))
        self.selectors_text.insert("1.0", '{\n  "title": "h1",\n  "content": "p"\n}')
        
        # Output Settings
        output_frame = ttk.LabelFrame(left_frame, text="💾 Output Settings", padding="10")
        output_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        
        # Output format
        ttk.Label(output_frame, text="Format:").grid(row=0, column=0, sticky="w")
        self.output_format_var = tk.StringVar(value="json")
        format_combo = ttk.Combobox(output_frame, textvariable=self.output_format_var, 
                                   values=["json", "csv", "xml", "txt"], state="readonly", width=15)
        format_combo.grid(row=1, column=0, sticky="w", pady=(5, 10))
        
        # Filename
        ttk.Label(output_frame, text="Filename:").grid(row=2, column=0, sticky="w")
        self.filename_var = tk.StringVar(value="scraped_data")
        filename_entry = ttk.Entry(output_frame, textvariable=self.filename_var, width=30)
        filename_entry.grid(row=3, column=0, sticky="ew", pady=(5, 10))
        
        # Output directory
        dir_frame = ttk.Frame(output_frame)
        dir_frame.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Button(dir_frame, text="📁 Choose Output Dir", 
                  command=self.choose_output_dir).pack(side="left", padx=(0, 5))
        self.output_dir_var = tk.StringVar(value="output")
        ttk.Label(dir_frame, textvariable=self.output_dir_var, foreground="blue").pack(side="left")
        
        # Action Buttons
        action_frame = ttk.Frame(left_frame)
        action_frame.grid(row=4, column=0, sticky="ew", pady=(15, 0))
        
        self.scrape_btn = ttk.Button(action_frame, text="🔍 Start Scraping", 
                                    command=self.start_scraping, style="Primary.TButton", state="disabled")
        self.scrape_btn.pack(fill="x", pady=(0, 5))
        
        self.preview_btn = ttk.Button(action_frame, text="👁️ Preview Page", 
                                     command=self.preview_page, style="Secondary.TButton", state="disabled")
        self.preview_btn.pack(fill="x", pady=(0, 5))
        
        self.open_output_btn = ttk.Button(action_frame, text="📂 Open Output Folder", 
                                        command=self.open_output_folder, style="Secondary.TButton")
        self.open_output_btn.pack(fill="x")
        
    def create_right_panel(self, parent):
        """Create the right output panel"""
        right_frame = ttk.LabelFrame(parent, text="📊 Results & Browser Info", padding="10")
        right_frame.grid(row=1, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Browser info
        browser_info_frame = ttk.LabelFrame(right_frame, text="🌐 Browser Information", padding="10")
        browser_info_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.browser_status_label = ttk.Label(browser_info_frame, text="Browser: Not started", style="Status.TLabel")
        self.browser_status_label.pack(anchor="w")
        
        self.current_url_label = ttk.Label(browser_info_frame, text="URL: None", style="Status.TLabel")
        self.current_url_label.pack(anchor="w")
        
        # Results display
        results_frame = ttk.LabelFrame(right_frame, text="📋 Scraping Results", padding="10")
        results_frame.grid(row=1, column=0, sticky="nsew")
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, state="disabled")
        self.results_text.grid(row=0, column=0, sticky="nsew")
        
        # Results toolbar
        results_toolbar = ttk.Frame(results_frame)
        results_toolbar.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        
        ttk.Button(results_toolbar, text="📋 Copy Results", 
                  command=self.copy_results).pack(side="left", padx=(0, 5))
        ttk.Button(results_toolbar, text="🗑️ Clear Results", 
                  command=self.clear_results).pack(side="left", padx=(0, 5))
        ttk.Button(results_toolbar, text="💾 Save Results", 
                  command=self.save_results).pack(side="left")
        
    def create_bottom_panel(self, parent):
        """Create the bottom status and logs panel"""
        bottom_frame = ttk.LabelFrame(parent, text="📝 Logs & Status", padding="10")
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=1)
        
        # Status bar
        status_frame = ttk.Frame(bottom_frame)
        status_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Ready to start scraping...", style="Status.TLabel")
        self.status_label.pack(side="left")
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, mode="determinate")
        self.progress_bar.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        # Log display
        log_frame = ttk.Frame(bottom_frame)
        log_frame.grid(row=1, column=0, sticky="nsew")
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD, state="disabled")
        self.log_text.grid(row=0, column=0, sticky="nsew")
        
    def start_browser(self):
        """Start the browser"""
        if not SELENIUM_AVAILABLE:
            messagebox.showerror("Error", "Selenium not available. Please install: pip install selenium")
            return
        
        def start_browser_thread():
            try:
                self.update_status("Starting browser...")
                
                # Set up Chrome options
                options = Options()
                if self.headless_var.get():
                    options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1200,800')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                
                # Start browser
                self.driver = webdriver.Chrome(options=options)
                self.driver.implicitly_wait(10)
                
                self.window.after(0, self.browser_started)
                self.update_status("Browser started successfully")
                
            except Exception as e:
                self.window.after(0, lambda: self.browser_error(str(e)))
        
        threading.Thread(target=start_browser_thread, daemon=True).start()
    
    def browser_started(self):
        """Called when browser successfully starts"""
        self.start_browser_btn.config(state="disabled")
        self.stop_browser_btn.config(state="normal")
        self.scrape_btn.config(state="normal")
        self.preview_btn.config(state="normal")
        self.browser_status_label.config(text="Browser: Running", style="Success.TLabel")
        
        # Navigate to initial URL
        initial_url = self.url_var.get()
        if initial_url and initial_url != "https://example.com":
            self.navigate_to_url(initial_url)
    
    def browser_error(self, error_msg):
        """Handle browser startup error"""
        self.update_status(f"Browser error: {error_msg}", "error")
        messagebox.showerror("Browser Error", f"Failed to start browser:\n{error_msg}")
    
    def stop_browser(self):
        """Stop the browser"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
            
            self.start_browser_btn.config(state="normal")
            self.stop_browser_btn.config(state="disabled")
            self.scrape_btn.config(state="disabled")
            self.preview_btn.config(state="disabled")
            self.browser_status_label.config(text="Browser: Stopped", style="Error.TLabel")
            self.current_url_label.config(text="URL: None")
            self.update_status("Browser stopped")
            
        except Exception as e:
            self.update_status(f"Error stopping browser: {str(e)}", "error")
    
    def navigate_to_url(self, url):
        """Navigate to a URL"""
        if not self.driver:
            return
        
        try:
            self.update_status(f"Navigating to {url}...")
            self.driver.get(url)
            current_url = self.driver.current_url
            self.current_url_label.config(text=f"URL: {current_url}")
            self.update_status(f"Navigated to {current_url}")
            
        except Exception as e:
            self.update_status(f"Navigation error: {str(e)}", "error")
    
    def start_scraping(self):
        """Start the scraping process"""
        if not self.driver:
            messagebox.showerror("Error", "Browser not started")
            return
        
        url = self.url_var.get()
        if not url or url == "https://example.com":
            messagebox.showwarning("Warning", "Please enter a valid URL")
            return
        
        # Navigate to URL first
        self.navigate_to_url(url)
        
        # Start scraping in background
        def scrape_thread():
            try:
                self.update_status("Starting scraping...")
                self.progress_var.set(0)
                
                # Get selectors
                selectors_text = self.selectors_text.get("1.0", tk.END).strip()
                try:
                    selectors = json.loads(selectors_text)
                except json.JSONDecodeError:
                    messagebox.showerror("Error", "Invalid JSON in CSS selectors")
                    return
                
                # Simple scraping using browser
                data = {}
                for field_name, selector in selectors.items():
                    try:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        data[field_name] = element.text
                    except Exception as e:
                        data[field_name] = f"Error: {str(e)}"
                
                self.progress_var.set(100)
                self.window.after(0, lambda: self.handle_scraping_result(data))
                
            except Exception as e:
                self.window.after(0, lambda: self.handle_scraping_error(str(e)))
        
        threading.Thread(target=scrape_thread, daemon=True).start()
    
    def handle_scraping_result(self, result):
        """Handle successful scraping result"""
        self.update_status("Scraping completed successfully")
        
        # Display results
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)
        
        if isinstance(result, dict):
            result_text = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            result_text = str(result)
        
        self.results_text.insert("1.0", result_text)
        self.results_text.config(state="disabled")
        
        # Save results
        self.save_scraping_results(result)
    
    def handle_scraping_error(self, error_msg):
        """Handle scraping error"""
        self.update_status(f"Scraping failed: {error_msg}", "error")
        self.progress_var.set(0)
        
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", f"Error: {error_msg}")
        self.results_text.config(state="disabled")
    
    def save_scraping_results(self, data):
        """Save scraping results to file"""
        try:
            output_dir = self.output_dir_var.get()
            filename = self.filename_var.get()
            format_type = self.output_format_var.get()
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            full_filename = f"{filename}_{timestamp}.{format_type}"
            filepath = os.path.join(output_dir, full_filename)
            
            # Save data based on format
            if format_type == "json":
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            elif format_type == "txt":
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(data))
            else:
                # For CSV, XML - convert to JSON for now
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.update_status(f"Results saved to {filepath}")
            
        except Exception as e:
            self.update_status(f"Error saving results: {str(e)}", "error")
    
    def preview_page(self):
        """Preview the current page"""
        if not self.driver:
            messagebox.showerror("Error", "Browser not started")
            return
        
        try:
            self.update_status("Previewing page...")
            
            # Get page info
            page_info = {
                'url': self.driver.current_url,
                'title': self.driver.title,
                'links': len(self.driver.find_elements(By.CSS_SELECTOR, "a")),
                'images': len(self.driver.find_elements(By.CSS_SELECTOR, "img")),
                'tables': len(self.driver.find_elements(By.CSS_SELECTOR, "table")),
                'forms': len(self.driver.find_elements(By.CSS_SELECTOR, "form"))
            }
            
            # Display preview
            self.results_text.config(state="normal")
            self.results_text.delete("1.0", tk.END)
            
            preview_text = f"""Page Preview:
URL: {page_info['url']}
Title: {page_info['title']}
Elements found:
- Links: {page_info['links']}
- Images: {page_info['images']}
- Tables: {page_info['tables']}
- Forms: {page_info['forms']}

Available elements for scraping:
{json.dumps(page_info, indent=2)}
"""
            
            self.results_text.insert("1.0", preview_text)
            self.results_text.config(state="disabled")
            
            self.update_status("Preview completed")
            
        except Exception as e:
            self.update_status(f"Preview error: {str(e)}", "error")
    
    def choose_output_dir(self):
        """Choose output directory"""
        directory = filedialog.askdirectory(title="Choose Output Directory")
        if directory:
            self.output_dir_var.set(directory)
    
    def open_output_folder(self):
        """Open the output folder"""
        output_dir = self.output_dir_var.get()
        if os.path.exists(output_dir):
            webbrowser.open(f"file://{os.path.abspath(output_dir)}")
        else:
            messagebox.showwarning("Warning", "Output directory does not exist")
    
    def copy_results(self):
        """Copy results to clipboard"""
        try:
            results = self.results_text.get("1.0", tk.END)
            self.window.clipboard_clear()
            self.window.clipboard_append(results)
            self.update_status("Results copied to clipboard")
        except Exception as e:
            self.update_status(f"Error copying results: {str(e)}", "error")
    
    def clear_results(self):
        """Clear results display"""
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)
        self.results_text.config(state="disabled")
        self.update_status("Results cleared")
    
    def save_results(self):
        """Save current results to file"""
        try:
            results = self.results_text.get("1.0", tk.END)
            if not results.strip():
                messagebox.showwarning("Warning", "No results to save")
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(results)
                self.update_status(f"Results saved to {filename}")
                
        except Exception as e:
            self.update_status(f"Error saving results: {str(e)}", "error")
    
    def update_status(self, message, level="info"):
        """Update status message"""
        self.status_label.config(text=message)
        
        # Add to log
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, log_message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        
        # Color coding
        if level == "error":
            self.status_label.config(style="Error.TLabel")
        elif level == "warning":
            self.status_label.config(style="Warning.TLabel")
        else:
            self.status_label.config(style="Status.TLabel")
    
    def run(self):
        """Start the GUI application"""
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start GUI main loop
        self.window.mainloop()
    
    def on_closing(self):
        """Handle application closing"""
        try:
            if self.driver:
                self.driver.quit()
        except:
            pass
        self.window.destroy()


def main():
    """Main function to start the GUI"""
    print("🚀 Starting Standalone Browser Scraper GUI...")
    
    if not SELENIUM_AVAILABLE:
        print("⚠️ Selenium not available - install with: pip install selenium")
        print("The GUI will still work but browser automation will be disabled.")
    
    try:
        app = StandaloneScraperGUI()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start GUI: {e}")
        input("Press Enter to exit...")


if __name__ == '__main__':
    main() 