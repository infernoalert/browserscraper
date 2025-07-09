# Web Explorer - Text Extractor

A desktop application with an embedded browser that allows you to navigate websites, handle login forms, and extract text content automatically.

## Features

### 🚀 Core Functionality
- **Embedded Browser**: Full-featured web browser built into the application
- **Login Automation**: Automatically fill and submit login forms
- **Text Extraction**: Extract all text content from web pages
- **Batch Processing**: Save multiple pages of extracted text
- **Auto Mode**: Automated navigation between pages (configurable)

### 🎯 Key Components

#### Navigation Panel
- URL input field with auto-completion
- Back/Forward/Refresh buttons
- Real-time URL display

#### Login Handler
- Username and password input fields
- Automatic form detection and filling
- Support for various login form structures
- One-click login submission

#### Text Extraction
- Extract text from current page
- Preview extracted content
- Save to text or JSON format
- Clear extracted content

#### Auto Mode
- Enable/disable automatic navigation
- Configurable delay between pages
- Next/Skip page controls
- Progress tracking

## Installation

### Prerequisites
- Python 3.7 or higher
- Windows 10/11 (tested on Windows 10)

### Setup
1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python web_explorer.py
```

## Usage Guide

### Basic Navigation
1. Enter a URL in the address bar
2. Press Enter or click "Go"
3. Use Back/Forward buttons to navigate
4. Click "Refresh" to reload the page

### Login Automation
1. Navigate to a login page
2. Enter your username and password in the login panel
3. Click "Login" - the app will automatically:
   - Find username/email fields
   - Find password fields
   - Fill in your credentials
   - Submit the form

### Text Extraction
1. Navigate to a page you want to extract text from
2. Click "Extract Current Page Text"
3. View the extracted text in the preview panel
4. Click "Save All Extracted Text" to save to a file
5. Choose between .txt or .json format

### Auto Mode
1. Enable "Auto Mode" checkbox
2. Set delay between pages (in seconds)
3. Use "Next Page" to manually advance
4. Use "Skip Current Page" to skip without extracting

## File Formats

### Text File (.txt)
```
=== Page 1 ===
URL: https://example.com
Title: Example Page
Timestamp: 2024-01-01T12:00:00.000Z
--------------------------------------------------
[Extracted text content here]

==================================================

=== Page 2 ===
...
```

### JSON File (.json)
```json
[
  {
    "url": "https://example.com",
    "title": "Example Page",
    "text": "Extracted text content",
    "timestamp": "2024-01-01T12:00:00.000Z"
  }
]
```

## Technical Details

### Dependencies
- **PyQt5**: GUI framework
- **PyQtWebEngine**: Embedded web browser
- **requests**: HTTP requests
- **beautifulsoup4**: HTML parsing

### Architecture
- **Main Window**: WebExplorer class
- **Browser**: QWebEngineView with custom page handling
- **JavaScript Integration**: Custom login form detection
- **Text Processing**: Client-side text extraction

### Browser Features
- Full web compatibility
- JavaScript support
- Cookie handling
- Session management
- Modern web standards support

## Customization

### Adding Custom Navigation Logic
Modify the `go_to_next_page()` method in the WebExplorer class:

```python
def go_to_next_page(self):
    # Add your custom navigation logic here
    # Example: Click next button, follow links, etc.
    pass
```

### Custom Text Extraction
Modify the JavaScript in `extract_current_page()`:

```javascript
function extractText() {
    // Add custom text extraction logic
    // Example: Extract specific elements, filter content, etc.
}
```

### Login Form Detection
The app automatically detects common login form patterns:
- Username fields: `input[name="username"]`, `input[type="email"]`, etc.
- Password fields: `input[name="password"]`, `input[type="password"]`, etc.
- Submit buttons: `input[type="submit"]`, `button[type="submit"]`, etc.

## Troubleshooting

### Common Issues

1. **Browser not loading**
   - Check internet connection
   - Verify URL format (include https://)
   - Try refreshing the page

2. **Login not working**
   - Ensure username/password are correct
   - Check if the site uses custom login forms
   - Try manual login first

3. **Text extraction issues**
   - Some sites may block text extraction
   - Try different pages
   - Check browser console for errors

### Performance Tips
- Disable auto mode for large sites
- Clear extracted text periodically
- Use appropriate delay settings
- Close unnecessary browser tabs

## Security Notes

- Passwords are stored in memory only
- No credentials are saved to disk
- Use HTTPS sites when possible
- Be cautious with sensitive data

## Future Enhancements

- [ ] Multi-tab support
- [ ] Custom CSS selectors for extraction
- [ ] Proxy support
- [ ] Export to different formats
- [ ] Batch URL processing
- [ ] Advanced navigation patterns
- [ ] Screenshot capture
- [ ] Form automation beyond login

## License

This project is open source and available under the MIT License. 