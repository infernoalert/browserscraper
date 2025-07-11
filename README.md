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
│   │   └── gui.py               # Graphical user interface
│   ├── utils/
│   │   ├── logger.py            # Logging utilities
│   │   ├── exceptions.py        # Custom exceptions
│   │   └── file_utils.py        # File handling utilities
│   └── main.py                  # Main entry point
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
   - Download ChromeDriver matching your Chrome version
   - Place `chromedriver.exe` in the project directory
   - Or install via: `pip install webdriver-manager`

## 🎮 Usage

### Command-Line Interface (Recommended)

#### Basic Commands

```bash
# Show help and available commands
python -m src.main --help

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

### GUI Interface

```bash
# Launch GUI
python -m src.main gui

# Or run directly
python src/ui/gui.py
```

The GUI provides:
- Interactive website selection
- Real-time browser control
- Visual feedback and status updates
- Easy navigation controls

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

### E-commerce Product Scraping
```bash
python -m src.main scrape-page https://shop.example.com/product/123 \
  --selectors '{
    "title": "h1.product-title",
    "price": ".price-current",
    "description": ".product-description",
    "rating": ".rating-stars"
  }' --output json
```

### News Article Extraction
```bash
python -m src.main scrape-page https://news.example.com/article \
  --selectors '{
    "headline": "h1.headline",
    "author": ".author-name",
    "date": ".publish-date",
    "content": ".article-body"
  }' --output csv
```

### Social Media Links
```bash
python -m src.main scrape-links https://profile.example.com \
  --link-selector "a[href*='social']" --output json
```

### Data Tables
```bash
python -m src.main scrape-table https://data.example.com/table \
  --table-selector "table.data-table" --output csv
```

## 🔧 Advanced Features

### Custom Patterns
Extract data using regex patterns:
```bash
python -m src.main scrape-pattern https://example.com \
  --patterns '{
    "phone": "\\b\\d{3}-\\d{3}-\\d{4}\\b",
    "email": "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"
  }'
```

### Multiple Items Extraction
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
   - Download ChromeDriver matching your Chrome version
   - Install webdriver-manager: `pip install webdriver-manager`

2. **Permission denied:**
   - Run with administrator privileges
   - Check file permissions in output directory

3. **Browser crashes:**
   - Try running in headless mode: `--headless`
   - Reduce browser window size in config

4. **Element not found:**
   - Verify CSS selectors in browser dev tools
   - Increase implicit wait time in config
   - Check if page uses JavaScript loading

5. **Import errors:**
   - Ensure you're running from the project root
   - Check Python path configuration

### Debugging Tips

- Use `--verbose` flag for detailed logging
- Check `scraper.log` for detailed error information
- Use browser dev tools to verify selectors
- Test with simple pages first

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
- Check the troubleshooting section above
- Review the error logs in `scraper.log`
- Open an issue on the repository

---

**Happy Scraping! 🎉** 