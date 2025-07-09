# Selenium Auto Extractor

A command-line Python tool to automate login, navigation, and text extraction from modern websites using Selenium and Chrome.

## Features
- Automates login (if credentials provided)
- Navigates through N pages by clicking a button with specified text
- Extracts all visible text from each page
- Saves all extracted text into a single output file
- Works with any site that Chrome can display (including LinkedIn, if not blocked)
- Fully configurable via command-line arguments

## Requirements
- Python 3.7+
- Google Chrome browser
- ChromeDriver (matching your Chrome version)
- Install Python dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Setup
1. **Download ChromeDriver:**
   - [Get ChromeDriver here](https://sites.google.com/chromium.org/driver/)
   - Make sure the version matches your installed Chrome browser.
   - Place the `chromedriver` executable in your PATH or in the same folder as the script.

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the script from the command line:
```bash
python selenium_auto_extractor.py \
  --url "https://www.linkedin.com/login" \
  --username "your_email" \
  --password "your_password" \
  --button_text "Next" \
  --iterations 10 \
  --output extracted_text.txt
```

### Arguments
- `--url` (required): Start URL (e.g., login page)
- `--username` (optional): Username/email for login
- `--password` (optional): Password for login
- `--username_selector` (optional): CSS selector for username field (default: `#username`)
- `--password_selector` (optional): CSS selector for password field (default: `#password`)
- `--login_button_selector` (optional): CSS selector for login button (default: `button[type="submit"]`)
- `--button_text` (required): Text of the button to click for next page (case-insensitive)
- `--iterations` (optional): Number of pages to process (default: 10)
- `--output` (optional): Output file for all extracted text (default: `extracted_text.txt`)
- `--headless` (optional): Run Chrome in headless mode (no window)

### Example (LinkedIn)
```bash
python selenium_auto_extractor.py \
  --url "https://www.linkedin.com/login" \
  --username "your_email" \
  --password "your_password" \
  --button_text "Next" \
  --iterations 5 \
  --output linkedin_text.txt
```

### Example (Simple Site)
```bash
python selenium_auto_extractor.py \
  --url "https://quotes.toscrape.com/login" \
  --username "user" \
  --password "pass" \
  --button_text "Next" \
  --iterations 3 \
  --output quotes.txt
```

## Notes
- Make sure ChromeDriver is installed and matches your Chrome version.
- Adjust CSS selectors if the login form uses different field names.
- The script will stop early if the next button is not found.
- All extracted text is saved in one file, with page numbers and URLs.
- For advanced extraction (e.g., specific elements), modify the script as needed.

## License
MIT License 