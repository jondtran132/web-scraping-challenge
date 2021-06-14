from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_info():
    
    #Nasa Mars News
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url1 = 'https://redplanetscience.com/'
    browser.visit(url1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title = soup.find("div", class_="content_title").get_text()
    news_p = soup.find("div", class_="article_teaser_body").get_text()

    browser.quit()

    #-----------------------------------------------------------
    #JPL Mars Space Images - Featured Image
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    image_end = soup.find("img", class_="headerimage")["src"]
    image_url = url2+image_end

    browser.quit()

    #----------------------------------------------------------
    #Mars Facts
    url3 = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url3)


    df = tables[0]
    df.columns = df.iloc[0]
    df = df.drop(df.index[0]).set_index("Mars - Earth Comparison")
    html_table = df.to_html().replace('\n','')

	#----------------------------------------------------------
    #Mars Hemispheres
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)

    hemisphere_image_urls = []

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    all_links = soup.find_all('div', class_='description')

    for item in all_links:

        html = browser.html
        soup = BeautifulSoup(html, "html.parser")

        link = item.find('a')['href']
        title = item.find('h3').get_text()

        browser.links.find_by_partial_text(title).click()

        html = browser.html
        soup = BeautifulSoup(html, "html.parser")

        image_url_end = soup.find('div', class_='downloads').find('a')['href']

        browser.links.find_by_partial_text('Back').click()

        hemisphere_image_urls.append({'title':title, 'img_url':url4+image_url_end})

    browser.quit()
    
    #--------------------------------------------------------------------
    #Store All Variables
    info = {
        'news_title':news_title,
        'news_p':news_p,
        'image_url':image_url,
        'html_table':html_table,
        'hemispheres':hemisphere_image_urls
    }
    
    return info