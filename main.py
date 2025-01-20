# Install necessary packages

# !pip install selenium
# !apt-get update
# !apt install -y chromium-chromedriver
# !cp /usr/lib/chromium-browser/chromedriver /usr/bin
# !apt-get install -y wget unzip
# !apt-get install -y chromium-chromedriver
# !pip install webdriver-manager

# Import libraries
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')  # Prevent sandboxing issues
chrome_options.add_argument('--disable-dev-shm-usage')  # Disable shared memory issues
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")  # Block popups
chrome_options.add_argument("--disable-infobars")  # Disable infobars

# Configure download directory
download_dir = r"/Users/aabid/Desktop/flipkart_scraper"  # Update to a local directory
os.makedirs(download_dir, exist_ok=True)

# Set Chrome options for downloading files
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.popups": 2,
    "download.default_directory": download_dir,  # Set the download directory
    "download.prompt_for_download": False,  # Disable the download prompt
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,  # Enable safe browsing
})

# Initialize WebDriver with automatic ChromeDriver management
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Function to safely click an element
def safe_click(xpath, driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        # print(f"Clicked element with XPath: {xpath}")
    except TimeoutException:
        print(f"Element not found or not clickable: {xpath}")

# Main script
try:
    # Open Flipkart homepage
    url = "https://advertising.flipkart.com/login?tenant=BSS"
    driver.get(url)
    time.sleep(3)  # Allow the page to load

    # Log in
    username_field = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div/div[2]/div/div[2]/form/div[1]/div/div[2]/div/input')
    username_field.send_keys("")
    password_field = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div/div[2]/div/div[2]/form/div[2]/div[1]/div[2]/div/input')
    password_field.send_keys("")
    login_button = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div/div[2]/div/div[2]/form/div[3]/div[1]/button')
    login_button.click()

    # Wait for login to complete
    time.sleep(5)
    print("Login successful!")

    # Close popups if any (adjust the function if specific popups appear)
    try:
        popups = driver.find_elements(By.XPATH, '//button[contains(text(),"Close") or contains(@aria-label, "close")]')
        for popup in popups:
            popup.click()
            print("Popup closed.")
    except NoSuchElementException:
        print("No popups to close.")

    # Perform clicks on provided XPaths
    xpaths_to_click = [
        '//*[@id="popover-content"]/div/div/div/button/div',
        '//*[@id="app"]/div[1]/div[1]/div/button',
        '//*[@id="app"]/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[2]/div/div[1]',
        '//*[@id="app"]/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[2]/div/div[2]/div/div/span/div'
    ]

    for xpath in xpaths_to_click:
        safe_click(xpath, driver)
        time.sleep(2)  # Short delay to ensure the interaction completes

    print("All specified elements have been clicked.")
    time.sleep(5)

    # Check downloaded files
    downloaded_files = os.listdir(download_dir)
    print("Downloaded files:", downloaded_files)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
