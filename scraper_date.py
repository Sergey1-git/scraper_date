from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from datetime import date
import csv
import datetime

# Функция определяет периоды когда scrape_item_prices выполняет запросы данных с сайта.
def interval_scraper():
    now = datetime.datetime.now()
    day_week=now.weekday()


    # Функция проверяет находится ли время запроса данных в разрешенном интервале.
    def is_in_allowed_time(now, start_time, end_time):
        if start_time <= end_time:  # Простой случай (например, 9:00 - 18:00)
            return start_time <= now < end_time


    # Функция рассчитывает количество секунд до целевого времени.
    def get_seconds_until(target_time, now_time):
        if target_time > now_time:
            return (target_time - now_time).total_seconds()
            # Переход через полночь
        else:
            tomorrow = datetime.timedelta(days=1)
            return (datetime.datetime.combine(datetime.date.today(), target_time) + tomorrow
                    - datetime.datetime.combine(datetime.date.today(), now_time)).total_seconds()

    # Блокировка запросов  scrape_item_prices в дни (суббота и воскресенье) когда данные на сайте не обновляются.
    if day_week==5 or day_week==6:
        days_before_monday = (0 - now.weekday() + 7) % 7
        date_next_monday = now.date() + datetime.timedelta(days=days_before_monday)
        next_monday_dt = datetime.datetime.combine(date_next_monday, datetime.time(6, 50, 0))
        time_before_monday = (next_monday_dt - now).total_seconds()
        if time_before_monday > 0:
            print(f"Программа будет ждать до понедельника, {next_monday_dt} когда в запрашиваемой таблице появятся"
                  f" свежие данные.")
            return time_before_monday
    else:

        # Задается интервал опроса scrape_item_prices данных на сайте в рабочие дни.
        start_allow = datetime.time(6, 50)
        end_allow = datetime.time(23, 45)
        now = datetime.datetime.now().time()
        if is_in_allowed_time(now, start_allow, end_allow):
            print(f"Разрешен запрос данных")
            return 0
        else:
            # Рассчитываем время до начала следующего разрешенного периода
            seconds_to_wait = get_seconds_until(start_allow, now)
            print(f"Программа будет ждать до {start_allow} следующего дня когда в запрашиваемой таблице появятся"
                  f" свежие данные.")
            return seconds_to_wait


# Функция сбора данных с сайта.
def scrape_item_prices(url):
    list_name=['LKOH']
    options = webdriver.EdgeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    time.sleep(interval_scraper())
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
