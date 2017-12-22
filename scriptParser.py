from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import re
import pandas as pd

driver = webdriver.Chrome('C:\\Users\\Abdullah\\Downloads\\chromedriver_win32\\chromedriver.exe')

url = 'https://www.healthgrades.com/usearch?what=Family%20Medicine&entityCode=PS305&searchType=PracticingSpeciality&spec=null&where=NE&state=NE'

cols = ['Name', 'Rating', 'Reviews']
entries = []

def openBrowser():
	driver.get(url)

def closeBrowser():
	driver.quit()

def getInfo():
	driver.implicitly_wait(10) #THIS WEBSITE's HTML SUCKS 
	pre = '//*[@id="card-carousel-search"]/div[2]/ul/li['
	suffix = ']/div/div/div/div[1]/div/div[2]/div[2]/span[1]'
	suffix2 = ']/div/div/div/div[1]/div/div[2]/h3'

	global entries
	x = 1
	while x < 21:
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'uCard__rating')))
		except TimeoutException:
			print('Shitty HTML took too long to load')

		rates = driver.find_elements_by_class_name('uCard__rating')
		for rate in rates:
			if x == 1:
				driver.implicitly_wait(5)
			try:
				driver.implicitly_wait(3)
				rateText = rate.text
			except:
				rateText = 'Leave a review'
			
			if rateText != 'Leave a review':
				url = pre + str(x) + suffix
				url2 = pre + str(x) + suffix2

				try:
					WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, url2)))
					#rating = driver.find_element_by_xpath(url)
					name = driver.find_element_by_xpath(url2)
					name = name.text
					name = name.split(',',1)[0][4:]
				except:
					print('Shitty HTML took too long to load')
					name = ''
				try:
					WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, url)))
					rating = driver.find_element_by_xpath(url)
					rateValue = re.findall(r'\d+\.*\d*', rating.get_attribute('aria-label'))
				except:
					print('Shitty HTML took too long to load')
					rating = ''

				#name = name.text
				#name = name.split(',',1)[0][4:]

				#try:
				if name and rating:
					print(name, rateValue[0], "\t Reviews:" + rateText[0:2])
					entries.append([name, float(rateValue[0]), float(rateText[0:2])])
				#except:
				#	pass

				x += 1
			else:
				x += 1
'''
		url = pre + str(x + 1) + suffix
		url2 = pre + str(x + 1) + suffix2
		try:
			rating = driver.find_element_by_xpath(url)
			name = driver.find_element_by_xpath(url2)
		except:			
			rating = driver.find_element_by_xpath('//*[@id="card-carousel-search"]/div[2]/ul/li[' + str(x+1) + ']/div/div/div/div[1]/div/div[2]/a/span[1]')
			name = driver.find_element_by_xpath(url2)

		#driver.implicitly_wait(3)
			#CHANGE THIS TO EXPLICIT TIMER

		#timeout = 3
		#try:
		#	element_present = EC.presence_of_element_located((By.XPATH, 'url'))
		#	WebDriverWait(driver, timeout).until(element_present)
		#except TimeoutException:
   		#	print("Timed out waiting for page to load")

		#print(name.text, rating.get_attribute('aria-label'))

		try:
			rateValue = re.findall(r'\d+\.*\d*', rating.get_attribute('aria-label'))
			name = name.text
			name = name.split(',',1)[0][4:]
			print(name, rateValue[0])

			entries.append([name, float(rateValue[0])])
		except:
			pass

		#global entries
		#entries.append([name, float(rateValue[0])])
'''
def nextPage():
	#nextpage = driver.find_element_by_xpath('//*[@id="card-carousel-search"]/div[2]/div/a[2]')
	nextpage = driver.find_element_by_css_selector('a.shuffle-next-hand.active')
	nextpage.click()

def parsePages(x):
	y = 0
	while(y < x):
		print('Page ', y + 1)
		getInfo()
		nextPage()
		y += 1

def loadCSV():
	df = pd.DataFrame(entries, columns = cols)

	df = df.sort_values(by = 'Rating', ascending = True)

	print(df.shape)

	df = df.drop(df[(df.Rating < 4.0) & (df.Rating > 2.5)].index)
	df = df.drop(df[(df.Rating == 0)].index)	
	#df = df[df.Rating <= 2.5 and df.Rating >=4]

	df.to_csv('Healthgrade Employees.csv', index=False)
	#df.to_csv('plzWORK.csv', index=False)

	print(df.shape)

if __name__ == '__main__':
	openBrowser()
	parsePages(61)
	closeBrowser()
	loadCSV()


'''
	#retrieves names
	posts = driver.find_elements_by_class_name('uCard__name')
	for post in posts:
		print(post.text)

	#retrieves number of reviews	
	rates = driver.find_elements_by_class_name('uCard__rating')
	for rate in rates:
		print(rate.text)
	
	#Full Details
	cards = driver.find_elements_by_class_name('card-column__details')
	for card in cards:
		print(card.text)
'''