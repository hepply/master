# -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 12:53:02 2014

@author: NateEpply
"""
#import necessary libraries
import pandas as pd
import ystockquote as ysq
#*************************
#NOTE: This uses a modified version of ystockquote
#Changes were made to the get_all function in ystockquote to obtain more information
#Some parts of this program may not work properly or at all if the modifications
#to ystockquote library are not made as well
#**************************

#variable for company, start and end dates for quote info to be pulled
TICKER = 'AAPL'
start_date = '1970-01-01'
end_date = '2014-10-10'

#using ystockquote to pull the data
data_dict = ysq.get_historical_prices(TICKER,start_date,end_date)

#data is in dict format need to convert to pandas dataframe    
df1 = pd.DataFrame.from_dict(data_dict, orient = 'index')

#Get prices from dataframe
def get_all(date):
    return df1.ix[date]
   
def open_price(date):
    return df1.ix[date,'Open']
    
def close_price(date):
    return df1.ix[date,'Close']
    
def day_high(date):
    return df1.ix[date,'High']
    
def day_low(date):
    return df1.ix[date,'Low']

def day_volume(date):
    return df1.ix[date,'Volume']

def adj_close(date):
    return df1.ix[date,'Adj Close']

#Simple Moving Average Calculation
def sma(period,date):
    var1=[]
    count = 0
    start_loc = df1.index.get_loc(date)
    while count < period:
        var1.append(float(df1.ix[start_loc - count,'Close']))
        count += 1
    return (sum(var1)/len(var1))

#def sma_period(length,start,end): 

def sma_period(period,start,end):
    start_index = df1.index.get_loc(start)
    end_index = df1.index.get_loc(end)
    var2 = []
    if start_index < (period -1):
        for each in df1.index[period - 1:end_index]:
            var2.append(sma(50,each))#**********LOOK AT THE 5 SHOULD BE PERIOD????????
    else:
        for each in df1.index[start_index:end_index+1]:
            var2.append(sma(period,each))
        sma_series = pd.Series(var2, index = df1.index[start_index:end_index+1])
    return sma_series
    
#Exponential Moving Average

close = df1['Close']

def ema(period,date):
    prev_date = df1.index[df1.index.get_loc(date) - 1]
    prev_sma = sma(period,prev_date)
    multiplier = (2/((period + 1)))
    return ((float(close[date]) -prev_sma) * multiplier + prev_sma)
    
def ema_period(period,start,end):
    start_index = df1.index.get_loc(start)
    end_index = df1.index.get_loc(end)
    var3 = [ema(period,start)]
    multiplier = (2/((period + 1)))
    for each in df1.index[start_index + 1:end_index + 1]:
        current_close = float(close[pd.DataFrame(close).index.get_loc(each)])      
        var3.append((current_close - var3[-1]) * multiplier + var3[-1])
    return var3
        
#BUY and SELL FUNCTION
''' 
def order_buy(amount,money):
    cash -= money
    shares += amount
    return ('Buy Order Confirmed')

def order_sell(amount,money):
    cash += money
    shares -= amount
    return ('Sell Order Confirmed')

def log(trans_type,date,amount,money):
    pass
'''    
#**********************************
#Strategy Parameters
#Here is where we will implement different trading strategies to be backtested


cash = 1000000
shares = 0  
test_start = '1981-01-02'
start_index = df1.index.get_loc(test_start)
test_end = '2014-10-07'
end_index = df1.index.get_loc(test_end)
sma_log = []
current_log = []

#if the current(close) price is 2% greater than the 5 day simple moving avg
#then we will buy
#And if the 5 day simple moving avg is 7% below the current(close) then
#we will sell sell sell and return our position to zero(0)
'''
for each in df1.index[start_index:end_index]:
    simple_moving_average = float(sma(10,each))
    current_price = float(close_price(each))
    sma_log.append(float(sma(10,each)))
    current_log.append(float(close_price(each)))
    if current_price > simple_moving_average * 1.05 and cash > current_price:
        buy_amount = int(cash/current_price)
        shares += buy_amount
        cash -= buy_amount * current_price
        print (each,'this would be a buy')
    elif current_price < simple_moving_average - (simple_moving_average *.07) and shares > 0:
        cash_from_sale = shares * current_price
        cash += cash_from_sale
        shares = 0
        print (each,'this would be a sell')


''' 


        
    