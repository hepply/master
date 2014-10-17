# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 18:40:29 2014

@author: NateEpply
"""

from pandas import *
import pandas.rpy.common as com
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
sta = {"skeleton.TA": "skeleton_dot_TA", "skeleton_TA": "skeleton_uscore_TA"}
quantmod = importr('quantmod', robject_translations = sta)

print ('\n\n')
print ('Welcome to Nate\'s Stock and Company Analysis Tool.\n')

print ('Please enter the symbol or ticker for the company you would like to analyze.\n')

TICKER = input('Enter Ticker Symbol ')

#Leave in notes until solved issue of using input to pull only A or Q
#FREQUENCY = input('Annual (A) or Quarterly (Q)? ').lower()

#Stock Prices from Yahoo Finance
import ystockquote

def get_stock_price(symbol):
    return ystockquote.get_price(symbol)

def yhistorical_stock_prices(symbol,start_date,end_date):
    return (ystockquote.get_historical_prices(symbol,start_date,end_date))

def get_all_info (symbol):
    return (ystockquote.get_all(symbol))

pydf_bs = pydf['BS']
pydf_is = pydf['IS']
pydf_cf = pydf['CF']

pydf_bs_a = pydf_bs['A'] 
balance_sheet_a = pydf_bs_a[sorted(pydf_bs_a.columns)]

pydf_bs_q = pydf_bs['Q']
balance_sheet_q = pydf_bs_q[sorted(pydf_bs_q.columns)]

pydf_is_a = pydf_is['A']
income_statement_a = pydf_is_a[sorted(pydf_is_a.columns)]

pydf_is_q = pydf_is['Q']
income_statement_q = pydf_is_q[sorted(pydf_is_q.columns)]

pydf_cf_a = pydf_cf['A']
cash_flow_a = pydf_cf_a[sorted(pydf_cf_a.columns)]

pydf_cf_q = pydf_cf['Q']
cash_flow_q = pydf_cf_q[sorted(pydf_cf_q.columns)]


#Sales and Revenue

is_revenue_a = income_statement_a.ix['Revenue']

is_revenue_a_graph = is_revenue_a.plot()

is_revenue_a_pctchange = is_revenue_a.pct_change()

is_revenue_a_pctchange_mean = round(is_revenue_a_pctchange.mean(),3)

if is_revenue_a_pctchange_mean > 0:
    up_or_down = 'increasing'
elif is_revenue_a_pctchange_mean < 0:
    up_or_down = 'decreasing'


print ('Revenues have been %s at an average rate of %s%% \
per year over the past %s fiscal years.' % (up_or_down,is_revenue_a_pctchange_mean*100,len(is_revenue_a)))

#Profit and Income

is_profit_a = concat([income_statement_a.ix['Gross Profit'],income_statement_a.ix['Income Before Tax'],income_statement_a.ix['Net Income']],axis = 1)
        
is_profit_a.plot()

#Margin Calculations

#Gross Profit Margin

gpm = (income_statement_a.ix['Gross Profit'] / is_revenue_a)

gpm_pct_change_mean = gpm.pct_change().mean()

if gpm_pct_change_mean > 0:
    up_or_down = 'positive'
elif gpm_pct_change_mean < 0:
    up_or_down = 'negative'

print (('The Gross-Profit Margin for %s during the most recently filed fiscal year is %s%%. %s has had a %s trend of %s%% over the past %s fiscal years.\n') % (TICKER,round(gpm[-1],3)*100,TICKER,up_or_down,round(gpm_pct_change_mean,3)*100,len(gpm)))

#Operating Profit Margin

opm = (income_statement_a.ix['Operating Income'] / is_revenue_a)

opm_pct_change_mean = opm.pct_change().mean()

if opm_pct_change_mean > 0:
    up_or_down = 'positive'
elif opm_pct_change_mean < 0:
    up_or_down = 'negative'

print (('The Operating-Profit Margin for %s during the most recently filed fiscal year is %s%%. %s has had a %s trend of %s%% over the past %s fiscal years.\n') % (TICKER,round(opm[-1],3)*100,TICKER,up_or_down,round(opm_pct_change_mean,3)*100,len(opm)))

#PreTax Profit Margin

ptpm = (income_statement_a.ix['Income Before Tax'] / is_revenue_a)

ptpm_pct_change_mean = ptpm.pct_change().mean()

if ptpm_pct_change_mean > 0:
    up_or_down = 'positive'
elif ptpm_pct_change_mean < 0:
    up_or_down = 'negative'

print (('The PreTax-Profit Margin for %s during the most recently filed fiscal year is %s%%. %s has had a %s trend of %s%% over the past %s fiscal years.\n') % (TICKER,round(ptpm[-1],3)*100,TICKER,up_or_down,round(ptpm_pct_change_mean,3)*100,len(ptpm)))

#Net Profit Margin

npm = (income_statement_a.ix['Net Income'] / is_revenue_a)

npm_pct_change_mean = npm.pct_change().mean()

if npm_pct_change_mean > 0:
    up_or_down = 'positive'
elif npm_pct_change_mean < 0:
    up_or_down = 'negative'

print (('The Net-Profit Margin for %s during the most recently filed fiscal year is %s%%. %s has had a %s trend of %s%% over the past %s fiscal years.\n') % (TICKER,round(npm[-1],3)*100,TICKER,up_or_down,round(npm_pct_change_mean,3)*100,len(npm)))

profit_margin_df = concat([gpm,opm,ptpm,npm], axis = 1)
profit_margin_df.columns = ['Gross Profit Margin','Operating Profit Margin','PreTax Profit Margin','Net Profit Margin']

#Cash Flow Analysis

#Plot Graph of Cash from Operating, Financing and Investing Activities
cfoa_a = cash_flow_a.ix['Cash from Operating Activities']
cffa_a = cash_flow_a.ix['Cash from Financing Activities']
cfia_a = cash_flow_a.ix['Cash from Investing Activities']
cash_from_a = concat([cfoa_a,cffa_a,cfia_a], axis = 1)
cash_from_a.plot()

#Cash From Operating Activities
cfoa_trend_a = cfoa_a.pct_change().mean()

if cfoa_trend_a > 0:
    up_or_down = 'positive'
elif cfoa_trend_a < 0:
    up_or_down = 'negative'

print ('Cash from Operating Activities has an overall %s trend of %s%% over the past %s fiscal years.\n' % (up_or_down,round(cfoa_trend_a,3)*100,len(cfoa_a)))

import math

def roundup(number):
    return int(math.ceil(number / 100.0)) * 100

cfoa_a_diff_max_a = max(cfoa_a.diff().dropna())

cfoa_a.diff().dropna().plot().set_ylim(0,roundup(cfoa_a_diff_max_a))


#Cash from Financing Activities

cffa_trend_a = cffa_a.pct_change().mean()

if cffa_trend_a > 0:
    up_or_down = 'positive'
elif cffa_trend_a < 0:
    up_or_down = 'negative'

print ('Cash from Financing Activities has an overall %s trend of %s%% over the past %s fiscal years.\n' % (up_or_down,round(cffa_trend_a,3)*100,len(cffa_a)))

cffa_a.diff().dropna().plot().set_ylim(0,roundup(max(cffa_a.diff().dropna())))


#Cash from Investing Activities

cfia_trend_a = cfia_a.pct_change().mean()

if cfia_trend_a > 0:
    up_or_down = 'positive'
elif cfia_trend_a < 0:
    up_or_down = 'negative'

print ('Cash from Investing Activities has an overall positive trend of %s%% over the past %s fiscal years.\n' % (round(cfia_trend_a,3)*100,len(cfia_a)))


cfia_a.diff().dropna().plot().set_ylim(0,roundup(max(cfia_a.diff().dropna())))

#*********************************
#Need to investigate why the cfoa,cfia,cffa graphs are combining
#************************************

#Debt Levels

#Debt Ratio --- Total Debt/Total Assets

debt_ratio_a = (balance_sheet_a.ix['Total Debt'] / balance_sheet_a.ix['Total Assets'])

recent_debt_ratio_a = debt_ratio_a[-1]

print ('The Debt Ratio from the most recent fiscal year is %s%%.\n' % (round(debt_ratio_a[-1],3)*100))

if debt_ratio_a.diff().mean() < 0:
    print ('The Debt Ratio has been decreasing at an average rate of %s%% over the past %s years.\n' % (round(debt_ratio_a.diff().mean(),3) * 100,len(debt_ratio_a)))
elif debt_ratio_a.diff().mean() > 0:
    print ('The Debt Ratio has been increasing at an average rate of %s%% over the past %s years.\n' % (round(debt_ratio_a.diff().mean(),3) * 100,len(debt_ratio_a)))

#Total Current Liabilities / Total Liabilities & Shareholder Equity
'''
total_curr_liab_to_equity = (balance_sheet_a.ix['Total Current Liabilities']) / balance_sheet_a.ix['Total Liabilities & Shareholders&#39; Equity']
'''

#Long Term Debt / Total Equity

ltd_over_equity_a = (balance_sheet_a.ix['Total Long Term Debt']) / balance_sheet_a.ix['Total Equity']

#Total Debt / Total Equity

td_equity_a = (balance_sheet_a.ix['Total Debt']) / balance_sheet_a.ix['Total Equity']

#Capitalization Ratio
#Long-Term Debt/(LongTermDebt +Shareholder Equity)
'''
capitalization_ratio_a = balance_sheet_a.ix['Total Long Term Debt'] /(balance_sheet_a.ix['Total Long Term Debt'] + balance_sheet_a.ix['Total Liabilities & Shareholders&#39; Equity'])
'''

#INTEREST COVERAGE RATIO
#EBIT/INTEREST EXPENSE
#************************
#NEED TO FIGURE OUT WHERE THEY ARE COMING THROUGH ON THE STATEMENT DATAFRAMES
#THEN ADD THE FORUMULAS AND EQUATIONS AND THAT SHIT
#***********************

#CASH FLOW TO DEBT RATIO
#OPERATING CASH FLOW / TOTAL DEBT

cash_flow_debt_ratio_a = cfoa_a/ balance_sheet_a.ix['Total Debt']

#Determining Overall Liquidity
#We will use three ratios, Current, Quick and Cash

#Current Ratio
#Current Assests/Current Liabilities

current_ratio_a = balance_sheet_a.ix['Total Current Assets']/balance_sheet_a.ix['Total Current Liabilities']

print ('The Current Ratio at the end of the most recent fiscal year was %s%%.' % (current_ratio_a[-1]))

#Quck Ratio
#(Cash & Equivalents + Short-Term Investments + Accounts Receivable) / Current Liabilities

quick_ratio_a = (balance_sheet_a.ix['Cash & Equivalents'] + balance_sheet_a.ix['Short Term Investments'] + balance_sheet_a.ix['Accounts Receivable - Trade, Net']) / balance_sheet_a.ix['Total Current Liabilities']

print ('The Quick Ratio at the end of the most recent fiscal year was %s%%.' % (quick_ratio_a[-1]))

#Cash Ratio
#Cash & Equivalents and Short Term Investments / Total Current Liabilities

cash_ratio_a = balance_sheet_a.ix['Cash and Short Term Investments'] / balance_sheet_a.ix['Total Current Liabilities']

print ('The Cash Ratio at the end of the most recent fiscal year was %s%%.' % (cash_ratio_a[-1]))

#Efficiency Ratios

#DuPont Calculation
#The Three-Step Process
#ROE = (net profit margin) * (assest turnover) * (equity multiplier)

#npm is net profit margin defined above
#Operating Efficiency - as measured by profit margin

#Net Profit Margin was calculated earlier is stored as variable npm

#ASSET TURNOVER (SALES/ASSETS)
#Asset use efficiency - as measured by total asset turnover

asset_turnover_a = (is_revenue_a/balance_sheet_a.ix['Total Assets'])

#EQUITY MULTIPLIER (ASSETS/SHAREHOLDER EQUITY)
#Financial leverage - as measured by the equity multiplier

equity_multiplier_a = (balance_sheet_a.ix['Total Assets']/balance_sheet_a.ix['Total Equity'])

#ROE1 is after tax
roe1_a = (npm) * (asset_turnover_a) * (equity_multiplier_a)

#ROE2 is pre-tax
roe2_a = income_statement_a.ix['Operating Income']/balance_sheet_a.ix['Total Equity']

#Valuation

#Method 1 Discounted Cash Flow Analysis

#Step One Determine the Forecast Period

dcf_forecast_period_a = int(input('Please Enter the forecast period for DCF? '))

#Step 2 Revenue Growth Rate

revenue_growth_mean_a = is_revenue_a.pct_change().mean()

revenue_growth_std_a = is_revenue_a.pct_change().std()

current_revenue_a = is_revenue_a[-1]

rev_for_lst = [current_revenue_a]

count = 0

while count < dcf_forecast_period_a:
    if count == 0:
        var1 = is_revenue_a[-1] * (1 + revenue_growth_mean_a)
        rev_for_lst.append(var1)
        count += 1
    else:
        var1 = var1 * (1 + revenue_growth_mean_a)
        rev_for_lst.append(var1)
        count += 1
  
revenue_forecast_a = Series(rev_for_lst)

#Step 3 Forecasting Free Cash Flows

operating_costs_a = income_statement_a.ix['Total Revenue'] - income_statement_a.ix['Operating Income']

operating_margin_a = operating_costs_a / is_revenue_a

operating_margin_mean_a = operating_margin_a.mean()

operating_costs_forecast_a = operating_margin_mean_a * revenue_forecast_a


#Cocat the two Series Rev Forecast at operating cost forecast
'''
fcf_df = concat([revenue_forecast_a,operating_costs_forecast_a],axis = 1)

fcf_df = fcf_df.columns.values('Revenue Forecast','Operating Costs')
'''


#**********************************
#TAX Rate
#does not down load with data will need to either enter in manually or find a trustworthy
#source to gather this data from
#*********************************

tax_rate_a = float(input('Please enter the tax rate (as a decimal) you would like to use to forecast FCF. '))

tax_forecast_a = (revenue_forecast_a - operating_costs_forecast_a) * tax_rate_a

#NET INVESTMENT FORECAST

temp_income_statement_a = income_statement_a.where((notnull(income_statement_a)), 0)

net_investment_a = cash_flow_a.ix['Capital Expenditures'].abs() - temp_income_statement_a.ix['Depreciation/Amortization'].dropna()

net_investment_pct_revenue_a = net_investment_a/is_revenue_a

net_investment_pct_revenue_mean_a = net_investment_pct_revenue_a.mean()

net_investment_forecast_a = revenue_forecast_a * net_investment_pct_revenue_mean_a

#Changes in Working Capital

changes_working_capital_a = cash_flow_a.ix['Changes in Working Capital']

change_work_cap_lst = [changes_working_capital_a[-1]]

count = 0

while count < dcf_forecast_period_a:
    if count == 0:
        var1 = changes_working_capital_a[-1] * (1 + revenue_growth_mean_a)
        change_work_cap_lst.append(var1)
        count += 1
    else:
        var1 = var1 * (1 + revenue_growth_mean_a)
        change_work_cap_lst.append(var1)
        count += 1

change_working_cap_forecast_a = Series(change_work_cap_lst)

#Free Cash Flow

fcf_forecast_a = revenue_forecast_a - operating_costs_forecast_a - tax_forecast_a - net_investment_forecast_a - change_working_cap_forecast_a

fcf_df = concat([revenue_forecast_a,operating_costs_forecast_a,tax_forecast_a,net_investment_forecast_a,change_working_cap_forecast_a,fcf_forecast_a], axis = 1)

fcf_df = fcf_df.T

fcf_df_columns = []

count = 0

while count < dcf_forecast_period_a + 1:
    fcf_df_columns.append('Year %s' % count)
    count += 1

fcf_df.columns = fcf_df_columns

fcf_df.index = ['Revenue Forecast','Operating Cost Forecast','Tax Cost Forecast','Net Investment Forecast','Change in Working Capital Forecast','Free Cash Flow Forecast']

import numpy as np
fcf_df = np.round(fcf_df)

#COST OF EQUITY
#Cost of Equity (Re) = Rf + Beta (Rm-Rf).

#risk free rate
#The Commonly used proxy is the 3-month US treasury bond rate.
#http://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield
Rf = float(input('Please Enter the Risk Free Rate(Rf) you would like to use. '))

#Beta
beta = float(input('Please Enter the Beta you would like to use. '))

#Equity Market Premium

#Rm1 = eps/stock price (earnings based approach)

full_quote = get_all_info(TICKER)

eps = float(full_quote['earnings_per_share'])

stock_price = float(full_quote['price'])

rm1 = eps/stock_price

'''
#Rm2 = (dps/stock price) + growth in dividends

dps = float(full_quote['dividend_per_share'])

dividend_growth = float(input('Please Enter the growth in dividends %% (as a decimal) you would like to use. '))

rm2 = (dps/stock_price) + dividend_growth
'''
equity_market_premium = (rm1 -Rf)

Re = Rf + beta*(equity_market_premium)

#Cost of Debt

cost_of_debt_before_tax = float(input('Please enter the rate of a 20 Corporate Bond (as decimal) for the companies S&P rating. '))

current_avg_tax_rate = ((income_statement_a.ix['Income Before Tax']-income_statement_a.ix['Income After Tax'])/income_statement_a.ix['Income Before Tax']).mean()

cost_of_debt_after_tax = cost_of_debt_before_tax * (1- current_avg_tax_rate)


#WACC = Re x E/V + Rd x (1 - corporate tax rate) x D/V

equity_to_value = balance_sheet_a.ix['Total Equity'][-1]/(balance_sheet_a.ix['Total Equity'][-1]+balance_sheet_a.ix['Total Debt'][-1])

debt_to_value = balance_sheet_a.ix['Total Debt'][-1]/(balance_sheet_a.ix['Total Equity'][-1]+balance_sheet_a.ix['Total Debt'][-1])

wacc = (equity_to_value * Re ) + (debt_to_value * cost_of_debt_after_tax)

#Calulate Terminal Value using Gordon Growth Model

#Terminal Value = Final Projected Year Cash Flow X (1+Long-Term Cash Flow Growth Rate) / (Discount Rate – Long-Term Cash Flow Growth Rate)

final_proj_cash_flow = fcf_forecast_a[dcf_forecast_period_a]

long_term_cash_flow_growth_rate = float(input('Please Enter the long term cash flow growth rate (as a decimal) you would like to use. '))

terminal_value = (final_proj_cash_flow *(1 + long_term_cash_flow_growth_rate))/(wacc - long_term_cash_flow_growth_rate)

#Change terminal_value to a series so we can append to fcf_forecast_a
terminal_value = Series(terminal_value, index = [dcf_forecast_period_a + 1])




#Enterprise Value

fcf_forecast_a = fcf_forecast_a.append(terminal_value)

fcf_forecast_a = fcf_forecast_a[1:] # remove year zero as we do not need it

ev_denom_a = []

x = 1

while x <= dcf_forecast_period_a:
    var1 = (1 + wacc)**x
    ev_denom_a.append(var1)
    if x == dcf_forecast_period_a:
        ev_denom_a.append(var1)
    x += 1
    

    
enterprise_value = sum(fcf_forecast_a/ev_denom_a)

net_debt = balance_sheet_a.ix['Total Debt'][-1] - balance_sheet_a.ix['Cash & Equivalents'][-1]

fair_value = enterprise_value - net_debt

#Export Data for Presentation

with ExcelWriter('Boeing Analysis.xlsx') as writer:
    income_statement_a.to_excel(writer,sheet_name = 'Income Statement')
    balance_sheet_a.to_excel(writer, sheet_name = 'Balance Sheet')
    cash_flow_a.to_excel(writer,sheet_name = 'Cash Flow Statement')
