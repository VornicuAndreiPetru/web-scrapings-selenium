from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import requests

# Set the download directory
download_dir = "C:\\Users\\Vornicu\\Desktop\\FolderFisa"


chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False
}
chrome_options.add_experimental_option("prefs", prefs)

# Specify the path to your webdriver
webdriver_service = Service('//chromedriver.exe')


driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)


driver.get("https://regionordest.ro/apeluri-de-proiecte/")


time.sleep(5)


project_elements = driver.find_elements(By.XPATH, '//div[@data-posttype="apel-proiect"]')


for project in project_elements:
    try:

        project_link = project.find_element(By.XPATH, './/a[contains(@href, "/apel-proiect/")]')
        project_link.send_keys(Keys.CONTROL + Keys.RETURN)


        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)
        status = driver.find_element(By.XPATH, '//*[@id="stare_apel_proiect"]/div/div/div[1]/div')
        if status.text == "Deschis" or status.text == "Consultare publică închisă" or status.text == "Lansat":


            details_link = driver.find_element(By.XPATH, '//*[@id="template_apel_proiect"]/div/div[1]/div[11]/div/div/a')
            details_link.send_keys(Keys.CONTROL + Keys.RETURN)


            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)



            download_link = driver.find_element(By.XPATH, '//a[contains(@href, "/wp-content/")]')
            file_url = download_link.get_attribute('href')

            # Download the file using requests to ensure it goes to the specific folder
            response = requests.get(file_url)
            file_name = os.path.join(download_dir, file_url.split("/")[-1])

        with open(file_name, 'wb') as file:
            file.write(response.content)


        driver.close()
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        print(f"An error occurred: {e}")

        while len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
        driver.switch_to.window(driver.window_handles[0])

# Quit the driver
driver.quit()
