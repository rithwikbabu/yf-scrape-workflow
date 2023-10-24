from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re

# Initialize ChromeDriver
service = Service(executable_path='/usr/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)

driver.get(f'https://finance.yahoo.com/news/')

news_boxes = driver.find_elements(By.CLASS_NAME, 'Cf')
pattern = re.compile(r'https://finance\.yahoo\.com/news/.+\.html')

# To hold unique links
unique_links = set()

for box in news_boxes:
    link = box.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    if pattern.match(link):
        unique_links.add(link)

# Save unique links to a file
with open('links.txt', 'w') as f:
    for link in unique_links:
        f.write(f"{link}\n")

driver.quit()
