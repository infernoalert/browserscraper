# Browser Scraper 🌐

A comprehensive, modular web scraping tool built with Selenium that supports both command-line and GUI interfaces. Extract data from websites with powerful scraping capabilities, flexible output formats, and robust error handling.

## ✨ Features

### Core Functionality
- **🔍 Multiple Scraping Methods**: Page scraping, table extraction, link collection, image scraping, form analysis, and custom regex patterns
- **🖥️ Dual Interface**: Command-line interface (CLI) for automation and GUI for interactive use
- **📊 Multiple Output Formats**: JSON, CSV, XML, and plain text with automatic file management
- **🌐 Browser Support**: Chrome and Firefox with configurable options
- **⚡ Robust Error Handling**: Comprehensive exception handling with retry mechanisms
- **📝 Advanced Logging**: Colored console output, file logging, and session tracking

### Advanced Features
- **🎯 Smart Element Detection**: Multiple extraction methods for reliable data capture
- **🔄 Automatic Retry**: Configurable retry attempts with exponential backoff
- **💾 Data Export**: Multiple formats with timestamps and backup functionality
- **🛡️ Session Management**: Track scraping sessions with detailed statistics
- **⚙️ Configuration Management**: External config files with sensible defaults
- **🔍 Pattern Matching**: Custom regex patterns for specific data extraction

### Recent Improvements (v2.0.0)
- **🚀 Unified Launcher**: New `launcher.py` script handles all import issues automatically
- **🔧 Robust Error Handling**: Multiple fallback mechanisms for import and runtime errors
- **📦 Better Package Structure**: Proper setup.py and package organization
- **🧪 Comprehensive Testing**: Built-in test suite with `launcher.py test`
- **🛠️ Multiple Entry Points**: Choose from GUI, CLI, or standalone options
- **📝 Enhanced Documentation**: Updated README with troubleshooting guides
- **⚡ Improved Reliability**: Null checks and error handling throughout the codebase

## 🏗️ Project Structure

