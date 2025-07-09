import sys
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# --- Command-line arguments ---
def parse_args():
    parser = argparse.ArgumentParser(description="Automate login, navigation, and text extraction using Selenium.")
    parser.add_argument('--url', required=True, help='Start URL (e.g., LinkedIn login page)')
    parser.add_argument('--username', help='Username/email for login (if required)')
    parser.add_argument('--password', help='Password for login (if required)')
    parser.add_argument('--username_selector', default='#username', help='CSS selector for username field')
    parser.add_argument('--password_selector', default='#password', help='CSS selector for password field')
    parser.add_argument('--login_button_selector', default='button[type="submit"]', help='CSS selector for login button')
    parser.add_argument('--button_text', required=True, help='Text of the button to click for next page (case-insensitive)')
    parser.add_argument('--iterations', type=int, default=10, help='Number of pages to process')
    parser.add_argument('--output', default='extracted_text.txt', help='Output file for all extracted text')
    parser.add_argument('--headless', action='store_true', help='Run Chrome in headless mode (no window)')
    return parser.parse_args()

# --- Main automation logic ---
def main():
    args = parse_args()

    # Set up Chrome options
    chrome_options = Options()
    if args.headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1200,800')

    # Start Chrome
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    try:
        print(f"Opening: {args.url}")
        driver.get(args.url)
        time.sleep(2)

        # --- Login if credentials provided ---
        if args.username and args.password:
            print("Attempting login...")
            username_field = driver.find_element(By.CSS_SELECTOR, args.username_selector)
            password_field = driver.find_element(By.CSS_SELECTOR, args.password_selector)
            username_field.clear()
            username_field.send_keys(args.username)
            password_field.clear()
            password_field.send_keys(args.password)
            login_button = driver.find_element(By.CSS_SELECTOR, args.login_button_selector)
            login_button.click()
            time.sleep(5)  # Wait for login to complete

        extracted_texts = []

        for i in range(args.iterations):
            print(f"[Step {i+1}/{args.iterations}] Extracting text...")
            # Extract visible text from the page
            body = driver.find_element(By.TAG_NAME, 'body')
            page_text = body.text.strip()
            extracted_texts.append({
                'url': driver.current_url,
                'text': page_text
            })

            # Try to find and click the next button
            print(f"[Step {i+1}/{args.iterations}] Looking for button: '{args.button_text}'")
            found = False
            # Try buttons, links, and inputs
            elements = driver.find_elements(By.XPATH, f"//*[self::button or self::a or self::input[@type='button'] or self::input[@type='submit']]")
            for el in elements:
                try:
                    text = (el.text or el.get_attribute('value') or '').strip().lower()
                    if text == args.button_text.strip().lower():
                        el.click()
                        found = True
                        print(f"[Step {i+1}/{args.iterations}] Clicked button: {el.tag_name}")
                        break
                except Exception:
                    continue
            if not found:
                print(f"[Step {i+1}/{args.iterations}] Button with text '{args.button_text}' not found. Stopping loop.")
                break
            time.sleep(3)  # Wait for next page to load

        # --- Save all extracted texts to one file ---
        print(f"Saving all extracted text to: {args.output}")
        with open(args.output, 'w', encoding='utf-8') as f:
            for i, entry in enumerate(extracted_texts, 1):
                f.write(f"=== Page {i} ===\n")
                f.write(f"URL: {entry['url']}\n")
                f.write("-" * 50 + "\n")
                f.write(entry['text'] + "\n\n")
        print("Done!")

    finally:
        driver.quit()

if __name__ == '__main__':
    main() 