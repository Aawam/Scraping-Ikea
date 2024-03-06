import json
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
import time


def initialize(url):
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(5)
    return browser


def get_html(browser):
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_max_page(soup: BeautifulSoup) -> int:
    max_page: list[BeautifulSoup] = soup.find("ul", class_="pagination mb-0").find_all(
        "li", class_="page-item"
    )
    return int(max_page[-2].find("a").get_text())


def get_products(soup, index, category):
    database = (
        soup.find("div", id="product-list-component")
        .find("div", class_="productList product-list-component")
        .find("div", class_="productList-content d-flex flex-wrap")
    )
    data = database.find_all("div", class_="col-6 col-md-4 col-lg-3 p-0 itemBlock")

    final_result = []

    try:
        for item in data:
            # Scraping Data Header
            product = item.find("div", class_="card")
            link = product.find("div", class_="d-flex flex-row").find("a").get("href")
            final_link = f"https://www.ikea.co.id{link}"

            response = requests.get(final_link)
            soup_link = BeautifulSoup(response.content, "html.parser")

            # description access
            head = soup_link.find("div", class_="row item_detail_information clearfix")

            desc_access = head.find(
                "div",
                class_="col-12 col-sm-12 col-md-5 col-lg-5 col-xl-4 product-box-wrap mt-4 mt-md-0",
            ).find("div", class_="itemInfo")
            name = (
                desc_access.find("h1")
                .find("div", class_="d-flex flex-row")
                .get_text(strip=True)
            )
            short_desc = (
                desc_access.find("h1")
                .find("span", class_="itemFacts font-weight-normal")
                .get_text(strip=True)
            )
            price = (
                desc_access.find("div", class_="itemPrice-wrapper")
                .find("span", class_="currency")
                .next_sibling.get_text(strip=True)
                .replace(".", "")
            )
            purchased = (
                desc_access.find("p", class_="partNumber")
                .get_text(strip=True)
                .replace(" orang telah membeli produk ini", "")
            )

            # additional access
            prod_details = (
                soup_link.find("div", id="modal-product-details")
                .find("div", class_="card")
                .find("div", class_="card-body")
            )

            num_article = (
                prod_details.find(
                    "div", class_="partNumber my-2 d-inline-flex flex-column"
                )
                .find("span", class_="item-code")
                .get_text(strip=True)
            )

            long_desc = (
                prod_details.find("div", class_="product-desc-wrapper mb-4")
                .find("p")
                .get_text(strip=True)
            )
            material = (
                prod_details.find("div", class_="modal-accordeon mt-5")
                .find("div", id="materials-details")
                .find("div", class_="mb-3")
                .get_text(strip=True)
                .replace("<br>", " \t")
                .replace("</strong>", " ")
            )

            try:
                advantage = (
                    prod_details.find("div", class_="modal-accordeon mt-5")
                    .find("div", id="benefits")
                    .find("div", class_="card-body")
                    .find_all("p")
                )
                final_advantage = " ".join(p.get_text(strip=True) for p in advantage)
            except:
                final_advantage = "This product whether doesn't have benefits or the writer just lazy to write it down"

            # additional access 2
            measurements = (
                soup_link.find("div", id="modal-measurements")
                .find("div", class_="card")
                .find("div", class_="card-body")
                .find("div", class_="mb-3")
                .find("tbody")
                .find_all("td")
            )
            final_measurements = " ".join(m.get_text(strip=True) for m in measurements)

            # Result_Product
            result = [
                {
                    "No": index,
                    "Name": name,
                    "Category": category,
                    "Link": final_link,
                    "No Article": num_article,
                    "Short desc": short_desc,
                    "Long desc": long_desc,
                    "Advantage": final_advantage,
                    "Material": material,
                    "Measurements": final_measurements,
                    "Price (IDR)": int(price),
                    "Number Purchased": int(purchased),
                }
            ]
            final_result.extend(result)
            print(f"---This is content no {index}----")
            index += 1
            time.sleep(0.5)
    except Exception as e:
        index += 1
        print(f"Error accessing content {index} : {e}")

    return final_result, int(index)


