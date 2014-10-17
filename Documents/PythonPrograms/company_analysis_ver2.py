# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 19:44:02 2014

@author: NateEpply
"""

import Quandl
from pandas import *

#used for authenticating to Quandl
TOKEN = 'xaXXXjruuuzmfFYmFvAb'

#user inputs for company to analyze and report frequency Annual 'A' or Quarterly 'Q'
TICKER = input('Enter Ticker ')
FREQUENCY = input('Enter Frequency ')

#INCOME STATEMENT

#List of items on Income Sheet, not every will have data for each
#This is a consolidated list from Quandl to access their database with
#As the data on the SEC database each company uses their own wordage this is consolidated

IS_ITEMS = ['REVENUE','TOTAL_REVENUE','COST_OF_REVENUE_TOTAL','GROSS_PROFIT','SELLING_GENERAL_ADMIN_EXPENSES_TOTAL',
            'GAIN_LOSS_ON_SALE_OF_ASSETS','OTHER_NET','INCOME_BEFORE_TAX','INCOME_AFTER_TAX','NET_INCOME_BEFORE_EXTRA_ITEMS',
            'NET_INCOME','INCOME_AVAILABLE_TO_COMMON_EXCL_EXTRA_ITEMS','INCOME_AVAILABLE_TO_COMMON_INCL_EXTRA_ITEMS',
            'DILUTED_WEIGHTED_AVERAGE_SHARES','DILUTED_EPS_EXCLUDING_EXTRAORDINARY_ITEMS','RESEARCH_DEVELOPMENT','UNUSUAL_EXPENSE_INCOME',
            'OPERATING_INCOME','MINORITY_INTEREST','DIVIDENDS_PER_SHARE_COMMON_STOCK_PRIMARY_ISSUE','DEPRECIATION_AMORTIZATION','EQUITY_IN_AFFILIATES',
            'TOTAL_OPERATING_EXPENSE','DILUTED_NORMALIZED_EPS','OTHER_OPERATING_EXPENSES_TOTAL','DILUTION_ADJUSTMENT','OTHER_REVENUE_TOTAL',
            'INTEREST_INCOME_EXPENSE_NET_NON_OPERATING']

#simple count to the below for loop and building the dataframe for the income statement
count = 0
is_indexes = []
#for loop that goes through IS_ITEMS and builds a data frame of the income statement for company
#Based on the data pulled from Quandl
for each in IS_ITEMS:
    try:
        if count < 1:
            var1 = Quandl.get('RAYMOND/%s_%s_%s' % (TICKER,each,FREQUENCY), authtoken = TOKEN)
            var1.columns = [each]
            count += 1
            income_statement = var1 / 1000
            is_indexes.append(each)
        else:
            var2 = Quandl.get('RAYMOND/%s_%s_%s' % (TICKER,each,FREQUENCY), authtoken = TOKEN)
            var2.columns = [each]
            if 'STOCK' not in each and 'EPS' not in each: # Dividing data to make easier to read, but not all data needs to be divided            
                var2 = var2 / 1000
            income_statement = concat([income_statement,var2], axis = 1)
            is_indexes.append(each)
    except:
        continue

#Transposing completed dataframe so that dates are column labels and items from IS_ITEMS are the indexes
income_statement = income_statement.T

#BALANCE SHEET

BS_ITEMS = ['ACCOUNTS_RECEIVABLE_TRADE_NET','TOTAL_INVENTORY','PREPAID_EXPENSES','OTHER_CURRENT_ASSETS_TOTAL',
            'TOTAL_CURRENT_ASSETS','GOODWILL_NET','TOTAL_ASSETS','ACCOUNTS_PAYABLE','CURRENT_PORT_OF_LT_DEBT_CAPITAL_LEASES',
            'TOTAL_CURRENT_LIABILITIES','DEFERRED_INCOME_TAX','TOTAL_LIABILITIES','COMMON_STOCK_TOTAL','ADDITIONAL_PAID_IN_CAPITAL',
            'RETAINED_EARNINGS_ACCUMULATED_DEFICIT','TOTAL_EQUITY','TOTAL_LIABILITIES_SHAREHOLDERS_EQUITY','TOTAL_COMMON_SHARES_OUTSTANDING',
            'CASH_EQUIVALENTS','CASH_AND_SHORT_TERM_INVESTMENTS','INTANGIBLES_NET','OTHER_LONG_TERM_ASSETS_TOTAL','LONG_TERM_DEBT','TOTAL_LONG_TERM_DEBT',
            'TOTAL_DEBT','MINORITY_INTEREST','OTHER_EQUITY_TOTAL','PROPERTY_PLANT_EQUIPMENT_TOTAL_GROSS','OTHER_CURRENT_LIABILITIES_TOTAL',
            'OTHER_LIABILITIES_TOTAL','LONG_TERM_INVESTMENTS','ACCRUED_EXPENSES','NOTES_PAYABLE_SHORT_TERM_DEBT','TOTAL_RECEIVABLES_NET',
            'PREFERRED_STOCK_NON_REDEEMABLE_NET','SHORT_TERM_INVESTMENTS','CAPITAL_LEASE_OBLIGATIONS','ACCUMULATED_DEPRECIATION_TOTAL',
            'REDEEMABLE_PREFERRED_STOCK_TOTAL','TREASURY_STOCK_COMMON']

count = 0
bs_indexes = []
for each in BS_ITEMS:
    try:
        if count < 1:
            var1 = Quandl.get('RAYMOND/%s_%s_%s' % (TICKER,each,FREQUENCY), authtoken = TOKEN)
            var1.columns = [each]
            count += 1
            balance_sheet = var1 / 1000
            bs_indexes.append(each)
        else:
            var2 = Quandl.get('RAYMOND/%s_%s_%s' % (TICKER,each,FREQUENCY), authtoken = TOKEN)
            var2.columns = [each]
            var2 = var2 / 1000
            balance_sheet = concat([balance_sheet,var2], axis = 1)
            bs_indexes.append(each)
    except:
        continue

balance_sheet = balance_sheet.T

#CASH FLOW STATEMENT

CF_ITEMS = ['NET_INCOME_STARTING_LINE','DEPRECIATION_DEPLETION','AMORTIZATION','CASH_FROM_OPERATING_ACTIVITIES',
            'ISSUANCE_RETIREMENT_OF_DEBT_NET','CASH_FROM_FINANCING_ACTIVITIES','NET_CHANGE_IN_CASH','CASH_INTEREST_PAID_SUPPLEMENTAL',
            'CASH_TAXES_PAID_SUPPLEMENTAL','DEFERRED_TAXES','CHANGES_IN_WORKING_CAPITAL','CASH_FROM_INVESTING_ACTIVITIES',
            'FOREIGN_EXCHANGE_EFFECTS','NON_CASH_ITEMS','OTHER_INVESTING_CASH_FLOW_ITEMS_TOTAL','FINANCING_CASH_FLOW_ITEMS',
            'TOTAL_CASH_DIVIDENDS_PAID','ISSUANCE_RETIREMENT_OF_STOCK_NET','CAPITAL_EXPENDITURE']
            
count = 0
cf_indexes = []
for each in CF_ITEMS:
    try:
        if count < 1:
            var1 = Quandl.get('RAYMOND/%s_%s_%s' % (TICKER,each,FREQUENCY), authtoken = TOKEN)
            var1.columns = [each]
            count += 1
            cash_flow_statement = var1 / 1000
            cf_indexes.append(each)
        else:
            var2 = Quandl.get('RAYMOND/%s_%s_%s' % (TICKER,each,FREQUENCY), authtoken = TOKEN)
            var2.columns = [each]
            var2 = var2 / 1000
            cash_flow_statement = concat([cash_flow_statement,var2], axis = 1)
            cf_indexes.append(each)
    except:
        continue

cash_flow_statement = cash_flow_statement.T

#The Three Statements have been put together now it is time to analyze them

#ANALYZE INCOME STATEMENT

def is_analysis(each):
    is_separate = income_statment.ix[each]
    is_separate_pct_change = is_separate.pct_change()
    is_separate_mean = is_separate_pct_change.mean()
    return (is_separate_mean)


#Analyze Balance Sheet

def bs_analysis(each):
    bs_separate = balance_sheet.ix[each]
    bs_separate_pct_change = bs_separate.pct_change()
    bs_separate_mean = bs_separate_pct_change.mean()
    return (bs_separate_mean)
    
#ANALYZE CASH FLOW STATEMENT
    
def cf_analysis(each):
    cf_separate = cash_flow_statement.ix[each]
    cf_separate_pct_change = cf_separate.pct_change()
    cf_separate_mean = cf_separate_pct_change.mean()
    return (cf_separate_mean)
    
#For Loops to execute the analysis functions

for each in bs_indexes:
    print ('%s has had an average yearly growth of %s' % (each,bs_analysis(each)), '%\n')
        
#FUNDAMENTAL ANALYSIS
        
#Sales & Profit Growth Trends

#Revenue Trends aka Sales Trends

is_revenue = income_statement.ix['REVENUE']
is_revenue.plot(label = 'REVENUE').legend()

is_rev_pct_change = is_revenue.pct_change().mean()
is_revenue_length = len(is_revenue.dropna())

if is_rev_pct_change > 0:
    up_or_down = 'increased'
elif is_rev_pct_change < 0:
    up_or_down = 'decreased'

print ('Revenue has %s at an average rate of %s%% over the past %s years.\n\n' % (up_or_down,is_rev_pct_change,is_revenue_length))

#Profit Growth

#Profit Margins



#Gross Profit Margin

gpm = (income_statement.ix['GROSS_PROFIT'] / is_revenue) * 100

gpm_pct_change_mean = gpm.pct_change().mean()

print (('The Gross-Profit Margin for %s during the most recently filed fiscal year is %s%%. %s has had a positive/negative trend of %s%% over the past %s fiscal years.\n') % (TICKER,gpm[-1],TICKER,gpm_pct_change_mean,len(gpm)))

#Operating Profit Margin

opm = (income_statement.ix['OPERATING_INCOME'] / is_revenue) * 100

opm_pct_change_mean = opm.pct_change().mean()

print (('The Operating-Profit Margin for %s during the most recently filed fiscal year is %s%%. %s has had a positive/negative trend of %s%% over the past %s fiscal years.\n') % (TICKER,opm[-1],TICKER,opm_pct_change_mean,len(opm)))


#PreTax Profit Margin

ptpm = (income_statement.ix['INCOME_BEFORE_TAX'] / is_revenue) * 100

ptpm_pct_change_mean = ptpm.pct_change().mean()

print (('The PreTax-Profit Margin for %s during the most recently filed fiscal year is %s%%. %s has had a positive/negative trend of %s%% over the past %s fiscal years.\n') % (TICKER,ptpm[-1],TICKER,ptpm_pct_change_mean,len(ptpm)))

#Net Profit Margin

npm = (income_statement.ix['NET_INCOME'] / is_revenue) * 100

npm_pct_change_mean = npm.pct_change().mean()

print (('The Net-Profit Margin for %s during the most recently filed fiscal year is %s%%. %s has had a positive/negative trend of %s%% over the past %s fiscal years.\n') % (TICKER,npm[-1],TICKER,npm_pct_change_mean,len(npm)))

#Graph of all the profit margins


profit_margin_graph = concat([gpm,opm,ptpm,npm], axis = 1)
profit_margin_graph.columns = ['Gross Profit Margin (%)','Operating Profit Margin (%)','PreTax Profit Margin (%)','Net Profit Margin (%)']

profit_margin_graph.plot()

#Build Data frame and plot the actuals of Gross Profit, EBIT and Net Income

profit_growth_lst = ['GROSS_PROFIT','INCOME_BEFORE_TAX','NET_INCOME']

count = 0
for each in profit_growth_lst:
    if count < 1:
        is_profit = income_statement.ix[each]
        count += 1
    else:
        var1 = income_statement.ix[each]
        is_profit = concat([is_profit,var1], axis = 1)


#Plot graph with Gross Profit, Income Before Tax and Net Income
is_profit.plot(label = 'Profit Growth')

#CASH FLOW ANALYSIS



#Plot Graph of Cash from Operating, Financing and Investing Activities
cfoa = cash_flow_statement.ix['CASH_FROM_OPERATING_ACTIVITIES']
cffa = cash_flow_statement.ix['CASH_FROM_FINANCING_ACTIVITIES']
cfia = cash_flow_statement.ix['CASH_FROM_INVESTING_ACTIVITIES']
cash_from = concat([cfoa,cffa,cfia], axis = 1)
cash_from.plot()

#Cash From Operating Activities
cfoa_trend = cfoa.pct_change().mean()

if cfoa_trend > 0:
    print ('Cash from Operating Activities has an overall positive trend of %s%% over the past %s fiscal years.' % (cfoa_trend,len(cfoa)))
elif cfoa_trend < 0:
    print ('Cash from Operating Activities has an overall negative trend of %s%% over the past %s fiscal years.' % (cfoa_trend,len(cfoa)))

for each in cfoa.diff():
    if each < 0:
        print ('Note there was a decrease in Cash from Operating Activities from YYYY to YYYY, in the amount of %s.' % (each)) 
    else:
        print ('Cash flow from Operating Activities increasd from YYYY to YYYY.')

#Cash from Financing Activities

cffa_trend = cffa.pct_change().mean()

if cffa_trend > 0:
    print ('Cash from Financing Activities has an overall positive trend of %s%% over the past %s fiscal years.' % (cffa_trend,len(cffa)))
elif cffa_trend < 0:
    print ('Cash from Financing Activities has an overall negative trend of %s%% over the past %s fiscal years.' % (cffa_trend,len(cffa)))

for each in cffa.diff():
    if each < 0:
        print ('Note there was a decrease in Cash from Financing Activities from YYYY to YYYY, in the amount of %s.' % (each)) 
    else:
        print ('Cash flow from Financing Activities increasd from YYYY to YYYY.')

#Cash from Investing Activities

cfia_trend = cfia.pct_change().mean()

if cfia_trend > 0:
    print ('Cash from Investing Activities has an overall positive trend of %s%% over the past %s fiscal years.' % (cfia_trend,len(cfia)))
elif cfia_trend < 0:
    print ('Cash from Investing Activities has an overall negative trend of %s%% over the past %s fiscal years.' % (cfia_trend,len(cfia)))

for each in cfia.diff():
    if each < 0:
        print ('Note there was a decrease in Cash from Investing Activities from YYYY to YYYY, in the amount of %s.' % (each)) 
    else:
        print ('Cash flow from Investing Activities increasd from YYYY to YYYY.') 
        
        
#DEBT LEVELS

#Debt Ratio --- Total Debt/Total Assets


debt_ratio = (balance_sheet.ix['TOTAL_DEBT'] / balance_sheet.ix['TOTAL_ASSETS'])
debt_ratio_as_pct = debt_ratio * 100

recent_debt_ratio = debt_ratio[-1]
recent_debt_ratio_as_pct = recent_debt_ratio * 100

print ('The Debt Ratio from the most recent fiscal year is %s%%.' % (recent_debt_ratio_as_pct))

debt_ratio_diff_mean = debt_ratio.diff().mean() * 100

if debt_ratio_diff_mean < 0:
    print ('The Debt Ratio has been decreasing at an average rate of %s%% over the past %s years.' % (debt_ratio_diff_mean,len(debt_ratio)))
elif debt_ratio_diff_mean > 0:
    print ('The Debt Ratio has been increasing at an average rate of %s%% over the past %s years.' % (debt_ratio_diff_mean,len(debt_ratio)))

#********************
#DEBT Equity Ratio
#Need to add in equation and everything else
#Equation is Total Liabilities / Shareholder Equity
#Need to look into how to get Total Liabilities, some companies only showing total current liabilities
#*********************

#Capitalization Ratio
#Long-Term Debt/(LongTermDebt +Shareholder Equity)
#The capitalization ratio measures the debt component of a company's capital structure, 
#or capitalization (i.e., the sum of long-term debt liabilities and shareholders' equity) 
#to support a company's operations and growth. 

capitalization_ratio = balance_sheet.ix['TOTAL_LONG_TERM_DEBT'] /(balance_sheet.ix['TOTAL_LONG_TERM_DEBT'] + balance_sheet.ix['TOTAL_LIABILITIES_SHAREHOLDERS_EQUITY'])

#***************
#NEED TO ADD IN PRINT STATEMENTS TO SHOW THE CAP RATIO DATA AND ITS TRENDS
#***************

#INTEREST COVERAGE RATIO
#EBIT/INTEREST EXPENSE
#************************
#NEED TO FIGURE OUT WHERE THEY ARE COMING THROUGH ON THE STATEMENT DATAFRAMES
#THEN ADD THE FORUMULAS AND EQUATIONS AND THAT SHIT
#***********************

#CASH FLOW TO DEBT RATIO
#OPERATING CASH FLOW / TOTAL DEBT

cash_flow_debt_ratio = cash_flow_statement.ix['CASH_FROM_OPERATING_ACTIVITIES']/ balance_sheet.ix['TOTAL_DEBT']

#***************
#NEED TO ADD IN PRINT STATEMENTS TO SHOW THE CAP RATIO DATA AND ITS TRENDS
#***************

#Determining Overall Liquidity
#We will use three ratios, Current, Quick and Cash

#Current Ratio
#Current Assests/Current Liabilities

current_ratio = balance_sheet.ix['TOTAL_CURRENT_ASSETS']/balance_sheet.ix['TOTAL_CURRENT_LIABILITIES']

print ('The Current Ratio at the end of the most recent fiscal year was %s%%.' % (current_ratio[-1]))


#Quck Ratio
#(Cash & Equivalents + Short-Term Investments + Accounts Receivable) / Current Liabilities

quick_ratio = (balance_sheet.ix['CASH_EQUIVALENTS'] + balance_sheet.ix['SHORT_TERM_INVESTMENTS'] + balance_sheet.ix['ACCOUNTS_RECEIVABLE_TRADE_NET']) / balance_sheet.ix['TOTAL_CURRENT_LIABILITIES']

print ('The Quick Ratio at the end of the most recent fiscal year was %s%%.' % (quick_ratio[-1]))

#Cash Ratio
#Cash & Equivalents / Current Liabilities

cash_ratio = balance_sheet.ix['CASH_EQUIVALENTS'] / balance_sheet.ix['TOTAL_CURRENT_LIABILITIES']

print ('The Cash Ratio at the end of the most recent fiscal year was %s%%.' % (cash_ratio[-1]))

#Efficiency Ratios

#DuPont Calculation
#The Three-Step Process
#ROE = (net profit margin) * (assest turnover) * (equity multiplier)

#npm is net profit margin defined above
#Operating Efficiency - as measured by profit margin
npm1 = npm / 100

#ASSET TURNOVER (SALES/ASSETS)
#Asset use efficiency - as measured by total asset turnover

asset_turnover = (is_revenue/balance_sheet.ix['TOTAL_CURRENT_ASSETS'])

#EQUITY MULTIPLIER (ASSETS/SHAREHOLDER EQUITY)
#Financial leverage - as measured by the equity multiplier

equity_multiplier = (balance_sheet.ix['TOTAL_ASSETS']/balance_sheet.ix['TOTAL_EQUITY'])

roe = (npm1) * (asset_turnover) * (equity_multiplier)

#Valuation

#Method 1 Discounted Cash Flow Analysis

#Step One Determine the Forecast Period

dcf_forecast_period = int(input('Please Enter the forecast period for DCF? '))

#Step 2 Revenue Growth Rate

revenue_growth_mean = is_revenue.pct_change().mean()

revenue_growth_std = is_revenue.pct_change().std()

current_revenue = is_revenue[-1]

rev_for_lst = [current_revenue]

count = 0

while count < dcf_forecast_period:
    if count == 0:
        var1 = is_revenue[-1] * (1 + revenue_growth_mean)
        rev_for_lst.append(var1)
        count += 1
    else:
        var1 = var1 * (1 + revenue_growth_mean)
        rev_for_lst.append(var1)
        count += 1
  
revenue_forecast = Series(rev_for_lst)

#Step 3 Forecasting Free Cash Flows

operating_costs = income_statement.ix['TOTAL_REVENUE'] - income_statement.ix['OPERATING_INCOME']

operating_margin = operating_costs / is_revenue



