# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import requests

# Setup executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Setup the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# Assign the title and summary
slide_elem.find('div', class_='content_title')

# use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# Visit URL
url = 'https:spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem=browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Table of Facts

# Create pandas df
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# Convert DataFrame to HTML
df.to_html()


# # D1: Scrape High-Resolution Mars' Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
response=requests.get(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
img_soup = soup(response.text, 'html.parser')
print(img_soup.prettify())

# results returned as an interable list
img_link=img_soup.find_all('div', class_="item")

# Create for loop to iterate through list
for img in img_link:
    ref=img.find('a', class_="result-title")
    hem_link=img.a['href']
    img_url = f'https://marshemispheres.com/{hem_link}'
    browser.visit(img_url)
    html = browser.html
    img_soup2 = soup(html, 'html.parser')
    hem_title = img_soup2.find("h2", class_="title").get_text()
    hem_full_img = img_soup2.find("img", class_="wide-image").get("src")
    hem_img_url = f'https://marshemispheres.com/{hem_full_img}'
    hemispheres={"img_url":hem_img_url, "title":hem_title}
    hemisphere_image_urls.append(hemispheres)
    browser.back()


# Quit the browser
browser.quit()
