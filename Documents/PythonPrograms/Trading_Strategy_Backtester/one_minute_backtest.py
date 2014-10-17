# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 18:48:47 2014

@author: NateEpply
"""

#Trading Strategy backtest with 1-min interval intra-day data
#The data has been adjusted to account for splits prior to receiving the data

import pandas as pd
from backtest import Strategy, Portfolio #importing of meta classes
import numpy as np

bars = pd.read_csv('/Users/NateEpply/Downloads/IBM_adjusted.csv', index_col = 0,names = ['time','open','high','low','close','volume'] )

def date_format_change(dataframe):
    #function to change the date format from MM/DD/YYYY to YYYY-MM-DD
    count = 0
    var1_lst = []
    var2_lst = []
    for each in dataframe.index:
        var1_lst.append(each.split('/'))
    for each in var1_lst:
        var2_lst.append('%s-%s-%s' % (var1_lst[count][2],var1_lst[count][0],var1_lst[count][1]))
        count += 1
    dataframe.index = var2_lst
    return dataframe
    
#Create pd.DataFrame for moving averages
    
def close_price_df(dataframe):
    #function to remove dupliate dates, sort and create pd.DataFrame
    var1_lst = list(set(dataframe.index))
    var1_lst.sort()
    df = pd.DataFrame(var1_lst,index = var1_lst)
    df[0] = 0.0
    dates = df.index
    var3_lst = []
    var4_lst = []
    for each in dates:
        var3_lst.append(bars.ix[each]['close'][-1:])
    for item in var3_lst:
        for price in item:
            var4_lst.append(price)
    df['close'] = var4_lst
    del df[0]
    return df

date_format_change(bars)
df_mavg = close_price_df(bars)

#Add Multiple Periods of MAVG to pd.DataFrame

df_mavg['10 Day MAVG'] = pd.rolling_mean(df_mavg['close'],10)
df_mavg['20 Day MAVG'] = pd.rolling_mean(df_mavg['close'],20)
df_mavg['100 Day MAVG'] = pd.rolling_mean(df_mavg['close'],100)
df_mavg['400 Day MAVG'] = pd.rolling_mean(df_mavg['close'],400)

def rate_of_change(close,close_n_dayago):
    roc = (close-close_n_dayago)/(close_n_dayago)
    return roc
    
    
count = 0
roc_lst = []
for each in range(9):
    roc_lst.append(each * 0.0)
var1 = 0
var2 = 9

while count < len(df_mavg['close']):
    y1 = df_mavg['close'][var1]
    y2 = df_mavg['close'][var2]
    roc_lst.append(rate_of_change(y2,y1))
    var1 += 1
    var2 += 1
    count += 1
    if var2 == 4221:
        break

df_mavg['ROC for 10 Day in $'] = roc_lst


'''
signals = pd.DataFrame(bars.ix['1998-01-16']['time'])
signals['close'] = bars.ix['1998-01-16']['close']
signals['10 Day MAVG'] = df_mavg['1998-01-15']['10 Day MAVG']
signals['signal'] = np.where(signals['close'] > signals['10 Day MAVG'], 1.0, 0.0)'''







'''
I want to look at each bar of data, calculate the moving average for X & Y period of days.
Then I need to compare these 2 moving averages and based on that comparison return a signal.
The signal will need to represent buy(long), hold, sell(short).
These signals need to be returned in the form of a pd.DataFrame, with a timestamp to represent
what action the portfolio needs to take at that time.

Once the signals have been generated (1,0,-1) we will need to create a portfolio
that consists of cash(initial_capital), holdings and method for interpreting the signals
from the strategy class as to how much to buy or sell.'''

class MovingAverageStrategy(Strategy):
    
    def __init__(self,symbol,bars,short_mavg, long_mavg):
        self.symbol = symbol
        self.bars = bars
        self.short_mavg = short_mavg
        self.long_mavg = long_mavg
        
    def generate_signals(self):
        signals = pd.DataFrame(bars['time'])
        signals['close'] = bars['close']
        signals['10 Day MAVG'] = df_mavg['10 Day MAVG']
        '''if signals['close'] > signals['10 Day MAVG']:
            signals['signal'] = 1.0
        elif signals['close'] < signals['10 Day MAVG']:
            signals['signal'] = -1.0
        else:
            signals['signal'] = 0.0'''
        signals['signal'] = np.where(signals['close'] > signals['10 Day MAVG'], 1.0,0.0)
        signals['signal'] = np.where(signals['close'] < signals['10 Day MAVG'], -1.0,0.0)
        return signals
        

mas = MovingAverageStrategy('IBM',bars,100,400)
signals = mas.generate_signals()

class MavgPortfolio(Portfolio):
    
    def __init__(self,bars,signals,initial_capital):
        self.bars = bars
        self.signals = signals
        self.initial_capital = initial_capital
        
    def generate_positions(self):
        positions = pd.DataFrame(bars['time'])
        positions['position'] = int(self.signals['signal'] * (self.initial_capital/bars['close']))
        return positions
        
    def backtest_portfolio(self):
        portfolio = pd.DataFrame(bars['time'])
        
        
        
        
        
    

        