# Web Explorer - Text Extractor

A desktop application with an embedded browser that allows you to navigate websites manually and extract text content automatically.

## Features

### 🚀 Core Functionality
- **Embedded Browser**: Full-featured web browser built into the application
- **Manual Navigation**: Browse websites naturally with full browser capabilities
- **Text Extraction**: Extract all text content from web pages
- **Batch Processing**: Save multiple pages of extracted text
- **Auto Navigation**: Automated navigation between pages (configurable)
- **Auto Loop**: Automated extraction and navigation for multiple iterations (1-100)
- **Debug Tools**: Analyze page structure for better understanding

### 🎯 Key Components

#### Navigation Panel
- URL input field with auto-completion
- Back/Forward/Refresh buttons
- Real-time URL display

#### Text Extraction
- Extract text from current page
- Preview extracted content
- Save to text or JSON format
- Clear extracted content
- Debug page structure

#### Auto Navigation
- Enable/disable automatic navigation
- Configurable delay between pages
- Next/Skip page controls
- Progress tracking

#### Auto Loop
- Set number of iterations (1-100)
- Automatic text extraction and saving
- Automatic navigation to next page
- Progress bar and status tracking
- Stop/start controls

#### Debug Tools
- Analyze page forms, inputs, buttons, and links
- Understand page structure for navigation
- Help with custom automation logic

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

Or use the batch file on Windows:
```bash
run_app.bat
```

## Usage Guide

### Basic Navigation
1. Enter a URL in the address bar
2. Press Enter or click "Go"
3. Use Back/Forward buttons to navigate
4. Click "Refresh" to reload the page
5. **Manual Login**: Log in to websites naturally using the browser interface

### Text Extraction
1. Navigate to a page you want to extract text from
2. Click "Extract Current Page Text"
3. View the extracted text in the preview panel
4. Click "Save All Extracted Text" to save to a file
5. Choose between .txt or .json format

### Debug Page Structure
1. Navigate to any page
2. Click "Debug Page" to analyze the page structure
3. View forms, inputs, buttons, and links in the debug log
4. Use this information for custom navigation logic

### Auto Navigation
1. Enable "Auto Navigation" checkbox
2. Set delay between pages (in seconds)
3. Use "Next Page" to manually advance
4. Use "Skip Current Page" to skip without extracting

### Auto Loop (New Feature)
1. Set the number of iterations (1-100) in the "Number of iterations" field
2. Enter the button text to click for next page (e.g., "Next", "Continue", "Skip for now")
3. Click "Start Auto Loop" to begin the automated process
4. The application will automatically:
   - Extract text from the current page
   - Save the extracted text to a file
   - Click the specified button to go to the next page
   - Repeat for the specified number of iterations
5. Monitor progress with the progress bar and status updates
6. Click "Stop Auto Loop" to stop the process early

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
- **JavaScript Integration**: Page analysis and text extraction
- **Text Processing**: Client-side text extraction
- **Compatibility Layer**: JavaScript polyfills for modern web standards

### JavaScript Compatibility
The application includes polyfills for modern JavaScript APIs that may not be supported in older WebEngine versions:
- **structuredClone polyfill**: Handles modern object cloning used by sites like Y Combinator
- **Multiple injection points**: Ensures compatibility across different page loads
- **Error handling**: Graceful fallbacks when polyfills fail

### Browser Features
- Full web compatibility
- JavaScript support
- Cookie handling
- Session management
- Modern web standards support
- Manual login and form handling

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

### Debug Information
The debug feature provides detailed information about:
- Forms and their attributes
- Input fields and their properties
- Buttons and their text content
- Links and their destinations

## Use Cases

### Content Extraction
- Extract text from news articles
- Collect information from documentation sites
- Gather data from research pages
- Archive web content

### Manual Browsing
- Browse websites that require login
- Navigate complex web applications
- Handle modern authentication systems
- Work with JavaScript-heavy sites

### Batch Processing
- Extract content from multiple pages
- Save structured data for analysis
- Create content archives
- Process large amounts of web content

## Troubleshooting

### Common Issues

1. **Browser not loading**
   - Check internet connection
   - Verify URL format (include https://)
   - Try refreshing the page

2. **Manual login issues**
   - Use the browser interface naturally
   - Some sites may have additional security measures
   - Try refreshing the page if login fails

3. **Text extraction issues**
   - Some sites may block text extraction
   - Try different pages
   - Check browser console for errors
   - Use debug feature to understand page structure

### Performance Tips
- Disable auto navigation for large sites
- Clear extracted text periodically
- Use appropriate delay settings
- Close unnecessary browser tabs

## Security Notes

- No automatic credential handling
- Manual login through browser interface
- Use HTTPS sites when possible
- Be cautious with sensitive data
- No credentials stored in the application

## Future Enhancements

- [ ] Multi-tab support
- [ ] Custom CSS selectors for extraction
- [ ] Proxy support
- [ ] Export to different formats
- [ ] Batch URL processing
- [ ] Advanced navigation patterns
- [ ] Screenshot capture
- [ ] Custom automation scripts
- [ ] Better error handling
- [ ] Performance optimizations

## License

This project is open source and available under the MIT License. 