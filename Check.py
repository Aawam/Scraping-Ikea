from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import pandas as pd
import time

#Starting Iniialize code
browser = webdriver.Chrome()

browser.get("https://www.ikea.co.id/in")

button = browser.find_element(By.TAG_NAME, 'aside')\
    .find_element(By.CLASS_NAME, 'sidebar-wrapper')\
    .find_element(By.CLASS_NAME, 'sidebar-menu-main-heading')\
    .find_element(By.TAG_NAME, 'b')
button.click

time.sleep(5)

button2 = browser.find_element(By.TAG_NAME, 'aside')\
    .find_element(By.CLASS_NAME, 'sidebar-wrapper')\
    .find_element(By.CLASS_NAME, 'sidebar-menu.products')\
    .find_element(By.TAG_NAME, 'b')
button2.click()

if button2.is_enabled():
    print("Correct")
else:
    print("Wrong")

time.sleep(5)

html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

products = soup.find("body")\
    .find("div", id = 'sidenavWrapper')\
    .find("aside", id ='sidebar-main-menu')\
    .find("div", class_='sidebar-wrapper')\
    .find("div", class_='sidebar-menu ra')

if products:
    print("Correct")
else:
    print("Wrong")

print(products)

browser.quit()