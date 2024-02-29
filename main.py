from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
import time

"""
#Starting Iniialize code
browser = webdriver.Chrome()
browser.get("https://www.ikea.co.id/in/produk/perabot-kamar-mandi")
time.sleep(5)
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

max_page: list[BeautifulSoup] = soup.find("ul", class_='pagination mb-0')\
    .find_all("li", class_="page-item")
max_page_number = int(max_page[-2].find("a").get_text())

final_result = []

index = 1

for i in range(1, max_page_number + 1):
    print(f"Accessing page : {i}")
    try:
        database = soup.find("div", id ='product-list-component')\
            .find("div", class_='productList-content d-flex flex-wrap')
        data = database.find_all("div", class_='col-6 col-md-4 col-lg-3 p-0 itemBlock')
        
        for item in data:
            #Scraping Data Header
            product = item.find("div", class_='card')
            link = product.find("div", class_='d-flex flex-row').find("a").get("href")
            final_link = (f'https://www.ikea.co.id{link}')
            response = requests.get(final_link)
            soup_link = BeautifulSoup(response.content, 'html.parser')
            #description access
            head = soup_link.find("div", class_='row item_detail_information clearfix')
            desc_access = head.find("div", class_='col-12 col-sm-12 col-md-5 col-lg-5 col-xl-4 product-box-wrap mt-4 mt-md-0')\
                .find("div", class_='itemInfo')
            name = desc_access.find("h1")\
                .find("div", class_='d-flex flex-row').get_text(strip=True)
            short_desc = desc_access.find("h1")\
                .find("span", class_='itemFacts font-weight-normal').get_text(strip=True)
            price = desc_access.find("div", class_='itemPrice-wrapper')\
                .find("span", class_='currency').next_sibling.get_text(strip=True)
            final_price = (f"IDR {price}")
            purchased = desc_access.find("p", class_='partNumber').get_text(strip=True)\
                .replace(" orang telah membeli produk ini", " Purchased")
            #additional access
            prod_details = soup_link.find("div", id='modal-product-details')\
                .find("div", class_='card')\
                .find("div", class_='card-body')
            num_article = prod_details.find("div", class_='partNumber my-2 d-inline-flex flex-column')\
                .find("span", class_='item-code')\
                .get_text(strip=True)
            long_desc = prod_details.find("div", class_='product-desc-wrapper mb-4')\
                .find("p").get_text(strip=True)
            material = prod_details.find("div", class_='modal-accordeon mt-5')\
                .find("div", id="materials-details")\
                    .find("div", class_="mb-3")\
                        .get_text(strip=True)\
                        .replace('<br>', ' \t')\
                        .replace('</strong>', ' ')
            try:
                advantage = prod_details.find("div", class_='modal-accordeon mt-5')\
                    .find("div", id='benefits')\
                    .find("div", class_='card-body')\
                    .find_all('p')
                final_advantage = ' '.join(p.get_text(strip=True) for p in advantage)
            except:
                final_advantage = ("This product whether doesn't have benefits or the writer just lazy to write it down")
            #additional access 2
            measurements = soup_link.find("div", id='modal-measurements')\
                .find("div", class_='card')\
                .find("div", class_='card-body')\
                .find("div", class_='mb-3')\
                .find("tbody")\
                .find_all("td")
            final_measurements = ' '.join(m.get_text(strip=True) for m in measurements)
            
            #Result_Product
            result = {
                "No" : index,
                "Name" : name,
                "Link" : final_link,
                "No Article" : num_article,
                "Short desc" : short_desc,
                "Long desc" : long_desc,
                "Advantage" : final_advantage,
                "Material" : material,
                "Measurements" : final_measurements,
                "Price" : final_price,
                "Number Purchased" : purchased 
            }
            
            final_result.append(result)
            
            print(f"---This is content no {index}----")
            index += 1
        
    except Exception as e:
        print(f"Error accessing page {i}: {e}")

    

for item in data:
    #Scraping Data Header
    product = item.find("div", class_='card')
    link = product.find("div", class_='d-flex flex-row').find("a").get("href")
    final_link = (f'https://www.ikea.co.id{link}')
    response = requests.get(final_link)
    soup_link = BeautifulSoup(response.content, 'html.parser')
    #description access
    head = soup_link.find("div", class_='row item_detail_information clearfix')
    desc_access = head.find("div", class_='col-12 col-sm-12 col-md-5 col-lg-5 col-xl-4 product-box-wrap mt-4 mt-md-0')\
        .find("div", class_='itemInfo')
    name = desc_access.find("h1")\
        .find("div", class_='d-flex flex-row').get_text(strip=True)
    short_desc = desc_access.find("h1")\
        .find("span", class_='itemFacts font-weight-normal').get_text(strip=True)
    price = desc_access.find("div", class_='itemPrice-wrapper')\
        .find("span", class_='currency').next_sibling.get_text(strip=True)
    final_price = (f"IDR {price}")
    purchased = desc_access.find("p", class_='partNumber').get_text(strip=True)\
        .replace(" orang telah membeli produk ini", " Purchased")
    #additional access
    prod_details = soup_link.find("div", id='modal-product-details')\
        .find("div", class_='card')\
        .find("div", class_='card-body')
    num_article = prod_details.find("div", class_='partNumber my-2 d-inline-flex flex-column')\
        .find("span", class_='item-code')\
        .get_text(strip=True)
    long_desc = prod_details.find("div", class_='product-desc-wrapper mb-4')\
        .find("p").get_text(strip=True)
    material = prod_details.find("div", class_='modal-accordeon mt-5')\
        .find("div", id="materials-details")\
            .find("div", class_="mb-3")\
                .get_text(strip=True)\
                .replace('<br>', ' \t')\
                .replace('</strong>', ' ')
    try:
        advantage = prod_details.find("div", class_='modal-accordeon mt-5')\
            .find("div", id='benefits')\
            .find("div", class_='card-body')\
            .find_all('p')
        final_advantage = ' '.join(p.get_text(strip=True) for p in advantage)
    except:
        final_advantage = ("This product whether doesn't have benefits or the writer just lazy to write it down")
    #additional access 2
    measurements = soup_link.find("div", id='modal-measurements')\
        .find("div", class_='card')\
        .find("div", class_='card-body')\
        .find("div", class_='mb-3')\
        .find("tbody")\
        .find_all("td")
    final_measurements = ' '.join(m.get_text(strip=True) for m in measurements)
    #Result_Product
    final_result.append = {
        "No" : index,
        "Name" : name,
        "Link" : final_link,
        "No Article" : num_article,
        "Short desc" : short_desc,
        "Long desc" : long_desc,
        "Advantage" : final_advantage,
        "Material" : material,
        "Measurements" : final_measurements,
        "Price" : final_price,
        "Number Purchased" : purchased 
    }
    index += 1
    print("-------")
    
    break


df = pd.DataFrame(final_result)
df.to_excel("output.xlsx", index=False)

"""

