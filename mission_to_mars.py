#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


# In[2]:


#NASA Mars News (BeautifulSoup)

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


# In[3]:


#JPL Mars Space Images - Featured Image
browser = webdriver.Chrome(r'D:\Users\Goutham\Documents\BOOTCAMP\mission to mars - web scraping\chromedriver_win32\chromedriver')
browser.get("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")

#using selenium to retrieve url instead of splinter
image_partial_url = browser.find_element_by_xpath("//a[@class='button fancybox']").get_attribute("data-fancybox-href")
base_partial_url = browser.find_element_by_id('jpl_logo').get_attribute("href")

#finding both halves of url and removing a slah from base url
featured_image_url = base_partial_url[:-1] + image_partial_url
print(featured_image_url)


# In[4]:


#Mars Facts (table scraping with Pandas)
mars_table= pd.read_html('https://space-facts.com/mars/')

#mars_table is HTML string
mars_table

#mars table df
df_mars_table = mars_table[1]
df_mars_table


# In[5]:


#Mars Hemispheres

driver = webdriver.Chrome(r'D:\Users\Goutham\Documents\BOOTCAMP\mission to mars - web scraping\chromedriver_win32\chromedriver')
driver.get("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")

image_elements = driver.find_elements_by_class_name("thumb")
image_elements_index = list(range(len(image_elements)))

#dictionary for links and titles as keys and values
hemisphere_image_urls = []

for element in image_elements_index:
    #resetting elements lists everytime for links
    image_elements = driver.find_elements_by_class_name("thumb")
    image_elements[element].click()

    #pull the title and links with Selenium methods
    original_url = driver.find_element_by_link_text('Original').get_attribute("href")
    hemisphere_title = driver.find_element_by_xpath("//h2[@class = 'title']")

    #store links and titles in homework defined variables
    img_url = original_url
    title = hemisphere_title.text[:-9]

    #storing into a dictionary
    new_dict = dict()
    new_dict["title"] = title
    new_dict["img_url"] = img_url

    hemisphere_image_urls.append(new_dict)

    #back to loop back to homepage to loop through all hemisphere pages
    driver.back()

#close browser
driver.close()

print(hemisphere_image_urls)


# In[6]:


driver = webdriver.Chrome(r'D:\Users\Goutham\Documents\BOOTCAMP\mission to mars - web scraping\chromedriver_win32\chromedriver')
driver.get("https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced")

xpath_test = driver.find_element_by_xpath("//h2[@class = 'title']")


# In[7]:


print(xpath_test.text)


# In[ ]:





# In[ ]:





# In[8]:


image_partial_url.get_attribute("data-fancybox-href")


# In[ ]:




