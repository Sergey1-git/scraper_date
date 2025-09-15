from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from datetime import date
import csv
# Функция сбора данных с сайта.
def scrape_item_prices(url):
    list_name=['LKOH']
    options = webdriver.EdgeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    #time.sleep(interval_scraper())
    driver = webdriver.Edge( options=options)
    driver.get(url)
    print("page loaded")


    # Функция создания файла date.csv и записи в него данных запроса.
    def date_csv(data1, data2, data3):
        path_data_csv = os.path.join(os.getcwd(), 'date.csv')
        if not os.path.isfile(path_data_csv):
            with open('date.csv', 'w', newline='', encoding='utf-8') as file_csv:
                csvwriter = csv.writer(file_csv)
                csvwriter.writerow(['Name', 'Price', 'Datetime'])
                csvwriter.writerow([data1, data2, data3])
        else:
            try:
                with open('date.csv', 'a', newline='', encoding='utf-8') as file_csv:
                    csvwriter = csv.writer(file_csv)
                    csvwriter.writerow([data1, data2, data3])
            except FileNotFoundError:
                print("Ошибка: Файл не найден!")

    # Запрос и выборка полученных данных для записи в файл
    while True:
        try:
            driver.get(url)
            item_element = driver.find_elements(By.XPATH,"//div[2]/div[2]/div[1]/div[2]/div/div/div/table/tbody/tr")
            for item in item_element:
                s = item.text
                for name in list_name:
                    if name in s:
                        print('Данные полученные scrape_item_prices',s)
                        s = s.split()
                        name=s[0]
                        price=s[1]
                        for i in s:
                            if ':' in i:
                                today = date.today()
                                d_t = f'{today} {i[0:5]}'
                                date_csv(name, price, d_t)
            print("Данные собраны.")
            time.sleep(120)
        except Exception as e:
            print(f"Произошла ошибка: {e}. Повторный запрос будет через 5 минут.")
            time.sleep(360)  # Пауза в случае ошибки


url = 'https://smart-lab.ru/q/shares/?ysclid=m8iv2muort794765457'
scrape_item_prices(url)
