from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from datetime import datetime
import threading
import os
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

def url_to_filename(url, extension):
    sanitized_url = "".join([c if c.isalnum() else "_" for c in url])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{sanitized_url}_{timestamp}{extension}"

def process_webpage(url):
    driver = None
    try:
        # Install ChromeDriver
        chromedriver_autoinstaller.install()

        # Set Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('w3c', True)

        try:
            # Try connecting to remote WebDriver
            driver = webdriver.Remote(
                command_executor='http://172.16.1.184:4444/wd/hub',
                options=chrome_options
            )
        except Exception as e:
            logging.warning(f"Remote WebDriver connection failed: {e}. Falling back to local ChromeDriver.")
            # Fallback to local ChromeDriver
            driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver-linux64/chromedriver', options=chrome_options)

        driver.get(url)
        driver.implicitly_wait(10)

        # Take a screenshot
        screenshot_filename = f'screenshots/{url_to_filename(url, ".png")}'
        os.makedirs(os.path.dirname(screenshot_filename), exist_ok=True)
        driver.save_screenshot(screenshot_filename)

        # Extract text content
        text_content = driver.find_element(By.TAG_NAME, "body").text
        text_filename = f'screenshots/{url_to_filename(url, ".txt")}'
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write(text_content)

    except Exception as e:
        logging.error(f"Error processing webpage {url}: {e}", exc_info=True)
    finally:
        if driver:
            driver.quit()

@app.route('/', methods=['POST'])
def index():
    if not request.is_json:
        logging.warning("Invalid request: No JSON data")
        return jsonify(error="Invalid request: No JSON data"), 400

    data = request.get_json()
    url = data.get('url')

    if not url:
        logging.warning('No URL provided in the request')
        return jsonify(error='No URL provided'), 400

    logging.info(f'URL received: {url}')
    threading.Thread(target=process_webpage, args=(url,)).start()
    logging.info('Started thread for processing the webpage')
    return jsonify(message="Request received, processing..."), 202

if __name__ == '__main__':
    logging.info('Starting Flask server')
    app.run(host='0.0.0.0', port=8090, threaded=True)
