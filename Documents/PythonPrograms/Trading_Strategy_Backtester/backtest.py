# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 14:36:32 2014

@author: NateEpply
"""
#backtest.py
#This file is to hold the abstract classes of the Strategy and Portfolio

#Abstract Strategy Class

from abc import ABCMeta, abstractmethod

#The Strategy Class is an abstract base class that will provide and interface
#for all subsequent (inhereted) trading strategies
#The goal for a (derived) Strategy object is to output a list of signals, 
#which has the form of a time series indexed pandas DataFrame.

class Strategy(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def generate_signals(self):
        raise NotImplementedError('Should implement generate_signals()!')
        

#Abstract Portfolio Class
        
#The Abstract Portfolio base Class represents a portfolio of positions
#including both instruments and cash, determined on the basis of a set of signals
#provided by a Strategy.
        
class Portfolio(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def generate_positions(self):
        raise NotImplementedError('Should implement generate_positions()!')
        
    @abstractmethod
    def backtest_portfolio(self):
        raise NotImplementedError('Should implement backtest_portfolio()!')
        
#Purpose of generate_positions is to provide a logic to determine how the portfolio
#positions are allocated on the basis of forecasting signals an available cash
        
#Purpose of backtest_portfolio is to provide a logic to generate the trading orders
#and subsequent equity curve (i.e growth of total equity), as a sum of holdings and cash
#and the bar-period returns associated with this curve based on the 'positions' DataFrame.
#It also produces a portfolio object that can be examined by other classes/functions