import os
from urllib.parse import urljoin
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import json

import time

username = 'marouansaif3@gmail.com'
password = 'zaze1234'

# Define login credentials

# Path to Chromium WebDriver executable
chromium_driver_path = "../chrome-win/chrome.exe"

# Initialize Chromium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')  # Bypass OS security model
#options.add_argument('--headless')  # No browser

options.add_argument('--disable-dev-shm-usage')  # Avoid /dev/shm usage
options.add_argument('--disable-gpu')  # Disable GPU acceleration
service=webdriver.ChromeService(chromium_driver_path)
driver = webdriver.Chrome(options=options)
driver

# URL of the login page
login_url = 'https://www.traceparts.com/en/sign-in'

# Load the login page
driver.get(login_url)

# Find the login form elements and fill them with credentials
email_field = driver.find_element(By.ID,'Email')
password_field = driver.find_element(By.ID,'Password')

email_field.send_keys(username)
password_field.send_keys(password)

# Submit the form
password_field.send_keys(Keys.RETURN)

# Wait for the login process to complete
time.sleep(5)  # You may need to adjust the sleep time depending on the website's response time

# Check if login was successful
if 'Design Library' in driver.page_source:
    print("Login successful!")
    url = "https://www.traceparts.com/fr/search/classification-traceparts-composants-mecaniques-elements-de-fixation-vis-et-boulons-boulons-dancrage?CatalogPath=TRACEPARTS%3ATP01001013007"
    driver.get(url)
    def extract_links(driver, url, depth=0, parent_url=None):
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        links = []

        # Tentative de localiser l'élément 'search-results-items' s'il est supposé être sur la page
        try:
            parent_element = wait.until(EC.presence_of_element_located((By.ID, "search-results-items")))
            cards = parent_element.find_elements(By.CLASS_NAME, "card")

            for card in cards:
                link_element = card.find_element(By.TAG_NAME, "a")
                href = link_element.get_attribute('href')
                if href:  # S'assurer que le lien est valide et unique
                    full_link = urljoin(driver.current_url, href)
                    links.append(full_link)

        except TimeoutException:
            print("No 'search-results-items' found at depth", depth, "under", parent_url)

        # Vérifier la présence du bouton
        try:
            button = driver.find_element(By.CLASS_NAME, "tp-i-download_3")
            print(f"Button found at depth {depth} under {parent_url}. No further action on this branch.")
            select = Select(driver.find_element(By.ID, 'cad-format-select'))

            select.select_by_value('659')
            print("STEP AP242 selected.")
            if select:
                # Cliquer sur le bouton pour rendre la section visible
                download_button = driver.find_element(By.ID, "direct-cad-download")
                download_button.click()
                print("Clicked on the download button to make the dashboard visible.")

                # Attendre que la section dashboard devienne visible
                WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.ID, "dashboard-section"))
                )
                print("Dashboard section is now visible.")


                download_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//aside[@id='dashboard-section']//div[contains(@class, 'download-item-container')]//a[contains(@data-ga-code, 'MYA-DFC')]"))
                )
                if download_link:
                    
                    download = driver.find_element(By.CLASS_NAME, "download-item")
                    label= driver.find_element(By.CLASS_NAME, "download-part-label")

                    print(download.get_attribute('href'))
                    print(label.text)
                    new_data = {
                        'label_text': label.text,
                        'link': download.get_attribute('href')
                    }

                    file_path = 'output.json'

                    if os.path.exists(file_path):
                        with open(file_path, 'r') as json_file:
                            data = json.load(json_file)
                        data.append(new_data)
                        with open(file_path, 'w') as json_file:
                            json.dump(data, json_file, indent=4)
                    else:
                        with open(file_path, 'w') as json_file:
                            json.dump([new_data], json_file, indent=4)  # Notez que les données sont stockées dans une liste
                        print("Fichier JSON créé avec succès.")



            return  # Arrêt après récupération du lien

        except NoSuchElementException:
            print("No desired button found at depth", depth, "under", parent_url)

        print("\nDepth", depth, ": Found", len(links), "links under", parent_url)
        for link in links:
            print(" -", link)

        # Continuer l'exploration seulement s'il y a des liens
        for link in links:
            print("\nNavigating to link at depth", depth + 1, ":", link)
            extract_links(driver, link, depth + 1, link)
        return

    extract_links(driver, url, parent_url=url)
        # Nettoyage : Fermer le navigateur après avoir terminé
        
else:
    print("Login failed.")

# Close the browser
driver.quit()