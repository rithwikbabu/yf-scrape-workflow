from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re
import json
from datetime import datetime

# Initialize ChromeDriver
service = Service(executable_path='/usr/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)

driver.get(f'https://finance.yahoo.com/news/')

news_boxes = driver.find_elements(By.CLASS_NAME, 'Cf')
patterns = {
    "news": re.compile(r'https://finance\.yahoo\.com/news/.+\.html'),
    "media": re.compile(r'https://finance\.yahoo\.com/m/.+\.html'),
    "video": re.compile(r'https://finance\.yahoo\.com/video/.+\.html'),
}

def extract_link_data(box):
    link_dict = {"link": None, "publisher": None, "type": None}
    s = box.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    box_text = re.split('\n', box.text)

    for string in box_text:
        if "•" in string:
            link_data = string.split("•")
            link_dict["publisher"] = link_data[0]
    return s, link_dict

news_links = []

for box in news_boxes:
    link, link_dict = extract_link_data(box)
    for category, pattern in patterns.items():
        if pattern.match(link):
            link_dict["link"] = link
            link_dict["type"] = category
            news_links.append(link_dict)
            break
        
# Remove duplicates
unique_links = {}
for d in news_links:
    link = d["link"]
    if link not in unique_links:
        unique_links[link] = d
    else:
        existing_entry = unique_links[link]
        if existing_entry["publisher"] is None and d["publisher"] is not None:
            unique_links[link] = d
            
news_links = list(unique_links.values())

with open(str(datetime.now()) + "_date.json", "w") as json_file:
    json.dump(news_links, json_file, default=str)

driver.quit()
