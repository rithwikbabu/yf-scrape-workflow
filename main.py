from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re

# Function to load existing links
def load_existing_links(filename):
    try:
        with open(filename, 'r') as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()

# Initialize ChromeDriver
service = Service(executable_path='/usr/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)

# Navigate to Yahoo Finance News
driver.get('https://finance.yahoo.com/news/')

# Sleep and scroll settings
SCROLL_COUNT = 30
time.sleep(2)

# Scroll 30 times
for _ in range(SCROLL_COUNT):
    driver.execute_script("window.scrollTo(0, 9999999);")  # Scroll to the very bottom
    time.sleep(5)  # Give it ample time to load new content

# Scrape after scrolling
news_boxes = driver.find_elements(By.CLASS_NAME, 'Cf')
pattern = re.compile(r'https://finance\.yahoo\.com/news/.+\.html')

# Load existing links from file into a set
unique_links = load_existing_links('links.txt')

# Update set with newly scraped links
for box in news_boxes:
    link = box.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    if pattern.match(link):
        unique_links.add(link)

# Save updated set back to file
with open('links.txt', 'w') as f:
    for link in unique_links:
        f.write(f"{link}\n")

# Close the driver
driver.quit()
