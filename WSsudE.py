from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

folder_destination = "C:\\Users\\Vornicu\\Desktop\\FolderFisa"

# Create the destination folder if it doesn't exist
if not os.path.exists(folder_destination):
    os.makedirs(folder_destination)

# Configure Chrome options
chrome_options = Options()
prefs = {
    "download.default_directory": folder_destination,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--disable-popup-blocking")  # Disable popup blocking
chrome_options.add_argument("--disable-search-engine-choice-screen")

# Path to the ChromeDriver executable
service = Service(executable_path="chromedriver.exe")  # Replace with the correct path

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)

def scroll_into_view(element):
    """Scrolls the given element into the viewport."""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    time.sleep(1)  # Optional: wait for the scroll to complete

def element_is_visible(element):
    """Checks if the element is visible in the viewport."""
    element_location = element.location_once_scrolled_into_view
    viewport_height = driver.execute_script("return window.innerHeight")
    element_position = driver.execute_script("return arguments[0].getBoundingClientRect();", element)
    return (element_position.top >= 0 and element_position.bottom <= viewport_height)

try:
    driver.get("https://regiosudest.ro/ghiduri")

    nav_boxes = driver.find_elements(By.XPATH, '//li[@class="nav-box"]')
    nav_boxes_count = len(nav_boxes)

    for nav_box_index in range(nav_boxes_count):
        try:
            # Re-fetch the nav_boxes to ensure you get the latest DOM state
            nav_boxes = driver.find_elements(By.XPATH, '//li[@class="nav-box"]')

            # Check if the index is within the current range of nav_boxes
            if nav_box_index >= len(nav_boxes):
                print(f"Nav box {nav_box_index} is out of range.")
                break

            nav_box = nav_boxes[nav_box_index]
            scroll_into_view(nav_box)
            nav_box.click()
            time.sleep(2)  # Wait for the page to load

            # Click on the folder icon
            folder_icon = wait.until(EC.element_to_be_clickable((By.XPATH, '//i[@class="far fa-folder-open"]')))
            scroll_into_view(folder_icon)
            folder_icon.click()
            time.sleep(2)  # Wait for the content to load

            # Process all article headers
            while True:
                article_headers = driver.find_elements(By.XPATH, '//div[@class="article-header"]')
                if not article_headers:
                    print("No article headers found.")
                    break

                for index in range(len(article_headers)):
                    try:
                        # Re-fetch article_headers before clicking on the next one
                        article_headers = driver.find_elements(By.XPATH, '//div[@class="article-header"]')
                        header = article_headers[index]
                        time.sleep(2)
                        if not element_is_visible(header):
                            header.click()
                            scroll_into_view(header)
                            header.click()
                        time.sleep(2)  # Wait for the article to load

                        # Download files in the article
                        download_links = driver.find_elements(By.XPATH, '//a[contains(@href, "/images/")]')
                        for link in download_links:
                            href = link.get_attribute('href')
                            if href:
                                driver.get(href)
                                time.sleep(10)  # Wait for the download to start
                                time.sleep(2)

                        driver.back()  # Go back to the list of articles
                        time.sleep(2)

                    except Exception as e:
                        print(f"Error processing article header {index}: {e}")
                        driver.back()  # Ensure you go back in case of an error
                        time.sleep(2)
                        continue

                # Scroll down to load more content if applicable
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(2)  # Wait for the scroll to complete

                # Re-fetch the article headers
                article_headers = driver.find_elements(By.XPATH, '//div[@class="article-header"]')
                if not article_headers:
                    break

            # Return to the main page with nav-boxes
            driver.back()
            driver.back()
            time.sleep(2)  # Wait for the page to load

        except Exception as e:
            print(f"Error in processing nav box {nav_box_index}: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
