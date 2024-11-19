import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
import time

folder_destinatie = "C:\\Users\\Vornicu\\Desktop\\FolderFisa"

# Creează folderul de destinație dacă nu există
if not os.path.exists(folder_destinatie):
    os.makedirs(folder_destinatie)

# Configurează opțiunile Chrome pentru a seta folderul de descărcare și pentru a descărca automat PDF-uri
chrome_options = webdriver.ChromeOptions()
prefs = {
    'download.default_directory': folder_destinatie,
    'plugins.always_open_pdf_externally': True
}
chrome_options.add_argument("--disable-search-engine-choice-screen")
chrome_options.add_experimental_option('prefs', prefs)

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.vest.ro/finantari?tab=toate")
page = 1  # Start with page 1
max_pages = 3

while page <= max_pages:
    try:
        WebDriverWait(driver, 100).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'i-col-3'))
        )
    except TimeoutException:
        print("Timed out waiting for page to load.")
        break

    elements = driver.find_elements(By.CLASS_NAME, 'i-col-3')

    for i in range(min(12, len(elements))):  # Process only 12 cards per page
        try:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get("https://www.vest.ro/finantari?tab=toate&page=" + str(page))

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="i-col-3"]/div/a'))
            )


            # Găsește din nou toate elementele în noul tab
            elements_new_tab = driver.find_elements(By.XPATH, '//div[@class="i-col-3"]/div/a')

            # Scroll the element into view
            driver.execute_script("arguments[0].scrollIntoView(true);", elements_new_tab[i])

            # Click pe elementul curent using JavaScript
            driver.execute_script("arguments[0].click();", elements_new_tab[i])

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="cookiebar"]/div[2]/button'))
                )
                driver.find_element(By.XPATH, '//*[@id="cookiebar"]/div[2]/button').click()
            except TimeoutException:
                pass

            xpath_query = (
                '//*[@id="page-interventie"]/div/div[2]/div[1]/div[2]/div/a | '
                '//*[@id="page-interventie"]/div/div[2]/div[1]/div[2]/a'
            )

            # Scroll the link into view and click using JavaScript
            link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_query))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", link)
            driver.execute_script("arguments[0].click();", link)

            # Wait for the PDF download to start (you can adjust the sleep time if necessary)
            time.sleep(5)

            driver.close()

            # Treci înapoi la tab-ul inițial
            driver.switch_to.window(driver.window_handles[0])

        except (TimeoutException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException) as e:
            print(f"An error occurred with element {i}: {e}")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    # Check for the "Next" button and click it
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="page-prioritate"]/section/div[2]/div/div[13]/nav/div/a[3]'))
        )
        print("Clicking the Next button.")
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        driver.execute_script("arguments[0].click();", next_button)
        page += 1
        time.sleep(5)  # Wait for the next page to load
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Cannot find the Next button or no more pages to navigate: {e}")
        break

driver.quit()
