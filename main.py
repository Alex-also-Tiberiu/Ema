#check if the modules below are installed
#launchpadlib
#yfinance
#tweepy


import datetime
#comand input from shell
#pip install matplot
import matplotlib.pyplot as plt
import numpy as np
#pip install pandas
import pandas as pd

#pip install pandas_datareader
from pandas_datareader.data import DataReader

#set the date
#in1 = input("type the year to start the analysis : ")
#in2 = input("type the month to start the analysis : ")
#in3 = input("type the day to start the analysis : ")
#yy = eval(in1)
#mm = eval(in2)
#dd = eval(in3)

#registering the date
start = datetime.datetime(2021,1,1)
end = datetime.datetime.now()

#show if it is right
print(start)
print(end)

#extract the closing price
ultratech_df = DataReader(['BTC-USD'],'yahoo',start = start,end = end) ['Close']
ultratech_df.columns = {'Close Price'}

# Create 20 days exponential moving average column
ultratech_df['20_EMA'] = ultratech_df['Close Price'].ewm(span = 20, adjust = False).mean()
# Create 50 days exponential moving average column
ultratech_df['50_EMA'] = ultratech_df['Close Price'].ewm(span = 50, adjust = False).mean()

# create a new column 'Signal' such that if 20-day EMA is greater
# than 50-day EMA then set Signal as 1 else 0
ultratech_df['Signal'] = 0.0
ultratech_df['Signal'] = np.where(ultratech_df['20_EMA'] > ultratech_df['50_EMA'], 1.0, 0.0)

# create a new column 'Position' which is a day-to-day difference of
# the 'Signal' column
ultratech_df['Position'] = ultratech_df['Signal'].diff()

plt.figure(figsize = (20,10))
# plot close price, short-term and long-term moving averages
ultratech_df['Close Price'].plot(color = 'k', lw = 1, label = 'Close Price')
ultratech_df['20_EMA'].plot(color = 'b', lw = 1, label = '20-day EMA')
ultratech_df['50_EMA'].plot(color = 'g', lw = 1, label = '50-day EMA')

# plot ‘buy’ and 'sell' signals
plt.plot(ultratech_df[ultratech_df['Position'] == 1].index,
         ultratech_df['20_EMA'][ultratech_df['Position'] == 1],
         '^', markersize = 15, color = 'g', label = 'buy')

plt.plot(ultratech_df[ultratech_df['Position'] == -1].index,
         ultratech_df['20_EMA'][ultratech_df['Position'] == -1],
         'v', markersize = 15, color = 'r', label = 'sell')

plt.ylabel('Price in Rupees', fontsize = 15 )
plt.xlabel('Date', fontsize = 15 )
plt.title('BTCUSD - EMA Crossover', fontsize = 20)
plt.legend()
plt.grid()
plt.show()