#import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import ticker
from matplotlib.ticker import AutoLocator, IndexLocator
import datetime

df = pd.read_csv('date.csv',header=0)
df['Datetime'] = pd.to_datetime(df['Datetime'], format='%Y-%m-%d %H:%M')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df=df.sort_values(by='Datetime')
df=df.reset_index(drop=True)


def average_value_week_minute():
    fig, ax = (plt.subplots(figsize=(10, 6)))
    ax.plot(df['Datetime'], df['Price'])
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    #ax.yaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    ax.yaxis.set_major_locator(IndexLocator(base=20, offset=0))
    ax.set_title( f"График изменения цены акции LKOH за период {df.loc[0,'Datetime']}-{df.loc[len(df) - 1,'Datetime']}")
    ax.set_xlabel('Дата и время')
    ax.set_ylabel('Цена акции')
    plt.grid(True)
    fig.autofmt_xdate()
    plt.savefig("week_minute.png")
    plt.show()
    plt.close()


def average_value_week_hour():
    average_value = df.copy(deep=True)
    average_value['day'] = average_value['Datetime'].dt.day
    average_value['hour'] = average_value['Datetime'].dt.hour
    average_value['Average_value_Price']=average_value.groupby(['day', 'hour'])['Price'].transform('mean')
    average_value['Average_value_dt']=average_value.groupby(['day', 'hour'])['Datetime'].transform('mean')
    average_value.loc[0]=df.loc[0]
    average_value.loc[len(average_value)] = {'Name': df.loc[len(df)-1, 'Name'],'Price': df.loc[len(df)-1,'Price'],'Datetime':
    df.loc[len(df)-1,'Datetime'], 'day': average_value.loc[len(average_value)-1]['day'], 'hour':
    average_value.loc[len(average_value)-1]['hour'],'Average_value_Price': df.loc[len(df)-1,'Price'],'Average_value_dt':
    df.loc[len(df)-1,'Datetime']}
    average_value.loc[0, 'Average_value_Price'] = average_value.loc[0, 'Price']
    average_value.loc[0, 'Average_value_dt'] = average_value.loc[0, 'Datetime']

    fig, ax = (plt.subplots(figsize=(10, 6)))
    ax.plot(average_value['Average_value_dt'], average_value['Average_value_Price'])
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    #ax.yaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    ax.yaxis.set_major_locator(IndexLocator(base=20, offset=0))
    ax.set_title(f"График изменения цены акции LKOH за период {df.loc[0,'Datetime']}-{df.loc[len(df) - 1,'Datetime']}\n"
                 f" (усредненный часовой)")
    ax.set_xlabel('Дата и время')
    ax.set_ylabel('Цена акции')
    plt.grid(True)
    fig.autofmt_xdate()
    plt.savefig("week_hour.png")
    plt.show()
    plt.close()


def average_value_day_minute():
    value_day_minute_min = datetime.datetime(2025, 9, 18, 6, 15)
    value_day_minute_max = datetime.datetime(2025, 9, 18, 23, 45)
    day_minute = df[(df['Datetime'] > value_day_minute_min) & (df['Datetime'] < value_day_minute_max)]
    day_minute=day_minute.reset_index(drop=True)

    fig, ax = (plt.subplots(figsize=(10, 6)))
    ax.plot(day_minute['Datetime'], day_minute['Price'])
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    # ax.yaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    ax.yaxis.set_major_locator(IndexLocator(base=20, offset=0))
    ax.set_title(
        f"График изменения цены акции LKOH за период {day_minute.loc[0,'Datetime']}-{ day_minute.loc[len(day_minute)- 1,
        'Datetime']}")
    ax.set_xlabel('Дата и время')
    ax.set_ylabel('Цена акции')
    plt.grid(True)
    fig.autofmt_xdate()
    plt.savefig("day_minute.png")
    plt.show()
    plt.close()


def distribution_by_price():

    fig = figsize = (10, 8)
    plt.title('Распределение значений цены акции LKOH по 10 интервалам')
    plt.xlabel('Стоимость акции')
    plt.ylabel('Количество значений в ценовом интервале')
    plt.grid(True)
    plt.hist(df['Price'], bins=10)
    plt.savefig("distribution.png")
    plt.show()
    plt.close()

average_value_week_minute()
average_value_week_hour()
average_value_day_minute()
distribution_by_price()