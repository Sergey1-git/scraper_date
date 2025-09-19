import flet as ft
from scraper_date import  scrape_item_prices,interval_scraper
import time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date
from datetime import time
from datetime import datetime

scheduler_instance = None


def main(page: ft.Page):
    page.title = "Окно запуска и остановки scraper_date"

    def button_clicked(n):
        if n==1:
            t.value = "Сбор данных запущен"
            t1.value = ""
            t5.value = ""
            page.update()
        else:
            t1.value = "Сбор данных остановлен"
            t.value = ""
            t5.value = ""
            page.update()


    # Функция запуска планировщика
    def start_planner():
        t5.value = interval_scraper()[1]
        time_start = time(7, 15, 00)
        time_end = time(23, 45, 00)
        today_start = datetime.combine(date.today(), time_start)
        today_end = datetime.combine(date.today(), time_end)
        scheduler = BackgroundScheduler()
        #scheduler.add_job(program_start, 'interval',  seconds=60)
        scheduler.add_job(program_start, 'cron',  day_of_week='0-4', minute='*/2', start_date = today_start,
                          end_date=today_end)
        scheduler.start()
        print('Планировщик запущен')
        t4.value = "Планировщик запущен"
        page.update()

        # Сохраняем ссылку на планировщик, чтобы остановить его извне
        global scheduler_instance
        scheduler_instance = scheduler

    def program_start():
        text=scrape_item_prices()
        t2.value=text
        page.update()


    # Функция остановки планировщика
    def stop_planner():
        global scheduler_instance
        if scheduler_instance:
            scheduler_instance.shutdown()
            print('Планировщик остановлен')
            t4.value = "Планировщик остановлен"
            page.update()
            scheduler_instance = None
        elif scheduler_instance is None:
            print('Планировщик не был запущен')
            t4.value = "Планировщик не был запущен"
            page.update()

    b = ft.TextButton("Запустить сбор данных", on_click= lambda e: (button_clicked(1), start_planner()))
    t = ft.Text()
    b1 = ft.TextButton("Остановить сбор данных", on_click= lambda e: (button_clicked(2), stop_planner()))
    t = ft.Text()
    t1 = ft.Text('Сбор данных остановлен')
    b2 = ft.Text("   Последние данные полученные scraper", color='blue')
    t2= ft.Text('')
    t3 = ft.Text('   Статус планировщика', color='blue')
    t4 = ft.Text('')
    t5=ft.Text('')


    page.add(ft.Row([b,t]),ft.Row([b1,t1]),ft.Row([b2,t2]), ft.Row([t3,t4]), ft.Row([t5]))

if __name__ == '__main__':
    ft.app(main)