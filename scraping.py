# Import Splinter, BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import requests
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    
    # Initiate the headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = mars_hemispheres(browser)
  
    # Run all scraping functions and store retults in dictionary (not sure if nested dictionary is right)
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemisphere_image_title": hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')  
        # use the parent element to find the first a tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text() 
        # use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()  

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    
    # ## JPL Space Images Featured Image

    # Visit URL
    url = 'https:spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem=browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


def mars_facts():

    # Get Mars facts and put into a DataFrame

    # Add try/except for error handling
    try:
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]  

    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    # Convert DataFrame to HTML format, add boostrap
    return df.to_html()


def mars_hemispheres(browser):

    # ## Scrape High-Resolution Mars' Hemisphere Images and Titles

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    response=requests.get(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    img_soup = soup(response.text, 'html.parser')
    
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

    # Return dictionary of images and titles of Mars hemispheres
    return hemisphere_image_urls

if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())