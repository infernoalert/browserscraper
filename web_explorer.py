import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLineEdit, QPushButton, QTextEdit, QLabel, 
                             QFileDialog, QMessageBox, QProgressBar, QGroupBox,
                             QGridLayout, QCheckBox, QSpinBox, QComboBox)
from PyQt5.QtCore import QUrl, QTimer, pyqtSignal, QThread, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebEngineCore import QWebEngineProfile
from PyQt5.QtGui import QFont, QIcon
import requests
from bs4 import BeautifulSoup

class WebExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
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
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
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
        
        # Login section
        login_group = QGroupBox("Login Information")
        login_layout = QGridLayout(login_group)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.perform_login)
        
        login_layout.addWidget(QLabel("Username:"), 0, 0)
        login_layout.addWidget(self.username_input, 0, 1)
        login_layout.addWidget(QLabel("Password:"), 1, 0)
        login_layout.addWidget(self.password_input, 1, 1)
        login_layout.addWidget(self.login_button, 2, 0, 1, 2)
        
        # Text extraction section
        extract_group = QGroupBox("Text Extraction")
        extract_layout = QVBoxLayout(extract_group)
        
        self.extract_button = QPushButton("Extract Current Page Text")
        self.extract_button.clicked.connect(self.extract_current_page)
        
        self.save_button = QPushButton("Save All Extracted Text")
        self.save_button.clicked.connect(self.save_extracted_text)
        
        self.clear_button = QPushButton("Clear Extracted Text")
        self.clear_button.clicked.connect(self.clear_extracted_text)
        
        extract_layout.addWidget(self.extract_button)
        extract_layout.addWidget(self.save_button)
        extract_layout.addWidget(self.clear_button)
        
        # Auto mode section
        auto_group = QGroupBox("Auto Mode")
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
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar)
        
        # Add all groups to left panel
        left_layout.addWidget(url_group)
        left_layout.addWidget(login_group)
        left_layout.addWidget(extract_group)
        left_layout.addWidget(auto_group)
        left_layout.addWidget(status_group)
        left_layout.addStretch()
        
        # Right panel for browser and extracted text
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Browser view
        self.web_view = QWebEngineView()
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
        # Create a custom web page to handle JavaScript execution
        self.web_page = CustomWebPage()
        self.web_view.setPage(self.web_page)
        
        # Connect signals
        self.web_view.urlChanged.connect(self.on_url_changed)
        self.web_view.loadFinished.connect(self.on_load_finished)
        
        # Load initial page
        self.web_view.load(QUrl("https://www.google.com"))
        
    def navigate_to_url(self):
        url = self.url_input.text().strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        self.web_view.load(QUrl(url))
        
    def on_url_changed(self, url):
        self.current_url = url.toString()
        self.url_input.setText(self.current_url)
        self.status_label.setText(f"Current URL: {self.current_url}")
        
    def on_load_finished(self, success):
        if success:
            self.status_label.setText("Page loaded successfully")
        else:
            self.status_label.setText("Failed to load page")
            
    def perform_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Warning", "Please enter both username and password")
            return
            
        # JavaScript to find and fill login forms
        js_code = f"""
        function findAndFillLoginForm() {{
            // Find username/email fields
            const usernameSelectors = [
                'input[name="username"]',
                'input[name="email"]',
                'input[name="user"]',
                'input[name="login"]',
                'input[type="email"]',
                'input[id*="username"]',
                'input[id*="email"]',
                'input[id*="user"]',
                'input[id*="login"]'
            ];
            
            // Find password fields
            const passwordSelectors = [
                'input[name="password"]',
                'input[name="pass"]',
                'input[name="pwd"]',
                'input[type="password"]',
                'input[id*="password"]',
                'input[id*="pass"]',
                'input[id*="pwd"]'
            ];
            
            let usernameField = null;
            let passwordField = null;
            
            // Find username field
            for (let selector of usernameSelectors) {{
                usernameField = document.querySelector(selector);
                if (usernameField) break;
            }}
            
            // Find password field
            for (let selector of passwordSelectors) {{
                passwordField = document.querySelector(selector);
                if (passwordField) break;
            }}
            
            if (usernameField && passwordField) {{
                usernameField.value = '{username}';
                passwordField.value = '{password}';
                
                // Trigger change events
                usernameField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                passwordField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                
                // Try to find and click submit button
                const submitSelectors = [
                    'input[type="submit"]',
                    'button[type="submit"]',
                    'button:contains("Login")',
                    'button:contains("Sign In")',
                    'button:contains("Log In")',
                    'input[value*="Login"]',
                    'input[value*="Sign In"]',
                    'input[value*="Log In"]'
                ];
                
                for (let selector of submitSelectors) {{
                    const submitBtn = document.querySelector(selector);
                    if (submitBtn) {{
                        submitBtn.click();
                        return true;
                    }}
                }}
                
                // If no submit button found, try form submit
                const form = usernameField.closest('form') || passwordField.closest('form');
                if (form) {{
                    form.submit();
                    return true;
                }}
            }}
            
            return false;
        }}
        
        findAndFillLoginForm();
        """
        
        self.web_page.runJavaScript(js_code)
        QMessageBox.information(self, "Login", "Login attempt completed. Check if the form was filled and submitted.")
        
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
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
                
    def clear_extracted_text(self):
        self.extracted_texts = []
        self.extracted_text_display.clear()
        self.status_label.setText("Extracted text cleared")
        
    def toggle_auto_mode(self, enabled):
        self.is_auto_mode = enabled
        if enabled:
            self.status_label.setText("Auto mode enabled")
        else:
            self.status_label.setText("Auto mode disabled")
            
    def go_to_next_page(self):
        # This is a placeholder for automatic navigation
        # You can implement your own logic here
        QMessageBox.information(self, "Next Page", "Next page functionality - implement your navigation logic here")
        
    def skip_current_page(self):
        if self.extracted_texts:
            self.extracted_texts.pop()  # Remove the last extracted text
            self.update_extracted_text_display()
            self.status_label.setText("Current page skipped")
        else:
            self.status_label.setText("No page to skip")

class CustomWebPage(QWebEnginePage):
    def __init__(self):
        super().__init__()
        
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        # Optional: Handle JavaScript console messages
        pass

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Web Explorer")
    
    # Set application style
    app.setStyle('Fusion')
    
    window = WebExplorer()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 