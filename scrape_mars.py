import time
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": '/app/.chromedriver/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    all_info ={}


    #NASA Info
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    time.sleep(1)
    nasa_html = browser.html
    nasa_soup = BeautifulSoup(nasa_html, 'lxml')

    news_title = nasa_soup.find('div', class_='content_title').text
    news_p = nasa_soup.find('div', class_='article_teaser_body').text
    nasa_news = [news_title, news_p]
    # time.sleep(1)
 
    #JPL Feature Image Extraction
    #Side note: I noticed that without a pause between each clicks, there are sometimes issue with interacting with the page.
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(1)
    browser.click_link_by_partial_href('/spaceimages/images/largesize/')

    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'lxml')


    jpl_image_url = jpl_soup.find('img')['src']
    # time.sleep(1)

    #Twitter Status Update
    twit_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twit_url)
    twit_html = browser.html
    twit_soup = BeautifulSoup(twit_html, 'lxml')

    mars_weather = twit_soup.find('div', class_='js-tweet-text-container').text
    # time.sleep(1)
    
    #Space facts Table
    space_url = "https://space-facts.com/mars/"
    tables = pd.read_html(space_url)
    df=tables[0]
    df.columns = ["Descriptions", "Values"]
    df.set_index('Descriptions', inplace=True)
    html_table = df.to_html()
    html_table.replace('\n', '')
    df.to_html('table.html')
    time.sleep(1)


    #USGS image URL and TItle
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)
    time.sleep(1)
    usgs_html = browser.html
    usgs_soup = BeautifulSoup(usgs_html, 'lxml')
    images = usgs_soup.find_all('div', class_='item')

    pic_list = []



    for image in images:
        group = image.find('div', class_='description')
        title = group.find('h3').text

        
        pic = image.find('a', class_='itemLink product-item')['href']
        temp_url = 'https://astrogeology.usgs.gov'
        image_url = f"{temp_url}{pic}"
        browser.visit(image_url)
        time.sleep(1)
        

        #reach the destination page and use soup again to extract html text.
        html = browser.html
        soup=BeautifulSoup(html, "lxml")
        downloads = soup.find("div", class_="downloads")
        img_url = downloads.find("a")["href"]
        
        pic_list.append({"title": title, "img_url": img_url})
        browser.visit(usgs_url)

    
    
    
    #Store all info into a python dictionary.
    all_info["nasa_news"] = nasa_news[0]
    all_info["nasa_paragraph"] = nasa_news[1]
    all_info["jpl_img"] = jpl_image_url
    all_info["twitter_status"] = mars_weather
    all_info["space_fact_table"] = html_table
    all_info["usgs_img"] = pic_list

    #Close the chrome driver browser
    browser.quit()
    return all_info 


        
