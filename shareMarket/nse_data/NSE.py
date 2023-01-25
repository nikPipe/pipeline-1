import json
import os
import nsetools
import pandas as pd
import numpy as np
import pprint
import requests
import datetime
import socket
import socks
port = 1080
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)

try:
    from importlib import reload
except:
    pass

for each in [nsetools]:
    reload(nsetools)




class NSETOOL:
    def __init__(self):
        self.nseTool = nsetools.Nse()
        self.file_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        self.csv_folder = '/'.join([self.file_path, 'csv_file'])
        isExist = os.path.exists(self.csv_folder)
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(self.csv_folder)

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
        self.pre_market_categories = {'NIFTY 50':'NIFTY', 'Nifty Bank':'BANKNIFTY', 'Emerge':'SME',
                                 'Securities in F&O':'FO', 'Others':'OTHERS', 'All':'ALL'}
        self.session = requests.Session()

        self.start_date = datetime.datetime(1983, 11, 24)
        self.end_date = datetime.datetime.today()

        read_json_dic = False
        self.jsonFile = '/'.join([self.file_path, 'NSE_Stock.json'])


        self.stock_dic = self.get_stock_dic(read_json_dic=read_json_dic)
        self.stock_code_list = self.get_stock_code_list()
        self.stock_name_list = self.get_stock_name_list()


        #self.get_stock_data(stock_data=False, pre_market=True)
        self.news()


    def news(self):
        '''

        :return:
        '''
        '''
        from GoogleNews import GoogleNews

        gnews = GoogleNews(period='1d')
        gnews.search('Mumbai')
        result = gnews.result()
        data = pd.DataFrame.from_dict(result)
        print(data)
        '''
        url = 'https://finance.yahoo.com/screener/unsaved/e32a99f5-6537-42e0-9e8f-7ccedf7406fd?count=100&offset=800'
        data = self.session.get(url)
        list_val = ['__attrs__', '__bool__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_content', '_content_consumed', '_next', 'apparent_encoding', 'close', 'connection', 'content', 'cookies', 'elapsed', 'encoding', 'headers', 'history', 'is_permanent_redirect', 'is_redirect', 'iter_content', 'iter_lines', 'json', 'links', 'next', 'ok', 'raise_for_status', 'raw', 'reason', 'request', 'status_code', 'text', 'url']
        print(data.headers)
        #print(data.text)



    def pre_market_data(self, category):
        '''

        :param category:
        :return:
        '''
        pre_market_categories = {'NIFTY 50':'NIFTY', 'Nifty Bank':'BANKNIFTY', 'Emerge':'SME',
                                 'Securities in F&O':'FO', 'Others':'OTHERS', 'All':'ALL'}


        url = f'https://www.nseindia.com/api/market-data-pre-open?key={pre_market_categories[category]}'
        print(url)
        data = self.session.get(f'https://www.nseindia.com/api/market-data-pre-open?key={pre_market_categories[category]}',
                                headers=self.headers)
        print(data)
        new_data = []
        for i in data:
            new_data.append(i['metadata'])

        df = pd.DataFrame(new_data)
        df = df.set_index('symbol', drop=True)
        return df



    def get_stock_data_url(self, stock_code_name, start_time_stamp, end_time_stamp):
        '''

        :return:
        '''
        url = 'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol=' + stock_code_name + '&resolution=1D&from=' + str(
            start_time_stamp) + '&to=' + str(end_time_stamp) + '&countback=9870&currencyCode=INR'

        return url

    def get_stock_data(self, stock_data=True, pre_market=True):
        '''

        :return:
        '''
        if stock_data:
            for each in self.stock_code_list:
                    url = self.get_stock_data_url(stock_code_name=each, start_time_stamp=int(self.start_date.timestamp()), end_time_stamp=int(self.end_date.timestamp()))
                    print(each, ' > ', url)
                    try:
                        if requests.head(url).status_code == 403:
                            data = self.session.get(url, headers=self.headers)
                            json_data = data.json()
                            new_data = []
                            for t_data in json_data['t']:
                                date = datetime.datetime.fromtimestamp(t_data)
                                date_val = str(date.date())
                                new_data.append(date_val)

                            json_data['t'] = new_data
                            pd_data = pd.DataFrame(json_data)
                            csv_file = '/'.join([self.csv_folder, each + '.csv'])
                            pd_data.to_csv(csv_file)
                        else:
                            print('not a 200: ', url)
                    except:
                        print('\n\nexcept URL: ', url, '\n\n')

        if pre_market:
            for each in self.pre_market_categories:
                data = self.pre_market_data(each)
                csv_file = '/'.join([self.csv_folder, self.pre_market_categories[each] + '.csv'])
                data.to_csv(csv_file)

    def get_stock_dic(self, read_json_dic=False):
        '''

        :return:
        '''
        if read_json_dic == False:
            stockCode = self.nseTool.get_stock_codes()
            stockCode_json = json.dumps(stockCode, indent=4)
            with open(self.jsonFile, "w") as outfile:
                outfile.write(stockCode_json)
        else:
            with open(self.jsonFile, 'r') as openfile:
                # Reading from json file
                stockCode = json.load(openfile)

        return stockCode

    def get_stock_code_list(self):
        '''

        :return:
        '''
        stock_code_list = []
        stock_dic = self.stock_dic
        for each in stock_dic:
            stock_code_list.append(each)

        return stock_code_list

    def get_stock_name_list(self):
        '''

        :return:
        '''
        stock_code_name_list = []
        stock_dic = self.stock_dic
        for each in stock_dic:

            stock_code_name_list.append(stock_dic[each])

        return stock_code_name_list


    def update(self):
        '''

        :return:
        '''
        self.get_stock_dic()
