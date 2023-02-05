import random
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By


def main():
    browser = webdriver.Chrome()
    link = 'https://www.sahibinden.com/alfa-romeo?pagingSize=50'
    car_list = []
    next_page = True
    page_limit = 5
    page_count = 0
    while next_page and page_count < page_limit:
        browser.get(link)
        time.sleep(2 + random.random())
        cars = browser.find_elements(by=By.CSS_SELECTOR, value='.searchResultsItem')
        for car in cars:
            if car.get_attribute('data-id') is None:
                continue
            else:
                model = car.find_elements(by=By.CSS_SELECTOR, value='.searchResultsTagAttributeValue')
                infos = car.find_elements(by=By.CSS_SELECTOR, value='.searchResultsAttributeValue')
                price = car.find_elements(by=By.CSS_SELECTOR, value='.searchResultsPriceValue')
                location = car.find_elements(by=By.CSS_SELECTOR, value='.searchResultsLocationValue')
                try:
                    car_list.append({'model': model[0].text,
                                     'version': model[1].text,
                                     'year': int(infos[0].text),
                                     'km': int(infos[1].text.replace('.', '')),
                                     'color': infos[2].text,
                                     'price': int(price[0].text.replace('.', '').replace('TL', '')),
                                     'location': location[0].text.replace('\n', ' ')})
                    print(model[0].text)
                finally:
                    continue
        time.sleep(1 + random.random())

        next_link = browser.find_elements(by=By.CSS_SELECTOR, value='.prevNextBut')
        next_page = False if len(next_link) == 0 else True
        for n in next_link:
            if n.get_attribute('title') == 'Sonraki':
                link = n.get_attribute('href')
                next_page = True
                page_count += 1
            else:
                next_page = False
    browser.close()

    with open('cars.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['model', 'version', 'year', 'km', 'color', 'price', 'location'])
        for car in car_list:
            writer.writerow([car['model'], car['version'],
                             car['year'], car['km'],
                             car['color'], car['price'], car['location']])


if __name__ == "__main__":
    main()