def initialize(url):
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(20)
    return browser

def get_html(browser):
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_max_page(soup: BeautifulSoup) -> int:
    max_page: list[BeautifulSoup] = soup.find("ul", class_='pagination mb-0')\
        .find_all("li", class_="page-item")
    return int(max_page[-2].find("a").get_text())

def get_products(soup,index):
    database = soup.find("div", id='product-list-component')\
        .find("div", class_='productList product-list-component')\
        .find("div", class_='productList-content d-flex flex-wrap')
    data = database.find_all("div", class_='col-6 col-md-4 col-lg-3 p-0 itemBlock')
    
    
    final_result = []
    
    try:
        for item in data:
        #Scraping Data Header
            product = item.find("div", class_='card')
            link = product.find("div", class_='d-flex flex-row').find("a").get("href")
            final_link = (f'https://www.ikea.co.id{link}')

            response = requests.get(final_link)
            soup_link = BeautifulSoup(response.content, 'html.parser')

            #description access
            head = soup_link.find("div", class_='row item_detail_information clearfix')

            desc_access = head.find("div", class_='col-12 col-sm-12 col-md-5 col-lg-5 col-xl-4 product-box-wrap mt-4 mt-md-0')\
                .find("div", class_='itemInfo')
            name = desc_access.find("h1")\
                .find("div", class_='d-flex flex-row').get_text(strip=True)
            short_desc = desc_access.find("h1")\
                .find("span", class_='itemFacts font-weight-normal').get_text(strip=True)
            price = desc_access.find("div", class_='itemPrice-wrapper')\
                .find("span", class_='currency').next_sibling.get_text(strip=True)
            final_price = (f"IDR {price}")
            purchased = desc_access.find("p", class_='partNumber').get_text(strip=True)\
                .replace(" orang telah membeli produk ini", " Purchased")

            #additional access
            prod_details = soup_link.find("div", id='modal-product-details')\
                .find("div", class_='card')\
                .find("div", class_='card-body')

            num_article = prod_details.find("div", class_='partNumber my-2 d-inline-flex flex-column')\
                .find("span", class_='item-code')\
                .get_text(strip=True)
            long_desc = prod_details.find("div", class_='product-desc-wrapper mb-4')\
                .find("p").get_text(strip=True)
            material = prod_details.find("div", class_='modal-accordeon mt-5')\
                .find("div", id="materials-details")\
                    .find("div", class_="mb-3")\
                        .get_text(strip=True)\
                        .replace('<br>', ' \t')\
                        .replace('</strong>', ' ')

            try:
                advantage = prod_details.find("div", class_='modal-accordeon mt-5')\
                    .find("div", id='benefits')\
                    .find("div", class_='card-body')\
                    .find_all('p')
                final_advantage = ' '.join(p.get_text(strip=True) for p in advantage)
            except:
                final_advantage = ("This product whether doesn't have benefits or the writer just lazy to write it down")

            #additional access 2
            measurements = soup_link.find("div", id='modal-measurements')\
                .find("div", class_='card')\
                .find("div", class_='card-body')\
                .find("div", class_='mb-3')\
                .find("tbody")\
                .find_all("td")
            final_measurements = ' '.join(m.get_text(strip=True) for m in measurements)

            #Result_Product
            result = {
                "No" : index,
                "Name" : name,
                "Link" : final_link,
                "No Article" : num_article,
                "Short desc" : short_desc,
                "Long desc" : long_desc,
                "Advantage" : final_advantage,
                "Material" : material,
                "Measurements" : final_measurements,
                "Price" : final_price,
                "Number Purchased" : purchased 
            }

            final_result.append(result)
            print(f"---This is content no {index}----")
            index += 1
            time.sleep(5)
        
    except Exception as e:
        print(f"Error accessing content {item} : {e}")
    
    return final_result