def save_xlsx(data):
    df = pd.DataFrame(data)
    df.to_excel("output.xlsx", index=False)
    print("Saved")
    return df


def main():

    final_products = []
    products = []

    browser = initialize(
        "https://www.ikea.co.id/in/produk/perabot-kamar-mandi?sort=SALES"
    )
    soup = get_html(browser)

    max_page = get_max_page(soup)
    index = 1
    count = 1
    for i in range(1, 3):
        print(f"Accessing page : {i}")
        try:
            browser = initialize(
                f"https://www.ikea.co.id/in/produk/perabot-kamar-mandi?sort=SALES&page={i}"
            )
            soup = get_html(browser)
            final, index = get_products(soup, index)
            products.extend(final)
            # browser = browser.get(
            #    f"https://www.ikea.co.id/in/produk/perabot-kamar-mandi?sort=SALES&page={i}"
            # )
            # soup = get_html(browser)
            print(index)
            time.sleep(1)
        except Exception as e:
            print(f"Error accessing page {i} : {e}")
    filters = [item["No Article"] for item in final_products]
    with open("output.json", "w") as file:
        json.dump({"products": products}, file)
    for y in products:
        try:
            if y["No Article"] not in filters:
                final_products.append(y)
                print(f"Item no {count} has been added")
                count += 1
                time.sleep(0.5)
            else:
                print(f"Item no {count} already written")
                count += 1
                time.sleep(0.5)
        except:
            print(y)
            print(type(y))

    print(len(final_products))
    save_xlsx(final_products)


def main2():
    browser = get_html(initialize("https://www.ikea.co.id/in/produk"))
    output = get_categories(browser)
    print(output)
    return output


def get_categories(html):
    output = []
    soup = html
    categories: list[BeautifulSoup] = soup.find_all(
        "div", class_="all-products-column-component"
    )
    for i in categories:
        endpoint = i.find("a")["href"]
        url = f"https://www.ikea.co.id{endpoint}"
        category = i.find("a").get_text()
        final = {"url": url, "category": category}
        output.append(final)
    return output


def scrape_categories(url, category):

    final_products = []
    products = []

    browser = initialize(f"{url}?sort=SALES")
    soup = get_html(browser)

    max_page = get_max_page(soup)
    index = 1
    count = 1
    for i in range(1, 2):
        print(f"Accessing page : {i}")
        try:
            browser = initialize(f"{url}?sort=SALES&page={i}")
            soup = get_html(browser)
            final, index = get_products(soup, index, category)
            products.extend(final)
            # browser = browser.get(
            #    f"https://www.ikea.co.id/in/produk/perabot-kamar-mandi?sort=SALES&page={i}"
            # )
            # soup = get_html(browser)
            print(index)
            time.sleep(1)
        except Exception as e:
            print(f"Error accessing page {i} : {e}")
    # filters = [item["No Article"] for item in final_products]
    with open("output.json", "w") as file:
        json.dump({"products": products}, file)
    # for y in products:
    #    try:
    #        if y["No Article"] not in filters:
    #            final_products.append(y)
    #            print(f"Item no {count} has been added")
    #            count += 1
    #            time.sleep(0.5)
    #        else:
    #            print(f"Item no {count} already written")
    #            count += 1
    #            time.sleep(0.5)
    #    except:
    #        print(y)
    #        print(type(y))

    print(len(final_products))
    # save_xlsx(final_products)
    return products


if __name__ == "__main__":
    categories = main2()
    output = []
    for category in categories[0:2]:
        url = category["url"]
        name_cat = category["category"]
        print(f"-------------{url}")
        result = scrape_categories(url, name_cat)
        output.extend(result)
    save_xlsx(output)
