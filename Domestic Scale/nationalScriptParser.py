from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import re


driver = webdriver.Chrome(executable_path = r'C:\\Users\\Abdullah\\Downloads\\chromedriver_win32\\chromedriver.exe')
#driver  = webdriver.PhantomJS(executable_path = r'C:\\Users\\Abdullah\\Downloads\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')

url = 'https://www.healthgrades.com/usearch?what=Family%20Medicine&entityCode=PS305&searchType=PracticingSpeciality&spec=null&where=AL'

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
 'LA', 'ME', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN', 'MS',
  'MO', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

cols = ['Name', 'Rating']
entries = []

def openBrowser():
	driver.get(url)
	driver.maximize_window()

def closeBrowser():
	driver.quit()

def getInfo():
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'uCard__name')))
			WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'uCard__rating ')))

			x = 1
			names = driver.find_elements_by_class_name('uCard__name')
			for name in names:
				#ratingStr = '#card-carousel-search > div:nth-child(2) > ul > li:nth-child(' + str(x) + ') > div > div > div > div:nth-child(1) > div > div.card-column__details > div.uCard__rating >'
				try:
					ratingStr = '//*[@id="card-carousel-search"]/div[2]/ul/li[' + str(x) + ']/div/div/div/div[1]/div/div[2]/div[2]/span[1]'
					rating = driver.find_element_by_xpath(ratingStr)
				#rating = driver.find_element_by_css_selector(ratingStr) 
					rateValue = re.findall(r'\d+\.*\d*',rating.get_attribute('aria-label'))
				#print(rateValue)
					entries.append([name.text, rateValue[0]])
				except:
					print('shitty html code took too long to load')
					pass
				x += 1
		except TimeoutException:
			print('Shitty HTML took too long to load')
		print('Parsing Finished')
		updateCSV()
def nextPage():
	nextpage = driver.find_element_by_css_selector('a.shuffle-next-hand.active')
	nextpage.click()

def parsePages(x):
	y = 0
	while(y < x):
		print('Page ', y + 1)
		getInfo()
		nextPage()
		y += 1

def openLocation(stateAB):
	location_name = stateAB
	location = driver.find_element_by_id('uSearch-search-location-selector-child')
	location.send_keys(location_name)
	location.send_keys(Keys.ENTER)

	restriction = driver.find_element_by_css_selector('#usearch-container > div > div.uSearch-container > div.locked-left > form > div.refiner__filter-pallet > div.filter-pallet > ul > li:nth-child(4) > fieldset > div.filter-drawer__filter > div > div.filter__checkbox-filter > ul > li:nth-child(5) > div > label > span.faux-checkbox')
	restriction.click()

	number = driver.find_element_by_class_name('uSearch-title').text
	print("Number of Benficiaries:", number)
	number = int(int(number.split(' ')[0]) / 20)
	print("Number of pages to parse:", number)
	parsePages(number)

def initCSV():

	df = pd.DataFrame(columns = ['Name', 'Rating'])
	df.to_csv('Alabama-Benficiaries.csv', index=False)
	print('CSV Initialized')

def updateCSV():
	df = pd.DataFrame(entries, columns = cols)
	df = df.sort_values(by = 'Rating', ascending = True)
	df.to_csv('Alabama-Benficiaries.csv', mode = 'a', header = False, index = False)

	print('CSV Updated')
def finalizeCSV():
	print(df.shape)

	df = df.drop(df[(df.Rating < 4.0) & (df.Rating > 2.5)].index)
	df = df.drop(df[(df.Rating == 0)].index)	
	#df = df[df.Rating <= 2.5 and df.Rating >=4]

	#df.to_csv('Alabama-Benficiaries.csv', index=False)
	#df.to_csv('plzWORK.csv', index=False)

	print(df.shape)

if __name__ == '__main__':
	openBrowser()
	#for x in states:
		#openLocation(x)
	initCSV()
	openLocation('AL')

	#openLocation('AK')
	closeBrowser()