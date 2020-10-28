from splinter import Browser
from bs4 import BeautifulSoup
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser(init_browser)
    listings = []


    ### 1st site visit
    # Pull latest news title and paragraph
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    
    # pause to visit website
    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('li', class_='slide')
    result = results[0]
    
    latest_title = result.find('div', class_ = "content_title").text
    latest_paragraph = result.find('div', class_ = "article_teaser_body").text


    ### 2nd site visit
    # Pull Featured Image
    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_img)
    
    # pause to visit website
    time.sleep(3)

    browser.click_link_by_partial_text('FULL IMAGE')
    # pause to visit website
    time.sleep(3)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('img', class_ = "fancybox-image")
    result = results[0]['src']

    featured_image_url = "https://www.jpl.nasa.gov" + result


    ### 3rd site visit
    # Pull Table/Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    html_table = df.to_html()

    ### 4th site visit: Mars Hemispheres
    # Pull Four Images and Titles
    main_url = 'https://astrogeology.usgs.gov'
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # pause to visit website
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', class_ = "item")
    
    # empty list of urls
    hemisphere_image_urls=[]

        # create dictionary of title and urls
    for result in results:
        # Pull title
        title = result.h3.text
        # Pull Url
        url = result.find('a', class_='itemLink product-item')['href']
        # Visit new url
        browser.visit(main_url + url)
        # Parse new url
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        # Pull url for large image
        url = soup.find('img', class_='wide-image')['src']
        # Obtain full link for large image
        url = main_url + url
        # Append
        hemisphere_image_urls.append({'Title':title, 'img_url':url})
    
    scrape_dict = {}
    
    scrape_dict["news_title"] = latest_title
    scrape_dict["featured_image"] = featured_image_url
    scrape_dict["table_html"] = html_table
    scrape_dict["title_img_list"] = hemisphere_image_urls

    return scrape_dict