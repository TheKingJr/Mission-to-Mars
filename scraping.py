#!/usr/bin/env python
# coding: utf-8

# In[12]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemi_image(browser),
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

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

# 2. Create a list to hold the images and titles.


def hemi_image(browser):
    hemisphere_image_urls = []
    
    try:
        # 3. Write code to retrieve the image urls and titles for each hemisphere.
        for i in range(4):
    
            # 1. Use browser to visit the URL 
            url = 'https://marshemispheres.com/'
            browser.visit(url)
    
            # Parse the resulting html with soup
            html = browser.html
            hemi_soup = soup(html, 'html.parser')
            hemi_title_elem = hemi_soup.find_all('div', class_='description')[i]
    
            # Obtaining the hemisphere title
            hemi_title = hemi_title_elem.find('a', class_='itemLink product-item').get_text(separator='\n').strip()
            hemi_title
    
            # Parse to find the thumbnail image and finding the href
            # I couldn't find a botton for browser to click into
            # Instead I found the href and built another url for browser to visit
            hemi_href = hemi_title_elem.find('a', class_='itemLink product-item')['href']
            hemi_url = f'https://marshemispheres.com/{hemi_href}'
            hemi_url

            # Onto the next step by getting browser to visit the url from above
            sample_image_elem = browser.visit(hemi_url)
    
            # Parsing the new url link/ I don't know if this is incorrect but it worked
            html = browser.html
            sample_soup = soup(html, 'html.parser')
            sample_elem = sample_soup.find('div', class_='downloads') # Setting up to get image url 
            sample_target = sample_elem.find('a', href=True)['href'] # Getting href to build url
            sample_url = f'https://marshemispheres.com/{sample_target}'
            sample_url
    
            hemisphere_image_urls.append({'img_url': sample_url, 'title': hemi_title})
    
    except AttributeError:
        return None
    
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

