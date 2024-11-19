import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import hashlib

folder_destinatie = "C:\\Users\\Vornicu\\Desktop\\FolderFisa"

if not os.path.exists(folder_destinatie):
    os.mkdir(folder_destinatie)

chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": folder_destinatie}
chrome_options.add_experimental_option("prefs", prefs)

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.adrbi.ro/programe-regionale/por-bi-2021-2027/ghiduri-in-consultare/")

WebDriverWait(driver, 100).until(
    EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/programe-regionale/por")]'))
)
elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/programe-regionale/por")]')



#article/p[10]/strong/span/a


for i in range(min(50, len(elements))):
    try:

        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])

        driver.get("https://www.adrbi.ro/programe-regionale/por-bi-2021-2027/ghiduri-lansate/")

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//article/p/a[contains(@href, "/programe-regionale/por")]'))
        )

        # elements_new_tab = driver.find_elements(By.XPATH, '//article/p/a[contains(@href, "/programe-regionale/por")]' or '//article/p/strong/span/a[contains(@href, "/programe-regionale/por")]' )


        xpath_query = (
            '//article/p/a[contains(@href, "/programe-regionale/por")] | '
            '//article/p/strong/span/a[contains(@href, "/programe-regionale/por")]'
        )

        elements_new_tab = driver.find_elements(By.XPATH, xpath_query)
        # Click pe elementul curent
        elements_new_tab[i].click()

        # try:
        #     WebDriverWait(driver, 2).until(
        #         EC.presence_of_element_located((By.CLASS_NAME, 'triggerCookies'))
        #     )
        #     driver.find_element(By.CLASS_NAME, 'triggerCookies').click()
        # except:
        #     pass

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, ".docx")]'))
        )

        link = driver.find_element(By.XPATH, '//a[contains(@href, ".docx")]')
        link.click()

        driver.close()

        # Treci înapoi la tab-ul inițial
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(f"An error occurred with element {i}: {e}")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])



for i in range(min(50, len(elements))):
    try:

        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])

        driver.get("https://www.adrbi.ro/programe-regionale/por-bi-2021-2027/ghiduri-in-consultare/")

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/programe-regionale/por")]'))
        )

        elements_new_tab = driver.find_elements(By.XPATH, '//a[contains(@href, "/programe-regionale/por")]')

        # Click pe elementul curent
        elements_new_tab[i].click()

        # try:
        #     WebDriverWait(driver, 2).until(
        #         EC.presence_of_element_located((By.CLASS_NAME, 'triggerCookies'))
        #     )
        #     driver.find_element(By.CLASS_NAME, 'triggerCookies').click()
        # except:
        #     pass

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, ".docx")]'))
        )

        link = driver.find_element(By.XPATH, '//a[contains(@href, ".docx")]')
        link.click()

        driver.close()

        # Treci înapoi la tab-ul inițial
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(f"An error occurred with element {i}: {e}")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


#            <------OPTIONAL------->

# def hash_file(filepath):
#     """Generate MD5 hash for a file."""
#     hasher = hashlib.md5()
#     with open(filepath, 'rb') as file:
#         buf = file.read()
#         hasher.update(buf)
#     return hasher.hexdigest()
#
#
# def delete_duplicates(folder_path):
#
#     files_checked = {}
#     files_deleted = 0
#
#     for root, dirs, files in os.walk(folder_path):
#         for filename in files:
#             filepath = os.path.join(root, filename)
#             file_hash = hash_file(filepath)
#
#             if file_hash in files_checked:
#                 os.remove(filepath)
#                 files_deleted += 1
#                 print(f"Deleted duplicate file: {filepath}")
#             else:
#                 files_checked[file_hash] = filepath
#
#     print(f"Total duplicates deleted: {files_deleted}")
#


# delete_duplicates("C:\\Users\\Vornicu\\Desktop\\FolderFisa")
time.sleep(10)