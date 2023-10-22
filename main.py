from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

# Initialize ChromeDriver
service = Service(executable_path='/usr/bin/chromedriver')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Open Google
driver.get("https://www.google.com")

# Find the search box using its name attribute value
search_box = driver.find_element_by_name("q")

# Type in the search query
search_box.send_keys("Hello, world!")

# Submit the query (like hitting 'Enter' key)
search_box.send_keys(Keys.RETURN)

# Wait for search results to load
time.sleep(2)

# Print the title of the current page
print("Title of the page is: ", driver.title)

# Close the browser
driver.quit()
