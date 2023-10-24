from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re

# Initialize ChromeDriver
service = Service(executable_path='/usr/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)

driver.get(f'https://finance.yahoo.com/news/')

news_links = driver.find_elements(By.XPATH, '//a[contains(@href, "https://finance.yahoo.com/news/")]')

# Extract and store the links in a list
links_list = []
for link in news_links:
    href = link.get_attribute('href')
    if href:
        links_list.append(href)

# Write the links to a file
with open('links.txt', 'w') as file:
    for link in links_list:
        file.write(link + '\n')

driver.quit()
