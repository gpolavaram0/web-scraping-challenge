from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

print("running program...")



def scrape():

    from bs4 import BeautifulSoup
    import requests
   
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import pandas as pd
    import time

    #NASA Mars News (BeautifulSoup)------------------------------------------------------------------

    #pulling html from webpage with soup
    response = requests.get("https://mars.nasa.gov/#")
    src = response.content
    soup = BeautifulSoup(src, "html.parser")

    #print(soup.prettify)

    #pulling first article webpage out
    media_feature_title = soup.find(class_="media_feature_title")
    news_title = media_feature_title.a.text

    #pulling paragraph text of first article out
    description  = soup.find(class_="description")
    news_p = description.text

    #printing variables
    print(news_title)
    print(news_p)

    #storing retrieved values into dict for flask part
    scraper_dict = {"news_title":news_title,"news_p":news_p,}

    #JPL Mars Space Images - Featured Image------------------------------------------------------------------
    browser = webdriver.Chrome(r'D:\Users\Goutham\Documents\BOOTCAMP\mission to mars - web scraping\chromedriver_win32\chromedriver')
    browser.get("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")

    #using selenium to retrieve url instead of splinter
    image_partial_url = browser.find_element_by_xpath("//a[@class='button fancybox']").get_attribute("data-fancybox-href")
    base_partial_url = browser.find_element_by_id('jpl_logo').get_attribute("href")

    #finding both halves of url and removing a slah from base url
    featured_image_url = base_partial_url[:-1] + image_partial_url
    print(featured_image_url)

    #Updating dict with new values
    scraper_dict.update({"featured_image_url":featured_image_url})

    browser.close()

    time.sleep(10)

    #Mars Facts (table scraping with Pandas)------------------------------------------------------------------
    mars_table= pd.read_html('https://space-facts.com/mars/')

    #mars_table is HTML string
    mars_table

    #mars table df
    df_mars_table = mars_table[1]
    df_mars_table.set_index("Mars - Earth Comparison", inplace = True)
    print(df_mars_table)

    #Updating dict with new values
    scraper_dict.update({"featured_image_url":featured_image_url})

    #converting df to dict
    dict_mars_table = df_mars_table.to_dict()

    #Updating dict with new values
    scraper_dict.update(dict_mars_table)



    #Mars Hemispheres------------------------------------------------------------------
    
    # driver = webdriver.Firefox(executable_path=r'D:\Users\Goutham\Documents\BOOTCAMP\mission to mars - web scraping\geckodriver-v0.26.0-win64\geckodriver')
    driver = webdriver.Chrome(r'D:\Users\Goutham\Documents\BOOTCAMP\mission to mars - web scraping\chromedriver_win32\chromedriver')
    driver.get("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")

    image_elements = driver.find_elements_by_class_name("thumb")
    image_elements_index = list(range(len(image_elements)))

    time.sleep(10)

    #dictionary for links and titles as keys and values
    hemisphere_image_urls = []

    #counter for separating dict entries for hemispheres
    counter = 0
    
    

    for element in image_elements_index:
        time.sleep(20)
        #resetting elements lists everytime for links
        image_elements = driver.find_elements_by_class_name("thumb")
        image_elements[element].click()

        time.sleep(10)
        counter += 1

        #pull the title and links with Selenium methods
        original_url = driver.find_element_by_link_text('Original').get_attribute("href")
        hemisphere_title = driver.find_element_by_xpath("//h2[@class = 'title']")

        #store links and titles in homework defined variables
        img_url = original_url
        title = hemisphere_title.text[:-9]

        #storing into a dictionary
        new_dict = {}
        new_dict["title" + str(counter)] = title
        new_dict["img_url" + str(counter)] = img_url

        hemisphere_image_urls.append(new_dict)
        
        #back to loop back to homepage to loop through all hemisphere pages
        time.sleep(5)
        driver.back()

    #close browser
    driver.close()

    for dict in hemisphere_image_urls:
        scraper_dict.update(dict)

    # print(hemisphere_image_urls) 
    

    
    


    print(scraper_dict)
    return scraper_dict

scrape()
    




