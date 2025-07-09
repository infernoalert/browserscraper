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
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QFont, QIcon
import requests
from bs4 import BeautifulSoup

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
        
        # Initialize variables
        self.current_url = ""
        self.extracted_texts = []
        self.current_page_index = 0
        self.urls_to_visit = []
        self.is_auto_mode = False
        
        # Setup UI
        self.setup_ui()
        self.setup_web_engine()
        
        logger.info("Web Explorer application initialized successfully")
        
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
        
        self.next_button = QPushButton("Next Page")
        self.next_button.clicked.connect(self.go_to_next_page)
        
        self.skip_button = QPushButton("Skip Current Page")
        self.skip_button.clicked.connect(self.skip_current_page)
        
        auto_layout.addWidget(self.auto_mode_checkbox)
        auto_layout.addWidget(QLabel("Delay between pages:"))
        auto_layout.addWidget(self.delay_spinbox)
        auto_layout.addWidget(self.next_button)
        auto_layout.addWidget(self.skip_button)
        
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
            // Remove script and style elements
            const scripts = document.querySelectorAll('script, style, nav, header, footer, aside');
            scripts.forEach(el => el.remove());
            
            // Get all text content
            const textContent = document.body.innerText || document.body.textContent;
            
            // Clean up the text
            const cleanedText = textContent
                .replace(/\\s+/g, ' ')
                .replace(/\\n+/g, '\\n')
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
        # This is a placeholder for automatic navigation
        # You can implement your own logic here
        QMessageBox.information(self, "Next Page", "Next page functionality - implement your navigation logic here")
        
    def skip_current_page(self):
        if self.extracted_texts:
            self.extracted_texts.pop()  # Remove the last extracted text
            self.update_extracted_text_display()
            self.status_label.setText("Current page skipped")
            logger.info("Current page skipped")
        else:
            self.status_label.setText("No page to skip")

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