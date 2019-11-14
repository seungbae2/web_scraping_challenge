from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd

def init_browser():
	executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
	return Browser("chrome", **executable_path, headless=False)


def scrape():
	browser = init_browser()

	# NASA Mars News
	url_news = 'https://mars.nasa.gov/news/'
	browser.visit(url_news)
	html_news = browser.html
	soup_news = BeautifulSoup(html_news, 'html.parser')

	news_title = soup_news.find('div', class_ = 'content_title').text
	news_p = soup_news.find('div', class_ = 'article_teaser_body').text

	# JPL Mars Space Images - Featured Image
	url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(url_img)
	html_img = browser.html
	soup_img = BeautifulSoup(html_img, 'html.parser')

	featured_image_url = soup_img.find('img', class_ = 'thumb')['src']
	featured_image_url = 'https://www.jpl.nasa.gov'+ featured_image_url

	# Mars weather
	url_weather = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(url_weather)
	html_weather = browser.html
	soup_weather = BeautifulSoup(html_weather, 'html.parser')

	mars_weather = soup_weather.find('div', class_ = 'js-tweet-text-container').text

	# Mars Facts
	url_fact = 'https://space-facts.com/mars/'
	tables = pd.read_html(url_fact)
	df = tables[0]
	df.columns = ['description','value']
	df = df.set_index('description')
	mars_fact = df.to_html()
	mars_fact = mars_fact.replace('\n', '')
	mars_fact


	# Mars Hemispheres
	url_hem = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(url_hem)
	html_hem = browser.html
	soup_hem = BeautifulSoup(html_hem, 'html.parser')

	image_urls = soup_hem.find_all('div', class_="item")

	hemisphere_image_urls = []

	for url in image_urls:
	    browser.visit('https://astrogeology.usgs.gov' + url.a['href'])
	    html = browser.html
	    soup = BeautifulSoup(html, 'html.parser')
	    
	    high_res_link = soup.find('li').a['href']
	    title = soup.find('h2').text
	    hemisphere_image_urls.append({'title': title, 'img_url': high_res_link})


	mars_data = {
	 	'news_title': news_title,
	 	'news_p': news_p,
	 	'featured_image_url': featured_image_url,
	 	'mars_weather': mars_weather,
	 	'mars_fact': mars_fact,
	 	'hemisphere_image_urls': hemisphere_image_urls
	 }

	browser.quit()

	return mars_data
