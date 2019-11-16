def scrape():
    from splinter import Browser
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Get news data
    url_nasa = 'https://mars.nasa.gov/news/'

    browser.visit(url_nasa)
    for y in range(1):
        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
        # Retrieve all elements that contain book information
        news_title = soup.find('div',class_='content_title').a.text
        news_p = soup.find('div',class_='article_teaser_body').get_text()

    # Get featured image    
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url_jpl)
    browser.click_link_by_id('full_image')
    try:
        for y in range(1):
            # HTML object
            html = browser.html
            # Parse HTML with Beautiful Soup
            soup = BeautifulSoup(html, 'html.parser')
            # Retrieve all elements that contain book information
            featured_image_url_piece = soup.find('img',class_='fancybox-image')['src']
            featured_image_url = 'https://www.jpl.nasa.gov' + str(featured_image_url_piece)
    except TypeError:
        featured_image_url = 'https://www.jpl.nasa.gov' + '/spaceimages/images/mediumsize/PIA16883_ip.jpg'

    # Get twitter weather report
    url_twitter = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(url_twitter)
    for y in range(1):
        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
        # Retrieve all elements that contain book information
        mars_weather = soup.find('div',class_='js-tweet-text-container').p.text

        

    # Get facts
    url_facts = 'https://space-facts.com/mars/'

    tables = pd.read_html(url_facts)
    df = tables[0]

    html_table = df.to_html()


    # Get four images
    url_astro = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url_astro)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    images = soup.find_all('a', class_='itemLink product-item')
    images = images[1::2]

    hemisphere_image_urls_dict = {}
    hemisphere_image_urls = []
        
    for image in images:
        #print(image['href'])
        browser.visit('https://astrogeology.usgs.gov'+str(image['href']))
        
        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
        
        image_url = soup.find('div',class_='downloads').ul.li.a['href']
        image_title = soup.find('h2',class_='title').text
        hemisphere_image_urls_dict['title']=image_title
        hemisphere_image_urls_dict['img_url']=image_url
        
        hemisphere_image_urls.append(hemisphere_image_urls_dict)
        hemisphere_image_urls_dict = {}

    results_dict={}
    results_dict['news_title']=news_title
    results_dict['news_p']=news_p
    results_dict['featured_image_url']=featured_image_url
    results_dict['mars_weather']=mars_weather
    results_dict['html_table']=html_table
    results_dict['hemisphere_image_urls']=hemisphere_image_urls
    browser.quit()
    return(results_dict)
        
#scrape()