# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 12:31:39 2014

@author: NateEpply
"""

from backtest import Strategy,Portfolio
        
#Strategy Object(s) - A trading strategy that we want to implement

import numpy as np
import pandas as pd
import ystockquote as ysq #How we will obtain financial data, note I am using a modified version of ystockquote

class Moving_Average_Strategy(Strategy):
    def __init__(self, symbol, bars, period):
        self.symbol = symbol
        self.bars = bars
        self.period = period
        
    #Simple Moving Average Calculation and puts the results into a pd.DataFrame
    def sma(self):
        return (pd.rolling_mean(pd.Series(bars['Open']),self.period).astype(float))
        
    def generate_signals(self):
        signals = pd.DataFrame((bars['Close']).astype(float),index=self.bars.index) #Creating a blank DataFrame with indexes from the column names of bars DataFrame        
        signals['Moving Average'] = mas.sma()
        signals['% Var'] = signals['Moving Average']/signals['Close']
        var1 = []
        for each in signals['% Var']:
            if each > 1.01:
                var1.append(1)
            elif each < .99:
                var1.append(-1)
            else:
                var1.append(0)
        s_var1 = pd.Series(var1, index=signals.index)
        signals['Signal'] = s_var1
        return signals


#Portfolio Object(s) - A Portfolio that accepts signals generating from a Strategy Object
#And then executes trades based on the signal it received.

#NOTE--- In addition, there are ZERO transactions costs and cash can be immediately
#borrowed for shorting (no margin posting or interest requirements)

#Requires:
#symbol - for the company that forms the basis of the portfolio
#bars - the data as a pd.DataFrame
#signals - created in the strategy object
#initial_capital - the amount of cash at the start of the portfolio
'''
class MarketOnClosePortfolio(Portfolio):
    def __init__(self,symbol,bars,signals,initial_capital=100000.0):
        self.symbol = symbol
        self.bars = bars
        self.signals = signals
        self.initial_capital= float(initial_capital)
        self.positions = self.generate_positions()
        
    def generate_positions(self):
        positions = pd.DataFrame(index=signals.index).fillna(0.0)
        positions[self.symbol] = 100*signals['Signal']
        return positions
        
    def backtest_portfolio(self):      
        portfolio = self.positions.mul(self.bars['Close'].astype(float),axis=0)
        pos_diff = self.positions.diff()
        
        portfolio['holdings'] = self.positions.mul(self.bars['Close'].astype(float),axis=0).sum(axis=1)
        
        portfolio['cash'] = self.initial_capital - (pos_diff.mul(self.bars['Close'].astype(float),axis=0).sum(axis=1))
        
        portfolio['total'] = portfolio['cash'] + portfolio['holdings']
        portfolio['returns'] = portfolio['total'].pct_change()
        
        return portfolio
'''
class MarketOnClosePortfolio(Portfolio):
    """Encapsulates the notion of a portfolio of positions based
    on a set of signals as provided by a Strategy.

    Requires:
    symbol - A stock symbol which forms the basis of the portfolio.
    bars - A DataFrame of bars for a symbol set.
    signals - A pandas DataFrame of signals (1, 0, -1) for each symbol.
    initial_capital - The amount in cash at the start of the portfolio."""

    def __init__(self, symbol, bars, signals, initial_capital=100000.0):
        self.symbol = symbol        
        self.bars = bars
        self.signals = signals
        self.initial_capital = float(initial_capital)
        self.positions = self.generate_positions()
        
    def generate_positions(self):
        positions = pd.DataFrame(index=signals.index).fillna(0.0)
        positions[self.symbol] = 100*signals['Signal']   # This strategy buys 100 shares
        return positions
                    
    def backtest_portfolio(self):
        portfolio = self.positions*self.bars['Close']
        pos_diff = self.positions.diff()

        portfolio['holdings'] = (self.positions*self.bars['Close']).sum(axis=1)
        portfolio['cash'] = self.initial_capital - (pos_diff*self.bars['Close']).sum(axis=1).cumsum()

        portfolio['total'] = portfolio['cash'] + portfolio['holdings']
        portfolio['returns'] = portfolio['total'].pct_change()
        return portfolio
'''
initial_capital = 1000000.00        
if __name__ == '__main__':
    symbol = 'AAPL'
    bars = pd.DataFrame.from_dict(ysq.get_historical_prices(symbol,'2002-01-03','2014-10-10'), orient = 'index')       

    
    mas = Moving_Average_Strategy(symbol,bars,5)
    signals = mas.generate_signals()
    
    portfolio = MarketOnClosePortfolio(symbol,bars,signals, initial_capital)
    returns = portfolio.backtest_portfolio()
    
    print (returns)
'''

class MovingAverageCrossStrategy(Strategy):
    '''
    Requires:
    symbol - A stock symbol on which to form a strategy on.
    bars - stock market data in the form of a pd.DataFrame
    short_window - Look back period for simple moving average
    long_window - Look back period for simple moving average.'''
    
    def __init__(self,symbol,bars,short_window=100,long_window=400):
        self.symbol = symbol
        self.bars = bars
        self.short_window = short_window
        self.long_window = long_window
        
    def generate_signals(self):
        signals = pd.DataFrame(index=self.bars.index)
        signals['Signal'] = 0.0
        
        signals['Short_mavg'] = pd.rolling_mean(bars['Close'], self.short_window,min_periods = 1)
        signals['Long_mavg'] = pd.rolling_mean(bars['Close'], self.long_window,min_periods = 1)
        
        signals['Signal'][self.short_window:] = np.where(signals['Short_mavg'][self.short_window:] > signals['Long_mavg'][self.short_window:], 1.0, 0.0)
        signals['Positions'] = signals['Signal'].diff()
        
        return signals

from pandas.io.data import DataReader
import datetime
import matplotlib.pyplot as plt
      
if __name__ == '__main__':
    symbol = 'AAPL'
    bars = DataReader(symbol,'yahoo',datetime.datetime(2014,1,1), datetime.datetime(2014,10,10))
    #short_window = 100
    #long_window = 400
    #initial_capital = 1000000.0    
    
    mac = MovingAverageCrossStrategy(symbol,bars,short_window = 100,long_window = 400)
    signals = mac.generate_signals()
    
    portfolio = MarketOnClosePortfolio(symbol,bars,signals,initial_capital=100000.0)
    returns = portfolio.backtest_portfolio()
    
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    ax1 = fig.add_subplot(211, ylabel ='Price in $')
    
    bars['Close'].plot(ax=ax1, color='r', lw=2.)
    signals[['Short_mavg','Long_mavg']].plot(ax=ax1, lw=2.)
    
    ax1.plot(signals.ix[signals.Positions == 1.0].index,
             signals.Short_mavg[signals.Positions == 1.0], '^',markersize = 10, color = 'k')
                  
    ax1.plot(signals.ix[signals.Positions == -1.0].index,
             signals.Short_mavg[signals.Positions == -1.0],
             'v', markersize = 10, color = 'k')
             
    ax2 = fig.add_subplot(212, ylabel='Portfolio value in $')
    returns['total'].plot(ax=ax2, lw=2.)
    
    ax2.plot(returns.ix[signals.Positions == 1.0].index,
             returns.total[signals.Positions == 1.0], '^', markersize = 10, color = 'm')
             
    ax2.plot(returns.ix[signals.Positions == -1.0].index,
             returns.total[signals.Positions == -1.0], 'v', markersize = 10, color = 'k')
             
    fig.show()
    
    
    
    
    
    