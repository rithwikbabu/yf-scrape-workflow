from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import time
import json

#====================================
#  To update the scraped_text.json file, all that needs to be done is run update(). This will run through all of links.txt, and scrape any articles that it has not already
#====================================
#	Note that since this script doesn't remove the links, any dead links will be re-scraped every time, this will slowly cause the script to take longer and longer, might be beneficial to delete/clear the links.txt file after scraping
#====================================

# Function to load existing links
def load_existing_links(filename):
    try:
        with open(filename, 'r') as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()

#Return the list containing elements that exist only in list2 and not in list1
def list_inverse(list1, list2):
	return [item2 for item2 in list2 if item2 not in list1]

def load_existing_articles(filename):
	try:
		with open(filename, 'r') as f:
			arts = json.load(f)
			links = set(art['link'] for art in arts)
			return links

	except FileNotFoundError:
		return set()

def scrape_content(link, driver, save_path):
	#Loading initial page in "classic" version
	driver.get(link+'?.neo_opt=0')
	print('Loaded Site')

	#Clicking story cotinues until we've loading the full thing, 
	#always clicking the most recent button that hasn't been clicked yet
	cont_buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'Story continues')]")
	clicked = []
	while len(list_inverse(clicked, cont_buttons)) > 0:
		button = list_inverse(clicked, cont_buttons)
		button[0].click()
		clicked.append(button[0])

		# time.sleep(2)
		cont_buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'Story continues')]")
	print('Opened Full Article')

	# time.sleep(1)

	#Getting main content
	contents = driver.find_elements(By.CLASS_NAME, 'caas-content-wrapper')
	if len(contents) > 0:
		content = contents[0]
	else:
		print('Article not found, Skipping')
		return
	
	article_data = {}

	#Getting the title
	title = driver.find_element(By.CLASS_NAME, 'caas-title-wrapper').find_element(By.XPATH, './/h1').text
	article_data['title'] = title

	#link
	article_data['link'] = link

	#Getting time
	publish_date = content.find_element(By.CLASS_NAME, 'caas-attr-time-style').find_element(By.XPATH, './/time').get_attribute('datetime')
	article_data['date'] = publish_date
	
	#Getting text
	text = ''
	paragraphs = content.find_element(By.CLASS_NAME, 'caas-body').find_elements(By.XPATH, './/p')
	for paragraph in paragraphs:
		text = f"{text}\n\n{paragraph.text}"
	article_data['text'] = text

	#Getting related stocks
	related_stocks = set()
	related_stock_elements = driver.find_elements(By.CLASS_NAME, 'xray-entity-title-link')
	#print(related_stock_elements)
	for elem in related_stock_elements:
		#print(elem.text)
		if elem.text != '':
			related_stocks.add(elem.text)
	article_data['stocks'] = list(related_stocks)

	print('Got Data')

	# Read existing data from the file
	try:
		with open(save_path, 'r') as file:
			data = json.load(file)
	except:
		print('Not able to open links file to read')
		return

	# Append the new dictionary to the existing data
	data.append(article_data)

	# Write the updated data back to the file
	try:
		with open(save_path, 'w') as file:
			json.dump(data, file, indent=4)
	except:
		print('Not able to open file to save')
		return

	print('Saved Data')

def update(driver, save_path, link_path, n=5):
	#Getting the full list of links and scraped links so we only scrape the new ones
	links = load_existing_links(link_path)
	scraped_links = load_existing_articles(save_path)
	for link in links:
		if n==0:
			break

		if not link in scraped_links: 
			print('Begining to scrape {}'.format(link))
			scrape_content(link, driver, save_path)
			scraped_links.add(link)			

			n -= 1

#Setting up the web scraper driver itself to pass into the internal scraper
service = Service(executable_path='/usr/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument(
	"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
options.add_argument("--log-level=3")
options.add_argument("--headless")
driver = webdriver.Chrome(options=options, service=service)

with open("scraped_text.json", 'r') as file:
	backup = json.load(file)

update(driver, 'scraped_text.json', 'links.txt')

try:
	with open("scraped_text.json", 'r') as file:
		scraped_text = json.load(file)
except:
	print('Save error in srapaced_text.json, reverting to backup')
	
	with open("scraped_text.json", 'w') as file:
		json.dump(backup, file, indent=4)