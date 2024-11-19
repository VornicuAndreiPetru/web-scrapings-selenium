import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


folder_destinatie = "C:\\Users\\Vornicu\\Desktop\\FolderFisa"

# Creează folderul de destinație dacă nu există
if not os.path.exists(folder_destinatie):
    os.makedirs(folder_destinatie)

# Configurează opțiunile Chrome pentru a seta folderul de descărcare
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': folder_destinatie}
chrome_options.add_experimental_option('prefs', prefs)


service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)


driver.get("https://2021-2027.adrmuntenia.ro/apeluri-de-proiecte")


WebDriverWait(driver, 2).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'bi-arrow-right-square-fill'))
)


elements = driver.find_elements(By.CLASS_NAME, 'bi-arrow-right-square-fill')



for i in range(min(100, len(elements))):
    try:

        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])


        driver.get("https://2021-2027.adrmuntenia.ro/apeluri-de-proiecte")


        WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'bi-arrow-right-square-fill'))
        )



        # Găsește din nou toate elementele în noul tab
        elements_new_tab = driver.find_elements(By.CLASS_NAME, 'bi-arrow-right-square-fill')

        # Click pe elementul curent
        elements_new_tab[i].click()


        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'triggerCookies'))
            )
            driver.find_element(By.CLASS_NAME, 'triggerCookies').click()
        except:
            pass


        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Descărcați '))
        )

        badge_secondary = driver.find_elements(By.CLASS_NAME, 'badge.bg-secondary')
        badge_success = driver.find_elements(By.CLASS_NAME, 'badge.bg-success')

        if badge_secondary or badge_success:
            link = driver.find_element(By.PARTIAL_LINK_TEXT, 'Descărcați ')
            link.click()


            time.sleep(10)


        driver.close()

        # Treci înapoi la tab-ul inițial
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(f"An error occurred with element {i}: {e}")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

driver.quit()
