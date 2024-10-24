from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import json

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL to navigate to
url = 'https://pyusd.mirror.xyz/'
driver.get(url)

try:
    # Wait for entry links to be present on the page
    entry_classes = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a._1sjywpl0._1sjywplf.bc5nci5.bc5nci4su.bc5nciih.bc5ncit6.bsvm2h0'))
    )

    # Initialize an array to store entry links
    entry_links = []

    # Loop through each entry link found and save them to the array
    for entry_class in entry_classes:
        entry_link = entry_class.get_attribute('href')
        if entry_link and entry_link.startswith('https://pyusd.mirror.xyz/'):
            entry_links.append(entry_link)  # Save valid links to the array

    # Now loop through the saved links and open each one
    for link in entry_links:
        print("Processing: " + link)
        driver.get(link)  # Navigate to the entry link
        sleep(5)  # Wait for 5 seconds on the new page
        modal_div = driver.find_element(By.CSS_SELECTOR, 'div._1sjywpl0._1sjywpl1.bc5nciih.bc5ncit1.bc5nciyg')
        collector_tags = modal_div.find_elements(By.TAG_NAME, 'a')

        for collector_tag in collector_tags:
            collector_link = collector_tag.get_attribute('href')
            if collector_link and collector_link.startswith('https://pyusd.mirror.xyz/0x'):
                wallet_address = collector_link.split('/')[2]
                print(wallet_address)
            else:
                try:
                    collector_img_tag = collector_tag.find_element(By.TAG_NAME, 'img')
                    wallet_address = collector_img_tag.get_attribute('alt')
                    print(wallet_address)
                except Exception as e:
                    driver.get(collector_link)
                    sleep(4)
                    target_script = driver.find_element(By.CSS_SELECTOR, 'script#__NEXT_DATA__')
                    print("find script")
                    json_data = json.loads(target_script.get_attribute('innerHTML'))
                    wallet_address = json_data['props']['pageProps']['publicationLayoutProject']['address']
                    print(wallet_address)
                    driver.back()

except Exception as e:
    print(f"An error occurred: {e}")

# Close the driver when done
driver.quit()