# loading libraries
import numpy as np
import pandas as pd
from pandas_datareader import data as web
import yfinance as yfin
from dateutil.relativedelta import relativedelta
from datetime import date
today = date.today()
yfin.pdr_override()
# portfolio of stocks parsing
tickers = ['MSFT', 'PEP', 'ACN', 'C', 'META','OMV.VI', 'UBSG.SW', 'ZURN.SW', 'BMW.DE', '6758.T', '^GSPC', 'EURUSD=X', 'EURCHF=X', 'EURJPY=X']
#loading into a new DF
new_data = pd.DataFrame()
for ticker in tickers:
    new_data[ticker] = web.get_data_yahoo(ticker,start = today - relativedelta(years = 1), end = today)['Adj Close']
# changing column names
column_names = ['Microsoft', 'Pepsico', 'Accenture', 'Citigroup', 'Meta', 'OMV', 'UBS', 'Zurich_Insurance_Group', 'BMW', 'Sony', 'S&P500', 'EUR/$', 'EUR/₣', 'EUR/¥']
new_data.columns = column_names
#print(new_data.head(5))
# checking the length of a DF
#print(len(new_data))
# checking null values
#print(new_data.isna().sum())
# finding companies with missing data
''''''
missing_values = new_data.isna().sum() > 0
comp_miss_val = new_data.columns[missing_values]
for i in comp_miss_val:
    new_data[i] = new_data[i].fillna(method='ffill')
# no missing data anymore
print(new_data.isna().sum())
# creating additional columns that we want to add to DF
additional_columns = []
for i in column_names:
    col_name = i + '_Returns'
    additional_columns.append(col_name)
additional_columns = additional_columns[:-3]
print(additional_columns)
new_data[additional_columns[0]] = new_data[column_names[0]] - new_data['Microsoft'].shift(1)
new_data[additional_columns[1]] = new_data[column_names[1]] - new_data['Pepsico'].shift(1)
new_data[additional_columns[2]] = new_data[column_names[2]] - new_data['Accenture'].shift(1)
new_data[additional_columns[3]] = new_data[column_names[3]] - new_data['Citigroup'].shift(1)
new_data[additional_columns[4]] = new_data[column_names[4]] - new_data['Meta'].shift(1)
new_data[additional_columns[5]] = new_data[column_names[5]] - new_data['OMV'].shift(1)
new_data[additional_columns[6]] = new_data[column_names[6]] - new_data['UBS'].shift(1)
new_data[additional_columns[7]] = new_data[column_names[7]] - new_data['Zurich_Insurance_Group'].shift(1)
new_data[additional_columns[8]] = new_data[column_names[8]] - new_data['BMW'].shift(1)
new_data[additional_columns[9]] = new_data[column_names[9]] - new_data['Sony'].shift(1)
new_data[additional_columns[10]] = new_data[column_names[10]] - new_data['S&P500'].shift(1)
print(new_data.head(2))
new_data.loc['Sum'] = new_data.sum()
for t in column_names:
    new_data.loc[new_data.index[-1], t] = ''
print(new_data.tail(1))

stock_prices = []
column_names = column_names[:-3]


for t in column_names:
    stock_price = new_data.iloc[0][t]
    stock_prices.append(stock_price)
print(stock_prices)

stock_returns = []
for t in additional_columns:
    stock_return = new_data.loc['Sum'][t]
    stock_returns.append(stock_return)
print(stock_returns)

stock_prices = np.array(stock_prices)
stock_returns = np.array(stock_returns)
return_prc = stock_returns / stock_prices
return_prc = pd.DataFrame(return_prc)
return_prc = return_prc.T
return_prc.columns = additional_columns

new_data = pd.concat([new_data, return_prc])
print(new_data.tail(2))

new_data.to_csv('/Users/danilavtonoskin/Desktop/Study/3 Semester/Empirical finance/HW/portfolio.csv')



