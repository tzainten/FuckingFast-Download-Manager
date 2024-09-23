import os
import os.path
import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.remote_connection import LOGGER
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

import logging
LOGGER.setLevel(logging.WARNING)

print("This program will automatically download all of the necessary .part.rar files for whatever FitGirl game you want to download.")
time.sleep(2)
print()
print("FuckingFast IS THE ONLY DOWNLOAD MIRROR THAT IS SUPPORTED! DO NOT TRY ANY OTHER LINKS!")
print("IF YOU NEED AN EXAMPLE, HERE IS A VALID LINK THAT WORKS: https://paste.fitgirl-repacks.site/?2d25d933656bc78a#6vZZAEdL8nYvhxN5Vji88SNLAkBEHhtXEUfQquPQ6Rw2")
print()
time.sleep(2)
print()
print("FILES WILL NOT APPEAR IN YOUR DEFAULT DOWNLOADS FOLDER!")
print("THEY WILL INSTEAD APPEAR IN A DOWNLOADS FOLDER THAT IS CREATED NEXT TO THIS .EXE FILE!")
time.sleep(2)

print()
print()
print("Enter the URL with the list of Download Links: ", end = "")
download_links_url = input()

executing_path = os.path.dirname(sys.argv[0])
download_path = executing_path + "/downloads"
if not os.path.exists(download_path):
    os.makedirs(download_path)

print("Downloading to " + download_path)

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--log-level=3")

prefs = {
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "download.default_directory": os.path.abspath(download_path),
    "savefile.default_directory": os.path.abspath(download_path)
}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.set_capability("browserVersion", "117")

driver = webdriver.Chrome(options=options)
driver.get(download_links_url)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "downloadlinks")))

all_links = driver.find_elements(By.TAG_NAME, "a")
filtered_links = list()
file_names = list()
for link in all_links:
    href = link.get_attribute("href")
    if (href == None): continue
    if ("part" not in href or ".rar" not in href): continue
    filtered_links.append(href)
    file_names.append(href.split("#", 1)[1])

local_file_names = list()
for entry in os.scandir(download_path):
    if not entry.is_file():
        continue

    local_file_names.append(entry.name)

for local_file_name in local_file_names:
    potential_duplicate = "(" in local_file_name and ").rar" in local_file_name
    if (".crdownload" in local_file_name or potential_duplicate):
        print("Removing " + local_file_name)
        os.remove(download_path + "/" + local_file_name)

# idx = 0
# for local_file_name in local_file_names:
#     try:
#         if local_file_name in file_names:
#             print("Skipping " + file_names[idx])
#             del file_names[idx]
#             del filtered_links[idx]
#             continue
#     except:
#         break
#     idx = idx + 1

link_idx = 0
while (True):
    if (link_idx >= len(file_names)):
        break
    
    file_name = file_names[link_idx]
    if (file_name in local_file_names):
        print("Skipping " + file_name)
        link_idx = link_idx + 1
        continue

    child_driver = webdriver.Chrome(options=options)
    child_driver.get(filtered_links[link_idx])

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "button")))

    all_buttons = child_driver.find_elements(By.TAG_NAME, "button")
    button = None
    for btn in all_buttons:
        if (btn.text == "DOWNLOAD"):
            button = btn
            break

    button.click()
    child_driver.switch_to.window(child_driver.window_handles[1]) # Try to close ad tab
    child_driver.close()
    child_driver.switch_to.window(child_driver.window_handles[0]) # Switch back to download page and click button again. The ad shouldn't show up again
    button.click()

    print("Downloading " + file_names[link_idx])
    time.sleep(5)

    while (True):
        file_path = download_path + "/" + file_names[link_idx] + ".crdownload"
        is_file_still_downloading = os.path.isfile(file_path)
        if (not is_file_still_downloading):
            link_idx = link_idx + 1
            break
        time.sleep(1)

    child_driver.close()

    if (link_idx >= len(filtered_links)):
        break

missing_files = list()
for file in file_names:
    file_path = download_path + "/" + file
    if (not os.path.isfile(file_path)):
        missing_files.append(file)

if (len(missing_files) == 0):
    print("Successfully installed all files!")
else:
    print("Missing " + str(len(missing_files)) + " files:")
    for missing_file in missing_files:
        print(missing_file)