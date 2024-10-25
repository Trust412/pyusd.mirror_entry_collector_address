from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import csv

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL to navigate to
url = 'https://pyusd.mirror.xyz/'
i = 0
driver.get(url)
# Open CSV file for writing addresses
with open('address.csv', 'a', newline="", encoding='utf-8-sig') as open_out:
    file_o_csv = csv.writer(open_out, delimiter=',')
    
    try:
        # Wait for entry links to be present on the page
        entry_classes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a._1sjywpl0._1sjywplf.bc5nci5.bc5nci4su.bc5nciih.bc5ncit6.bsvm2h0'))
        )

        # Initialize an array to store entry links
        entry_links = []
        collector_links = []
        # Loop through each entry link found and save them to the array
        for entry_class in entry_classes:
            entry_link = entry_class.get_attribute('href')
            if entry_link and entry_link.startswith('https://pyusd.mirror.xyz/'):
                entry_links.append(entry_link)  # Save valid links to the array
        print("entry_links:  ", entry_links)
        # Now loop through the saved links and open each one
        for url in entry_links:
            driver.get(url)  # Navigate to the entry link
            time.sleep(5)    # Wait for 5 seconds on the new page 
            
            # Scroll to the bottom of the page
            scroll_pause_time = 0.5  # Pause time between scrolls
            scroll_increment = 500    # Pixels to scroll each time

            # Get the initial height of the page
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll down by the defined increment
                driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
                
                # Wait for new content to load
                time.sleep(scroll_pause_time)
                
                # Calculate new scroll height and compare with last height
                new_height = driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    break  # Exit the loop if no new content is loaded
                
                last_height = new_height
            try:
                modal_div = driver.find_element(By.CSS_SELECTOR, 'div._1sjywpl0._1sjywpl1.bc5nciih.bc5ncit1.bc5nciyg')
                collector_tags = modal_div.find_elements(By.TAG_NAME, 'a')
                time.sleep(0.1)
                for collector_tag in collector_tags:
                    print('_______________________________________________________________')
                    collector_link = collector_tag.get_attribute('href')
                    if collector_link != None:
                        i += 1
                        print("collector_link:  ",i, collector_link)
                        collector_links.append(collector_link)
                    time.sleep(0.1)

            except Exception as e:
                print(f"An error occurred: {e}")
                for link in collector_links:
                    if link and link.startswith('https://pyusd.mirror.xyz/0x'):
                        wallet_address = link.split('/')[2]
                        print(wallet_address)
                        file_o_csv.writerow([wallet_address])  # Write to CSV

                    else:
                        try:
                            collector_img_tag = collector_tag.find_element(By.TAG_NAME, 'img')
                            wallet_address = collector_img_tag.get_attribute('alt')
                            print(wallet_address)
                            file_o_csv.writerow([wallet_address])  # Write to CSV

                        except Exception as e:
                            print("Opening new window for: ", link)
                            driver.switch_to.new_window('window')  # Open a new window
                            driver.get(link)  # Navigate to the collector link

                            try:
                                target_script = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, 'script#__NEXT_DATA__'))
                                )
                                json_data = json.loads(target_script.get_attribute('innerHTML'))
                                wallet_address = json_data['props']['pageProps']['publicationLayoutProject']['address']
                                print(wallet_address)
                                file_o_csv.writerow([wallet_address])  # Write to CSV

                            except Exception as json_error:
                                print(f"Error extracting wallet address from JSON: {json_error}")

                            finally:
                                if len(driver.window_handles) > 1:  # Check if there are multiple windows open
                                    driver.close()  # Close the new window
                                    driver.switch_to.window(driver.window_handles[0])  # Switch back to the original window

                
#                 if collector_link.startswith('https://pyusd.mirror.xyz/0x'):
#                     wallet_address = collector_link.split('/')[2]
#                     print(wallet_address)
#                     file_o_csv.writerow([wallet_address])  # Write to CSV

#                 else:
#                     try:
#                         collector_img_tag = collector_tag.find_element(By.TAG_NAME, 'img')
#                         wallet_address = collector_img_tag.get_attribute('alt')
#                         print(wallet_address)
#                         file_o_csv.writerow([wallet_address])  # Write to CSV

#                     except Exception as e:
#                         print("Opening new window for: ", collector_link)
#                         driver.switch_to.new_window('window')  # Open a new window
#                         driver.get(collector_link)  # Navigate to the collector link
#                         time.sleep(4)

#                         try:
#                             target_script = driver.find_element(By.CSS_SELECTOR, 'script#__NEXT_DATA__')
#                             json_data = json.loads(target_script.get_attribute('innerHTML'))
#                             wallet_address = json_data['props']['pageProps']['publicationLayoutProject']['address']
#                             print(wallet_address)
#                             file_o_csv.writerow([wallet_address])  # Write to CSV

#                         except Exception as json_error:
#                             print(f"Error extracting wallet address from JSON: {json_error}")

#                         finally:
#                             if len(driver.window_handles) > 1:  # Check if there are multiple windows open
#                                 driver.close()  # Close the new window
#                                 time.sleep(1)
#                                 driver.switch_to.window(driver.window_handles[0])  # Switch back to the original window

    except Exception as e:
        print(f"An error occurred: {e}")

# Close the driver when done
driver.quit()