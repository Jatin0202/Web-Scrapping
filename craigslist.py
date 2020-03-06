from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import urllib.request


#driver = webdriver.Chrome('/home/jatin/WebDriver/chromedriver')


class CraiglistScraper(object):
	def __init__(self, location, postal, max_price, radius):
		self.location = location 
		self.postal = postal 
		self.max_price = max_price 
		self.radius = radius 

		self.url = f"https://{location}.craigslist.org/search/sss?/search_distance={radius}&postal={postal}&max_price={max_price}"
		self.driver = webdriver.Chrome('/home/jatin/WebDriver/chromedriver')
		self.delay = 3

	def load_craiglist_url(self):
		self.driver.get(self.url)
		try:
			wait = WebDriverWait(self.driver, self.delay)
			wait.until(EC.presence_of_element_located((By.ID,"searchform")))
			print("Page is ready")
		except TimeoutException:
			print("Loading too much time")	
	
	def extract_post_information(self):
		all_post = self.driver.find_elements_by_class_name("result-row")
		post_title_list = []
		for post in all_post:
			title = post.text.split('$')

			if title[0] == "":
				title = title[1]
				
			else:
				title = title[0]
				
				
			title = title.split("\n")
			price=title[0]
			title =title[-1]
			title = title.split(" ")	
			month = title[0]
			day = title[1]
			date = month + " " + day
			title = ''.join(title[2:])
			post_title_list.append(post.text)

			print("Price : " +price)
			print("Title : " +title)	
			print("Date  : " +date)
		return post_title_list

	def extract_post_urls(self):
		url_list = []
		html_page = urllib.request.urlopen(self.url)
		soup = BeautifulSoup(html_page, "html.parser")
		for link in soup.find_all("a", {"class" : "result-image gallery"}):
			print(link.get('href'))
			url_list.append(link.get('href'))
		return url_list

	def quit(self):
		self.driver.close()
		

location = "sfbay"
postal = "94201"
max_price = "500"
radius = "5"

scraper = CraiglistScraper(location , postal , max_price , radius)
scraper.load_craiglist_url()
scraper.extract_post_information()
scraper.extract_post_urls()
scraper.quit()