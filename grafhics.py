import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import IndexLocator

df = pd.read_csv('date.csv')
df['Datetime'] = pd.to_datetime(df['Datetime'], format='%Y-%m-%d %H:%M')
t=df[df['Name'].isin(['LKOH'])]
print(t)

fig, ax = plt.subplots()
ax.plot(t['Datetime'], t['Price'])
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
ax.yaxis.set_major_locator(IndexLocator(base=2, offset=0))
ax.set_title("График изменения цены акции LKOH")
ax.set_xlabel('Datetime')
ax.set_ylabel('Price')
plt.grid(True)
fig.autofmt_xdate()
plt.savefig("my_plot.png")
plt.show()
plt.close()