def save_xlsx(data):
    df = pd.DataFrame(data)
    df.to_excel("output.xlsx", index=False)
    return df

def main():

    products = []

    browser = initialize("https://www.ikea.co.id/in/produk/perabot-kamar-mandi?sort=SALES")
    soup = get_html(browser)
    
    max_page = get_max_page(soup)
    index = 1
    for i in range(1, max_page + 1):
        print(f"Accessing page : {i}")
        try:
            final = get_products(soup, index)
            products.extend(final)
        except Exception as e:
            print(f"Error accessing page {i} : {e}")

    print(len(products))
    save_xlsx(products)

"""
    for i in range(1, max_page + 1):
        print(f"Accessing page : {i}")
        soup_page = get_html(f"https://www.ikea.co.id/in/produk/perabot-kamar-mandi?sort=SALES&page={i}")
        
        products = get_products(soup_page)
        products_items.extend(products)
    
    print(len(products_items))

    save_xlsx(products_items)

def main2():
    #products_items, list_products = [], []

    all_data = []

    browser = initialize("https://www.ikea.co.id/in/produk/perabot-kamar-mandi?sort=SALES")
    soup = get_html(browser)

    max_page = get_max_page(soup)

    for i in range(1, max_page + 1):
        print(f"Accessing page : {i}")
        url = (f"https://www.ikea.co.id/in/produk/perabot-kamar-mandi?sort=SALES&page={i}")
        browser.get(url)
        soup_page = get_html(browser)
        page_data = get_content2(soup_page)
        all_data.append(page_data)
        time.sleep(20)

    return print(all_data)
"""

if __name__ == '__main__':
    main()