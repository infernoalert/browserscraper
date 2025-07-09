import sys
import os
import json
import logging
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLineEdit, QPushButton, QTextEdit, QLabel, 
                             QFileDialog, QMessageBox, QProgressBar, QGroupBox,
                             QGridLayout, QCheckBox, QSpinBox, QComboBox)
from PyQt5.QtCore import QUrl, QTimer, pyqtSignal, QThread, Qt
try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False
    print("Error: PyQtWebEngine is not installed. Please install it with: pip install PyQtWebEngine")
from PyQt5.QtGui import QFont, QIcon
import requests
from bs4 import BeautifulSoup

# Import advanced navigation module
try:
    from advanced_navigation import AdvancedNavigator, URLManager, NavigationConfig
    ADVANCED_NAVIGATION_AVAILABLE = True
except ImportError:
    ADVANCED_NAVIGATION_AVAILABLE = False
    print("Warning: advanced_navigation module not available")

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('web_explorer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WebExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Initializing Web Explorer application")
        self.setWindowTitle("Web Explorer - Text Extractor")
        self.setGeometry(100, 100, 1400, 900)
        
        # Load configuration
        self.config = self.load_config()
        
        # Initialize variables
        self.current_url = ""
        self.extracted_texts = []
        self.current_page_index = 0
        self.urls_to_visit = []
        self.is_auto_mode = False
        
        # Auto loop variables
        self.auto_loop_running = False
        self.auto_loop_iterations = 0
        self.auto_loop_current_iteration = 0
        self.auto_loop_timer = QTimer()
        self.auto_loop_timer.timeout.connect(self.auto_loop_step)
        
        # Initialize advanced navigation if available
        if ADVANCED_NAVIGATION_AVAILABLE:
            self.url_manager = URLManager()
            self.nav_config = NavigationConfig()
        
        # Setup UI
        self.setup_ui()
        self.setup_web_engine()
        
        logger.info("Web Explorer application initialized successfully")
        
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info("Configuration loaded successfully")
            return config
        except FileNotFoundError:
            logger.warning("config.json not found, using default configuration")
            return self.get_default_config()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing config.json: {e}")
            return self.get_default_config()
            
    def get_default_config(self):
        """Return default configuration if config.json is missing"""
        return {
            "browser": {
                "default_url": "https://www.google.com",
                "enable_javascript": True,
                "timeout": 30000
            },
            "extraction": {
                "remove_scripts": True,
                "remove_styles": True,
                "min_text_length": 10
            },
            "auto_mode": {
                "enabled": False,
                "delay_between_pages": 3,
                "max_pages_per_session": 100
            },
            "output": {
                "default_format": "txt",
                "include_metadata": True
            }
        }

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create browser view early so it can be referenced by buttons
        self.web_view = QWebEngineView()
        self.web_view.setMinimumHeight(500)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel for controls
        left_panel = QWidget()
        left_panel.setMaximumWidth(400)
        left_layout = QVBoxLayout(left_panel)
        
        # URL input section
        url_group = QGroupBox("Navigation")
        url_layout = QVBoxLayout(url_group)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL (e.g., https://example.com)")
        self.url_input.returnPressed.connect(self.navigate_to_url)
        
        nav_buttons_layout = QHBoxLayout()
        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.navigate_to_url)
        self.back_button = QPushButton("← Back")
        self.back_button.clicked.connect(self.web_view.back)
        self.forward_button = QPushButton("Forward →")
        self.forward_button.clicked.connect(self.web_view.forward)
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.web_view.reload)
        
        nav_buttons_layout.addWidget(self.back_button)
        nav_buttons_layout.addWidget(self.forward_button)
        nav_buttons_layout.addWidget(self.refresh_button)
        nav_buttons_layout.addWidget(self.go_button)
        
        url_layout.addWidget(self.url_input)
        url_layout.addLayout(nav_buttons_layout)
        
        # Text extraction section
        extract_group = QGroupBox("Text Extraction")
        extract_layout = QVBoxLayout(extract_group)
        
        self.extract_button = QPushButton("Extract Current Page Text")
        self.extract_button.clicked.connect(self.extract_current_page)
        
        # Add debug button
        self.debug_button = QPushButton("Debug Page")
        self.debug_button.clicked.connect(self.debug_current_page)
        
        self.save_button = QPushButton("Save All Extracted Text")
        self.save_button.clicked.connect(self.save_extracted_text)
        
        self.clear_button = QPushButton("Clear Extracted Text")
        self.clear_button.clicked.connect(self.clear_extracted_text)
        
        extract_layout.addWidget(self.extract_button)
        extract_layout.addWidget(self.debug_button)
        extract_layout.addWidget(self.save_button)
        extract_layout.addWidget(self.clear_button)
        
        # Auto mode section
        auto_group = QGroupBox("Auto Navigation")
        auto_layout = QVBoxLayout(auto_group)
        
        self.auto_mode_checkbox = QCheckBox("Enable Auto Mode")
        self.auto_mode_checkbox.toggled.connect(self.toggle_auto_mode)
        
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setRange(1, 60)
        self.delay_spinbox.setValue(3)
        self.delay_spinbox.setSuffix(" seconds")
        
        # Add input for button text to click
        self.next_button_text_input = QLineEdit()
        self.next_button_text_input.setPlaceholderText("Button Text to Click (e.g., Skip for now)")
        
        self.next_button = QPushButton("Next Page")
        self.next_button.clicked.connect(self.go_to_next_page)
        
        self.skip_button = QPushButton("Skip Current Page")
        self.skip_button.clicked.connect(self.skip_current_page)
        
        auto_layout.addWidget(self.auto_mode_checkbox)
        auto_layout.addWidget(QLabel("Delay between pages:"))
        auto_layout.addWidget(self.delay_spinbox)
        auto_layout.addWidget(QLabel("Button Text to Click:"))
        auto_layout.addWidget(self.next_button_text_input)
        auto_layout.addWidget(self.next_button)
        auto_layout.addWidget(self.skip_button)
        
        # New Auto Loop section
        auto_loop_group = QGroupBox("Auto Loop")
        auto_loop_layout = QVBoxLayout(auto_loop_group)
        
        # Number of iterations input
        iterations_layout = QHBoxLayout()
        iterations_layout.addWidget(QLabel("Number of iterations:"))
        self.iterations_spinbox = QSpinBox()
        self.iterations_spinbox.setRange(1, 100)
        self.iterations_spinbox.setValue(10)
        iterations_layout.addWidget(self.iterations_spinbox)
        
        # Auto button
        self.auto_button = QPushButton("Start Auto Loop")
        self.auto_button.clicked.connect(self.start_auto_loop)
        
        # Progress display
        self.auto_progress_label = QLabel("Ready for auto loop")
        self.auto_progress_bar = QProgressBar()
        self.auto_progress_bar.setVisible(False)
        
        auto_loop_layout.addLayout(iterations_layout)
        auto_loop_layout.addWidget(self.auto_button)
        auto_loop_layout.addWidget(self.auto_progress_label)
        auto_loop_layout.addWidget(self.auto_progress_bar)
        
        # Status section
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("Ready")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        # Add debug log display
        self.debug_log = QTextEdit()
        self.debug_log.setMaximumHeight(150)
        self.debug_log.setPlaceholderText("Debug information will appear here...")
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar)
        status_layout.addWidget(QLabel("Debug Log:"))
        status_layout.addWidget(self.debug_log)
        
        # Add all groups to left panel
        left_layout.addWidget(url_group)
        left_layout.addWidget(extract_group)
        left_layout.addWidget(auto_group)
        left_layout.addWidget(auto_loop_group)
        left_layout.addWidget(status_group)
        left_layout.addStretch()
        
        # Right panel for browser and extracted text
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Browser view
        self.web_view.setMinimumHeight(500)
        
        # Extracted text display
        self.extracted_text_display = QTextEdit()
        self.extracted_text_display.setMaximumHeight(200)
        self.extracted_text_display.setPlaceholderText("Extracted text will appear here...")
        
        right_layout.addWidget(QLabel("Browser:"))
        right_layout.addWidget(self.web_view)
        right_layout.addWidget(QLabel("Extracted Text:"))
        right_layout.addWidget(self.extracted_text_display)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        
    def setup_web_engine(self):
        logger.info("Setting up web engine")
        # Create a custom web page to handle JavaScript execution
        self.web_page = CustomWebPage()
        self.web_view.setPage(self.web_page)
        
        # Connect signals
        self.web_view.urlChanged.connect(self.on_url_changed)
        self.web_view.loadFinished.connect(self.on_load_finished)
        
        # Inject polyfills immediately
        self.inject_polyfills()
        
        # Load initial page
        self.web_view.load(QUrl("https://www.google.com"))
        logger.info("Web engine setup complete")
        
    def inject_polyfills(self):
        """Inject JavaScript polyfills for compatibility"""
        polyfill_js = """
        // Comprehensive polyfill for structuredClone
        if (typeof structuredClone === 'undefined') {
            window.structuredClone = function(obj) {
                try {
                    // Handle null and undefined
                    if (obj === null || obj === undefined) {
                        return obj;
                    }
                    
                    // Handle primitives
                    if (typeof obj !== 'object') {
                        return obj;
                    }
                    
                    // Handle Date objects
                    if (obj instanceof Date) {
                        return new Date(obj.getTime());
                    }
                    
                    // Handle Array objects
                    if (Array.isArray(obj)) {
                        return obj.map(item => window.structuredClone(item));
                    }
                    
                    // Handle regular objects
                    if (obj.constructor === Object) {
                        const cloned = {};
                        for (const key in obj) {
                            if (obj.hasOwnProperty(key)) {
                                cloned[key] = window.structuredClone(obj[key]);
                            }
                        }
                        return cloned;
                    }
                    
                    // Fallback to JSON for other objects
                    return JSON.parse(JSON.stringify(obj));
                } catch (e) {
                    console.warn('structuredClone polyfill failed:', e);
                    // Return original object if cloning fails
                    return obj;
                }
            };
            console.log('structuredClone polyfill injected successfully');
        }
        
        // Also inject into global scope
        if (typeof globalThis !== 'undefined' && typeof globalThis.structuredClone === 'undefined') {
            globalThis.structuredClone = window.structuredClone;
        }
        
        // Override any existing structuredClone to use our polyfill
        if (typeof window.structuredClone === 'function') {
            const originalStructuredClone = window.structuredClone;
            window.structuredClone = function(obj) {
                try {
                    return originalStructuredClone(obj);
                } catch (e) {
                    console.warn('Original structuredClone failed, using polyfill:', e);
                    // Use our polyfill as fallback
                    return window.structuredClone(obj);
                }
            };
        }
        """
        self.web_page.runJavaScript(polyfill_js)
        
    def navigate_to_url(self):
        url = self.url_input.text().strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        logger.info(f"Navigating to URL: {url}")
        
        # Inject polyfills before loading new page
        self.inject_polyfills()
        self.web_view.load(QUrl(url))
        
    def on_url_changed(self, url):
        self.current_url = url.toString()
        self.url_input.setText(self.current_url)
        self.status_label.setText(f"Current URL: {self.current_url}")
        logger.info(f"URL changed to: {self.current_url}")
        
        # Inject polyfills when URL changes
        self.inject_polyfills()
        
    def on_load_finished(self, success):
        if success:
            self.status_label.setText("Page loaded successfully")
            logger.info("Page loaded successfully")
            # Inject polyfills after page loads
            self.inject_polyfills()
        else:
            self.status_label.setText("Failed to load page")
            logger.error("Failed to load page")
            
    def debug_current_page(self):
        """Debug the current page to see what forms and elements are available"""
        logger.info("Starting page debug")
        
        js_code = """
        function debugPage() {
            const result = {
                url: window.location.href,
                title: document.title,
                forms: [],
                inputs: [],
                buttons: [],
                links: []
            };
            
            // Find all forms
            const forms = document.querySelectorAll('form');
            forms.forEach((form, index) => {
                result.forms.push({
                    index: index,
                    action: form.action,
                    method: form.method,
                    id: form.id,
                    className: form.className
                });
            });
            
            // Find all input fields
            const inputs = document.querySelectorAll('input');
            inputs.forEach((input, index) => {
                result.inputs.push({
                    index: index,
                    type: input.type,
                    name: input.name,
                    id: input.id,
                    className: input.className,
                    placeholder: input.placeholder
                });
            });
            
            // Find all buttons
            const buttons = document.querySelectorAll('button');
            buttons.forEach((button, index) => {
                result.buttons.push({
                    index: index,
                    type: button.type,
                    text: button.textContent,
                    id: button.id,
                    className: button.className
                });
            });
            
            // Find all links
            const links = document.querySelectorAll('a');
            links.forEach((link, index) => {
                if (link.href && link.href.startsWith('http')) {
                    result.links.push({
                        index: index,
                        href: link.href,
                        text: link.textContent,
                        id: link.id,
                        className: link.className
                    });
                }
            });
            
            return result;
        }
        debugPage();
        """
        
        self.web_page.runJavaScript(js_code, self.on_debug_result)
        
    def on_debug_result(self, result):
        """Handle debug results"""
        if result:
            debug_info = f"=== Page Debug Info ===\n"
            debug_info += f"URL: {result.get('url', 'N/A')}\n"
            debug_info += f"Title: {result.get('title', 'N/A')}\n"
            debug_info += f"Forms found: {len(result.get('forms', []))}\n"
            debug_info += f"Inputs found: {len(result.get('inputs', []))}\n"
            debug_info += f"Buttons found: {len(result.get('buttons', []))}\n"
            debug_info += f"Links found: {len(result.get('links', []))}\n\n"
            
            # Show forms
            if result.get('forms'):
                debug_info += "Forms:\n"
                for form in result['forms']:
                    debug_info += f"  - Form {form['index']}: action={form['action']}, method={form['method']}\n"
            
            # Show inputs
            if result.get('inputs'):
                debug_info += "\nInputs:\n"
                for input_field in result['inputs']:
                    debug_info += f"  - Input {input_field['index']}: type={input_field['type']}, name={input_field['name']}, id={input_field['id']}\n"
            
            # Show buttons
            if result.get('buttons'):
                debug_info += "\nButtons:\n"
                for button in result['buttons']:
                    debug_info += f"  - Button {button['index']}: type={button['type']}, text='{button['text']}', id={button['id']}\n"
            
            # Show links
            if result.get('links'):
                debug_info += "\nLinks:\n"
                for link in result['links'][:10]:  # Show first 10 links
                    debug_info += f"  - Link {link['index']}: {link['text']} -> {link['href']}\n"
            
            self.debug_log.setText(debug_info)
            logger.info(f"Debug completed: {len(result.get('forms', []))} forms, {len(result.get('inputs', []))} inputs, {len(result.get('buttons', []))} buttons, {len(result.get('links', []))} links")
        else:
            self.debug_log.setText("Debug failed - no result received")
            logger.error("Debug failed - no result received")
            
    def extract_current_page(self):
        js_code = """
        function extractText() {
            // Do NOT remove any elements!
            const textContent = document.body.innerText || document.body.textContent;
            const cleanedText = textContent
                .replace(/\s+/g, ' ')
                .replace(/\n+/g, '\n')
                .trim();
            return {
                url: window.location.href,
                title: document.title,
                text: cleanedText,
                timestamp: new Date().toISOString()
            };
        }
        extractText();
        """
        self.web_page.runJavaScript(js_code, self.on_text_extracted)
        
    def on_text_extracted(self, result):
        if result:
            self.extracted_texts.append(result)
            self.update_extracted_text_display()
            self.status_label.setText(f"Text extracted from: {result['title']}")
            logger.info(f"Text extracted from: {result['title']} ({len(result['text'])} characters)")
            
    def update_extracted_text_display(self):
        display_text = ""
        for i, text_data in enumerate(self.extracted_texts, 1):
            display_text += f"=== Page {i} ===\n"
            display_text += f"URL: {text_data['url']}\n"
            display_text += f"Title: {text_data['title']}\n"
            display_text += f"Timestamp: {text_data['timestamp']}\n"
            display_text += f"Text Length: {len(text_data['text'])} characters\n"
            display_text += "-" * 50 + "\n"
            display_text += text_data['text'][:500] + "..." if len(text_data['text']) > 500 else text_data['text']
            display_text += "\n\n"
            
        self.extracted_text_display.setText(display_text)
        
    def save_extracted_text(self):
        if not self.extracted_texts:
            QMessageBox.warning(self, "Warning", "No text to save")
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Extracted Text", 
            f"extracted_text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text Files (*.txt);;JSON Files (*.json)"
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(self.extracted_texts, f, indent=2, ensure_ascii=False)
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        for i, text_data in enumerate(self.extracted_texts, 1):
                            f.write(f"=== Page {i} ===\n")
                            f.write(f"URL: {text_data['url']}\n")
                            f.write(f"Title: {text_data['title']}\n")
                            f.write(f"Timestamp: {text_data['timestamp']}\n")
                            f.write("-" * 50 + "\n")
                            f.write(text_data['text'])
                            f.write("\n\n" + "=" * 80 + "\n\n")
                            
                QMessageBox.information(self, "Success", f"Text saved to {filename}")
                logger.info(f"Text saved to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
                logger.error(f"Failed to save file: {str(e)}")
                
    def clear_extracted_text(self):
        self.extracted_texts = []
        self.extracted_text_display.clear()
        self.status_label.setText("Extracted text cleared")
        logger.info("Extracted text cleared")
        
    def toggle_auto_mode(self, enabled):
        self.is_auto_mode = enabled
        if enabled:
            self.status_label.setText("Auto mode enabled")
            logger.info("Auto mode enabled")
        else:
            self.status_label.setText("Auto mode disabled")
            logger.info("Auto mode disabled")
            
    def go_to_next_page(self):
        # Get the button text from the input
        button_text = self.next_button_text_input.text().strip()
        if not button_text:
            QMessageBox.warning(self, "Input Required", "Please enter the button text to click for the next page.")
            return
        # JavaScript to click the button with exact (case-insensitive) text match
        js_code = f'''
        (function() {{
            var targetText = "{button_text}".toLowerCase();
            var buttons = document.querySelectorAll('button, input[type="button"], input[type="submit"]');
            for (var i = 0; i < buttons.length; i++) {{
                var btn = buttons[i];
                var btnText = (btn.innerText || btn.value || '').trim().toLowerCase();
                if (btnText === targetText) {{
                    btn.click();
                    return true;
                }}
            }}
            return false;
        }})();
        '''
        self.web_view.page().runJavaScript(js_code, self._on_next_page_js_result)
    
    def _on_next_page_js_result(self, result):
        if result:
            self.status_label.setText("Next page button clicked.")
            logger.info("Next page button clicked.")
        else:
            self.status_label.setText("Button with specified text not found.")
            logger.warning("Button with specified text not found.")
            
    def skip_current_page(self):
        if self.extracted_texts:
            self.extracted_texts.pop()  # Remove the last extracted text
            self.update_extracted_text_display()
            self.status_label.setText("Current page skipped")
            logger.info("Current page skipped")
        else:
            self.status_label.setText("No page to skip")
    
    def start_auto_loop(self):
        """Start the auto loop process"""
        if self.auto_loop_running:
            QMessageBox.warning(self, "Warning", "Auto loop is already running!")
            return
        
        # Get number of iterations
        self.auto_loop_iterations = self.iterations_spinbox.value()
        self.auto_loop_current_iteration = 0
        
        if self.auto_loop_iterations < 1:
            QMessageBox.warning(self, "Warning", "Please set a valid number of iterations (1-100)")
            return
        
        # Start the auto loop
        self.auto_loop_running = True
        self.auto_button.setText("Stop Auto Loop")
        self.auto_button.clicked.disconnect()
        self.auto_button.clicked.connect(self.stop_auto_loop)
        
        # Setup progress bar
        self.auto_progress_bar.setVisible(True)
        self.auto_progress_bar.setMaximum(self.auto_loop_iterations)
        self.auto_progress_bar.setValue(0)
        
        # Start the first iteration
        self.auto_progress_label.setText(f"Starting auto loop ({self.auto_loop_iterations} iterations)")
        logger.info(f"Starting auto loop with {self.auto_loop_iterations} iterations")
        
        # Start the first step immediately
        self.auto_loop_step()
    
    def stop_auto_loop(self):
        """Stop the auto loop process"""
        self.auto_loop_running = False
        self.auto_loop_timer.stop()
        
        # Reset button
        self.auto_button.setText("Start Auto Loop")
        self.auto_button.clicked.disconnect()
        self.auto_button.clicked.connect(self.start_auto_loop)
        
        # Hide progress bar
        self.auto_progress_bar.setVisible(False)
        self.auto_progress_label.setText("Auto loop stopped")
        
        logger.info("Auto loop stopped by user")
    
    def auto_loop_step(self):
        """Execute one step of the auto loop"""
        if not self.auto_loop_running:
            return
        
        self.auto_loop_current_iteration += 1
        self.auto_progress_label.setText(f"Step {self.auto_loop_current_iteration}/{self.auto_loop_iterations}")
        self.auto_progress_bar.setValue(self.auto_loop_current_iteration)
        
        logger.info(f"Auto loop step {self.auto_loop_current_iteration}/{self.auto_loop_iterations}")
        
        # Step 1: Extract current page text
        self.status_label.setText(f"Step {self.auto_loop_current_iteration}: Extracting text...")
        self.extract_current_page()
        
        # Wait for extraction to complete, then continue
        # We'll use a timer to wait for the extraction to finish
        QTimer.singleShot(2000, self.auto_loop_step_2)
    
    def auto_loop_step_2(self):
        """Step 2: Save extracted text"""
        if not self.auto_loop_running:
            return
        
        self.status_label.setText(f"Step {self.auto_loop_current_iteration}: Saving text...")
        
        # Save the extracted text to a file
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"auto_extracted_text_{timestamp}_iteration_{self.auto_loop_current_iteration}.txt"
            
            if self.extracted_texts:
                with open(filename, 'w', encoding='utf-8') as f:
                    for i, text_data in enumerate(self.extracted_texts, 1):
                        f.write(f"=== Page {i} ===\n")
                        f.write(f"URL: {text_data['url']}\n")
                        f.write(f"Title: {text_data['title']}\n")
                        f.write(f"Timestamp: {text_data['timestamp']}\n")
                        f.write(f"Auto Loop Iteration: {self.auto_loop_current_iteration}\n")
                        f.write("-" * 50 + "\n")
                        f.write(text_data['text'])
                        f.write("\n\n" + "=" * 80 + "\n\n")
                
                logger.info(f"Text saved to {filename}")
                self.debug_log.setText(self.debug_log.toPlainText() + f"\nSaved: {filename}")
            else:
                logger.warning("No text to save in auto loop step 2")
                self.debug_log.setText(self.debug_log.toPlainText() + "\nWarning: No text to save")
        
        except Exception as e:
            logger.error(f"Failed to save file in auto loop: {str(e)}")
            self.debug_log.setText(self.debug_log.toPlainText() + f"\nError saving file: {str(e)}")
        
        # Wait a bit, then go to step 3
        QTimer.singleShot(1000, self.auto_loop_step_3)
    
    def auto_loop_step_3(self):
        """Step 3: Go to next page"""
        if not self.auto_loop_running:
            return
        
        self.status_label.setText(f"Step {self.auto_loop_current_iteration}: Navigating to next page...")
        
        # Check if we've completed all iterations
        if self.auto_loop_current_iteration >= self.auto_loop_iterations:
            self.auto_loop_complete()
            return
        
        # Get the button text to click for next page
        button_text = self.next_button_text_input.text().strip()
        if not button_text:
            self.debug_log.setText(self.debug_log.toPlainText() + "\nWarning: No button text specified for next page")
            self.auto_loop_complete()
            return
        
        # Click the next page button
        js_code = f'''
        (function() {{
            var targetText = "{button_text}".toLowerCase();
            var buttons = document.querySelectorAll('button, input[type="button"], input[type="submit"], a');
            for (var i = 0; i < buttons.length; i++) {{
                var btn = buttons[i];
                var btnText = (btn.innerText || btn.value || btn.textContent || '').trim().toLowerCase();
                if (btnText === targetText) {{
                    btn.click();
                    return true;
                }}
            }}
            return false;
        }})();
        '''
        
        self.web_view.page().runJavaScript(js_code, self._on_auto_next_page_result)
    
    def _on_auto_next_page_result(self, result):
        """Handle the result of clicking the next page button in auto loop"""
        if result:
            logger.info(f"Auto loop: Next page button clicked for iteration {self.auto_loop_current_iteration}")
            self.debug_log.setText(self.debug_log.toPlainText() + "\nAuto loop: Next page button clicked")
            
            # Wait for the page to load, then start the next iteration
            delay = self.delay_spinbox.value() * 1000  # Convert to milliseconds
            QTimer.singleShot(delay, self.auto_loop_step)
        else:
            logger.warning(f"Auto loop: Button with specified text not found for iteration {self.auto_loop_current_iteration}")
            self.debug_log.setText(self.debug_log.toPlainText() + "\nAuto loop: Button not found, stopping")
            self.auto_loop_complete()
    
    def auto_loop_complete(self):
        """Handle completion of the auto loop"""
        self.auto_loop_running = False
        self.auto_loop_timer.stop()
        
        # Reset button
        self.auto_button.setText("Start Auto Loop")
        self.auto_button.clicked.disconnect()
        self.auto_button.clicked.connect(self.start_auto_loop)
        
        # Hide progress bar
        self.auto_progress_bar.setVisible(False)
        
        # Show completion message
        if self.auto_loop_current_iteration >= self.auto_loop_iterations:
            self.auto_progress_label.setText(f"Auto loop completed! ({self.auto_loop_iterations} iterations)")
            self.status_label.setText("Auto loop completed successfully")
            QMessageBox.information(self, "Auto Loop Complete", 
                                  f"Auto loop completed successfully!\n"
                                  f"Processed {self.auto_loop_iterations} iterations.\n"
                                  f"Check the current directory for saved files.")
        else:
            self.auto_progress_label.setText("Auto loop stopped early")
            self.status_label.setText("Auto loop stopped")
        
        logger.info(f"Auto loop completed after {self.auto_loop_current_iteration} iterations")

class CustomWebPage(QWebEnginePage):
    def __init__(self):
        super().__init__()
        
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        # Log JavaScript console messages
        logger.debug(f"JS Console [{level}] {message} (line {lineNumber}, source: {sourceID})")

def main():
    logger.info("Starting Web Explorer application")
    app = QApplication(sys.argv)
    app.setApplicationName("Web Explorer")
    
    # Set application style
    app.setStyle('Fusion')
    
    window = WebExplorer()
    window.show()
    
    logger.info("Web Explorer application started successfully")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 