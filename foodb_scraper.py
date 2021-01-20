from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

pd.set_option('display.max_columns', 3)


def main():
    foods = {'FOOD00047': 'Raw'}
    browser = webdriver.Firefox()
    food_chems = get_chemicals_from_food(foods, browser)
    mock_db = []

    for food, chems in food_chems.items():
        for chem in chems:
            # print(food, chem['name'], chem["link"])
            cas = get_cas(chem['link'], browser)
            mock_db.append([food, chem["name"], cas])
            print(food, chem["name"], cas)

    browser.close()
    df = pd.DataFrame(data=mock_db, columns=["Name", "Chemical", "CAS"])
    print(df)
    print(len(df.index))
    df.to_csv("chickpea.csv")


def get_chemicals_from_food(foods, browser):
    foods_with_chemicals = {}

    for db_id, prep_type in foods.items():
        handle_food_browser(browser, db_id, prep_type)
        bs4 = BeautifulSoup(browser.page_source, 'html.parser')
        food_name = str(bs4.find('td').string)
        # print(food_name)
        chemicals = []
        for a in bs4.find_all('a'):
            if 'href' in a.attrs and "/compounds/" in a['href']:
                chemicals.append({"name": str(a.string), "link": a['href']})
        foods_with_chemicals[food_name] = chemicals

    return foods_with_chemicals


def get_cas(link, browser):
    url_base = "https://foodb.ca"
    browser.get("{}{}".format(url_base, link))
    try:
        cas = browser.find_element_by_xpath("//table/tbody/tr[10]/td").text
    except:
        cas = ""
    return cas


def handle_food_browser(browser, db_id, prep_type):
    url_base = "https://foodb.ca/foods/"
    browser.get("{}{}?&prep_type={}".format(url_base, db_id, prep_type))
    element = browser.find_element_by_xpath("//select[@name='DataTables_Table_0_length']/option[text()='100']")
    browser.execute_script("arguments[0].setAttribute('value',250)", element)
    element.click()
    time.sleep(10)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
