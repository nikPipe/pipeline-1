import datetime

import pandas as pd
import requests
import pprint
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
session = requests.Session()
print('One')
#a = session.get('https://www.nseindia.com', headers=headers)
#b = session.get('https://www.nseindia.com/api/market-data-pre-open?key=NIFTY', headers=headers).json()['data']
#b = session.get('https://www.nseindia.com/api/historical/cm/equity?symbol=ACC', headers=headers).json()
#b = session.get('https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/marks?symbol=AXISBANK&from=946870200&to=2114409600&resolution=1M')


start = int(datetime.datetime(1983, 11, 24).timestamp())
end = int(datetime.datetime.today().timestamp())
name = 'ACC'
name = '500410'
name = 'AARTISURF'
#name = '512599'
a = datetime.datetime.fromtimestamp(438566400)
b = datetime.datetime.fromtimestamp(1632441600)
#print(a)
#print(start)
#print(b)
#print(end)

#b = session.get('https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol=AXISBANK&resolution=5D&from=1673234835&to=1674098835&countback=2&currencyCode=INR')
url = 'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol=AXISBANK&resolution=1D&from=438566400&to=1632441600&countback=9870&currencyCode=INR'
url = 'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol='+ name +'&resolution=1D&from='+ str(start) +'&to='+ str(end) +'&countback=9870&currencyCode=INR'
#url = 'https://priceapi.moneycontrol.com/techCharts/intra?symbol=512599&resolution=1&from=1674102000&to=1674102240'
#url = 'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol=AXISBANK&resolution=1D&from='+ str(start) +'&to=' + str(end) + '&countback=2&currencyCode=INR'

data = session.get(url, headers=headers).json()
'''
for each in data['data']:
    each['time'] = datetime.datetime.fromtimestamp(each['time'])
pd_data = pd.DataFrame(data)
print(pd_data)

'''

new_data = []
for each in data['t']:
    date = datetime.datetime.fromtimestamp(each)
    new_data.append(date)

data['t'] = new_data

pd_data = pd.DataFrame(data)
print(pd_data)

#print(a)
'''
import nsetools
import pandas as pd
import numpy as np
import pprint

nse = nsetools.Nse()
infy = nse.get_stock_codes()
infy = nse.get_quote('infy')
pprint.pprint(infy)
'''