```
browserscraper/
├── src/
│   ├── core/
│   │   ├── browser_manager.py    # Browser initialization and management
│   │   ├── scraper.py           # Main scraping functionality
│   │   └── config.py            # Configuration management
│   ├── ui/
│   │   ├── cli.py               # Command-line interface
│   │   ├── gui_simple.py        # Simple GUI interface
│   │   └── gui.py               # Advanced GUI interface
│   ├── utils/
│   │   ├── logger.py            # Logging utilities
│   │   ├── exceptions.py        # Custom exceptions
│   │   └── file_utils.py        # File handling utilities
│   └── main.py                  # Main entry point
├── gui_standalone.py            # Standalone GUI (no dependencies)
├── run_gui.py                   # GUI launcher script
├── demo_gui.py                  # Demo with dependency checks
├── launcher.py                  # 🚀 Unified launcher (recommended)
├── test_imports.py              # Import testing script
├── setup.py                     # Package setup script
├── config.json                  # Configuration file (auto-generated)
├── requirements.txt             # Dependencies
├── README.md                    # This file
└── selenium_auto_extractor.py   # Original file (kept for reference)
```

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd browserscraper
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup ChromeDriver:**
   - **Option A**: Download ChromeDriver from [chromedriver.chromium.org](https://chromedriver.chromium.org/)
     - Match your Chrome browser version
     - Place `chromedriver.exe` in the project directory
   - **Option B**: Install webdriver-manager (recommended)
     ```bash
     pip install webdriver-manager
     ```

4. **Verify installation:**
   ```bash
   python launcher.py test
   ```

## 🎮 Usage

### Quick Start

**🚀 Recommended - Unified Launcher (Works Everywhere):**
```bash
# Launch GUI (recommended for beginners)
python launcher.py gui

# Launch CLI (for advanced users)
python launcher.py cli

# Run tests to verify setup
python launcher.py test

# Show all available options
python launcher.py help
```

**For Beginners (GUI):**
```bash
# Unified launcher (recommended - handles all issues)
python launcher.py gui

# Standalone GUI (works without dependencies)
python gui_standalone.py

# Modular GUI (may have import issues)
python run_gui.py

# Demo with dependency checking
python demo_gui.py
```

**For Advanced Users (CLI):**
```bash
# Unified launcher
python launcher.py cli

# Main module
python -m src.main cli

# Show help and available commands
python -m src.main --help
```

### Command-Line Interface (CLI)

#### Basic Commands

```bash
# Scrape a page with CSS selectors
python -m src.main scrape-page https://example.com \
  --selectors '{"title": "h1", "description": "p.description"}'

# Scrape table data
python -m src.main scrape-table https://example.com/table \
  --output csv --filename "extracted_table"

# Scrape all links
python -m src.main scrape-links https://example.com \
  --output json --link-selector "a.external"

# Scrape all images
python -m src.main scrape-images https://example.com \
  --output csv --img-selector "img.gallery"

# Scrape forms
python -m src.main scrape-forms https://example.com \
  --output json

# Custom regex patterns
python -m src.main scrape-pattern https://example.com \
  --patterns '{"email": "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"}'
```

#### Advanced Options

```bash
# Run in headless mode
python -m src.main scrape-page https://example.com \
  --selectors '{"title": "h1"}' --headless

# Use Firefox instead of Chrome
python -m src.main scrape-page https://example.com \
  --selectors '{"title": "h1"}' --browser firefox

# Custom output directory and format
python -m src.main scrape-links https://example.com \
  --output xml --output-dir "my_data" --filename "custom_links"

# Verbose logging
python -m src.main scrape-page https://example.com \
  --selectors '{"title": "h1"}' --verbose

# Custom configuration file
python -m src.main scrape-page https://example.com \
  --selectors '{"title": "h1"}' --config "my_config.json"
```

### GUI Interface (Recommended for Beginners)

#### Launching the GUI

```bash
# Unified launcher (recommended - handles all issues)
python launcher.py gui

# Standalone GUI (works without import issues)
python gui_standalone.py

# Modular GUI (may have import issues)
python run_gui.py

# Using the main module
python -m src.main gui

# Direct execution
python src/ui/gui_simple.py

# Demo with dependency checking
python demo_gui.py
```

#### GUI Features

- **🌐 Browser Control**: Start/stop Chrome/Firefox, headless mode
- **🔍 Scraping Options**: CSS selectors, output formats, file management
- **📊 Real-time Results**: Live display of scraped data
- **📝 Logging**: Detailed logs and status updates
- **💾 Data Export**: Multiple formats (JSON, CSV, XML, TXT)
- **🎛️ Easy Configuration**: Browser settings, output options
- **👁️ Preview Mode**: See page elements before scraping

#### GUI Workflow

1. **Launch GUI**: Run `python run_gui.py`
2. **Enter URL**: Type the website you want to scrape
3. **Configure Browser**: Choose Chrome/Firefox and headless mode
4. **Set Selectors**: Define CSS selectors in JSON format
5. **Choose Output**: Select format and output directory
6. **Start Scraping**: Click "Start Browser" then "Start Scraping"

#### Example CSS Selectors

```json
{
  "title": "h1",
  "content": "p",
  "price": ".price",
  "links": "a",
  "images": "img"
}
```

### Configuration Management

```bash
# Show current configuration
python -m src.main config --show

# Create default configuration file
python -m src.main config --create-default
```

## 📁 Output Files

All scraped data is saved to the `output/` directory by default:

- **Data Files**: `scraped_data_YYYYMMDD_HHMMSS.json` (or csv, xml, txt)
- **Summary Files**: `summary_YYYYMMDD_HHMMSS.json` with statistics
- **Log Files**: `scraper.log` with detailed operation logs

## ⚙️ Configuration

The tool uses a `config.json` file for settings:

```json
{
  "browser": {
    "browser_type": "chrome",
    "headless": false,
    "window_size": [1200, 800],
    "implicit_wait": 10,
    "page_load_timeout": 30,
    "disable_gpu": true,
    "disable_images": false,
    "user_agent": null
  },
  "scraping": {
    "default_delay": 1.0,
    "retry_attempts": 3,
    "retry_delay": 2.0,
    "respect_robots_txt": true,
    "max_pages": 100
  },
  "output": {
    "output_dir": "output",
    "output_format": "json",
    "filename_prefix": "scraped_data",
    "include_timestamp": true,
    "create_backup": true
  },
  "log_level": "INFO",
  "log_file": "scraper.log"
}
```

## 🎯 Scraping Examples

### GUI Examples

**E-commerce Product Scraping:**
1. Launch GUI: `python gui_standalone.py`
2. Enter URL: `https://shop.example.com/product/123`
3. Set selectors:
   ```json
   {
     "title": "h1.product-title",
     "price": ".price-current",
     "description": ".product-description",
     "rating": ".rating-stars"
   }
   ```
4. Choose output: JSON
5. Start scraping

**News Article Extraction:**
1. Enter URL: `https://news.example.com/article`
2. Set selectors:
   ```json
   {
     "headline": "h1.headline",
     "author": ".author-name",
     "date": ".publish-date",
     "content": ".article-body"
   }
   ```
3. Choose output: CSV

### CLI Examples

**E-commerce Product Scraping:**
```bash
python -m src.main scrape-page https://shop.example.com/product/123 \
  --selectors '{
    "title": "h1.product-title",
    "price": ".price-current",
    "description": ".product-description",
    "rating": ".rating-stars"
  }' --output json
```

**News Article Extraction:**
```bash
python -m src.main scrape-page https://news.example.com/article \
  --selectors '{
    "headline": "h1.headline",
    "author": ".author-name",
    "date": ".publish-date",
    "content": ".article-body"
  }' --output csv
```

**Social Media Links:**
```bash
python -m src.main scrape-links https://profile.example.com \
  --link-selector "a[href*='social']" --output json
```

**Data Tables:**
```bash
python -m src.main scrape-table https://data.example.com/table \
  --table-selector "table.data-table" --output csv
```

## 🔧 Advanced Features

### GUI Advanced Features

**Custom Patterns (Regex):**
1. Launch GUI and enter URL
2. Use the "Custom Patterns" option
3. Set patterns:
   ```json
   {
     "phone": "\\b\\d{3}-\\d{3}-\\d{4}\\b",
     "email": "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"
   }
   ```

**Preview Mode:**
- Click "Preview Page" to see available elements
- View page statistics (links, images, tables, forms)
- Identify CSS selectors before scraping

**Real-time Logging:**
- Watch scraping progress in real-time
- See detailed error messages
- Monitor browser status

### CLI Advanced Features

**Custom Patterns:**
```bash
python -m src.main scrape-pattern https://example.com \
  --patterns '{
    "phone": "\\b\\d{3}-\\d{3}-\\d{4}\\b",
    "email": "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"
  }'
```

**Multiple Items Extraction:**
```bash
python -m src.main scrape-page https://example.com/products \
  --selectors '{
    "container": ".product-item",
    "name": ".product-name",
    "price": ".product-price"
  }' --multiple
```

### Session Statistics
Each scraping session generates statistics:
- Pages visited
- Items extracted
- Errors encountered
- Session duration
- Success/failure rates

## 🛠️ Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black src/
flake8 src/
```

### Type Checking
```bash
mypy src/
```

## 🚨 Troubleshooting

### Common Issues

1. **ChromeDriver not found:**
   - **Solution**: Install webdriver-manager: `pip install webdriver-manager`
   - **Alternative**: Download ChromeDriver from [chromedriver.chromium.org](https://chromedriver.chromium.org/)

2. **GUI not starting:**
   - **First**: Try the unified launcher: `python launcher.py gui`
   - **Check**: Run `python launcher.py test` for dependency verification
   - **Solution**: Install missing dependencies: `pip install -r requirements.txt`

3. **Import errors:**
   - **Use unified launcher**: `python launcher.py gui` (handles all import issues)
   - **Try standalone GUI**: `python gui_standalone.py` (no import dependencies)
   - **Check**: Run `python launcher.py test` to verify setup

4. **Permission denied:**
   - Run with administrator privileges
   - Check file permissions in output directory

5. **Browser crashes:**
   - Try running in headless mode (GUI option)
   - Reduce browser window size in config
   - Update ChromeDriver to match Chrome version

6. **Element not found:**
   - Use GUI's "Preview Page" feature to identify elements
   - Verify CSS selectors in browser dev tools
   - Increase implicit wait time in config
   - Check if page uses JavaScript loading

### Debugging Tips

**For GUI:**
- Use the "Preview Page" button to see available elements
- Check the log panel for detailed error messages
- Try different CSS selectors if elements aren't found

**For CLI:**
- Use `--verbose` flag for detailed logging
- Check `scraper.log` for detailed error information
- Use browser dev tools to verify selectors
- Test with simple pages first

### Getting Help

1. **Run tests**: `python launcher.py test`
2. **Check dependencies**: The test will verify all required packages
3. **Test ChromeDriver**: The test will verify browser automation
4. **View logs**: Check the log panel in GUI or `scraper.log` file

### Quick Fixes

**If nothing works:**
```bash
# 1. Run tests to identify issues
python launcher.py test

# 2. Try standalone GUI (most reliable)
python gui_standalone.py

# 3. Install dependencies if needed
pip install -r requirements.txt

# 4. Try unified launcher
python launcher.py gui
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests and ensure they pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Selenium](https://selenium.dev/) for browser automation
- Uses [tkinter](https://docs.python.org/3/library/tkinter.html) for GUI
- Inspired by the need for accessible web scraping tools

## 📞 Support

For issues and questions:
- **First**: Run `python launcher.py test` to check your setup
- **Check**: The troubleshooting section above
- **Review**: Error logs in `scraper.log` or GUI log panel
- **Report**: Open an issue on the repository

## 🎯 Quick Reference

### 🚀 Unified Launcher (Recommended)
```bash
# Launch GUI
python launcher.py gui

# Launch CLI
python launcher.py cli

# Run tests
python launcher.py test

# Show help
python launcher.py help
```

### GUI Commands
```bash
# Unified launcher (handles all issues)
python launcher.py gui

# Standalone GUI (most reliable)
python gui_standalone.py

# Modular GUI
python run_gui.py

# Demo with checks
python demo_gui.py
```

### CLI Commands
```bash
# Unified launcher
python launcher.py cli

# Show help
python -m src.main --help

# Scrape page
python -m src.main scrape-page https://example.com --selectors '{"title": "h1"}'

# Scrape table
python -m src.main scrape-table https://example.com --output csv
```

### Common CSS Selectors
```json
{
  "title": "h1",
  "content": "p",
  "price": ".price",
  "links": "a",
  "images": "img"
}
```

### Troubleshooting Commands
```bash
# Test everything
python launcher.py test

# Check dependencies
pip install -r requirements.txt

# Try standalone GUI if others fail
python gui_standalone.py
```

---

**Happy Scraping! 🎉** 