import json
import pprint

import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

print('value and thing    ')
def web_content_div(web_content, class_path):
    '''

    :param web_content:
    :param class_path:
    :return:
    '''
    web_content_div_one = web_content.find_all('div', {'class' : class_path})
    print(web_content_div_one)
    try:
        spans = web_content_div_one[0].find_all('spans')
        texts = [span.get_text() for span in spans]
    except IndexError:
        texts = []

    return texts

def real_time_price(stock_code):
    '''

    :param stock_code:
    :return:
    '''
    url = 'https://finance.yahoo.com/quote/' +  stock_code + '?p=' +  stock_code + '&.tsrc=fin-srch'
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

        session = requests.Session()

        r = session.get(url, headers=headers)
        web_content = BeautifulSoup(r.text, 'lxml')

        texts = web_content_div(web_content, 'My(6px) Pos(r) smartphone_Mt(6px) W(100%) ')
        if texts != []:
            price, change = texts[0], texts[1]
        else:
            price, change = [], []
    except ConnectionError:
        print('this is connection error')
        price, change = [], []

    return price, change

def real_time_price_new():


    stock_code = 'TTM'
    url = 'https://finance.yahoo.com/quote/' +  stock_code + '?p=' +  stock_code + '&.tsrc=fin-srch'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

    session = requests.Session()

    r = session.get(url, headers=headers)
    web_content = BeautifulSoup(r.text, 'lxml')

    #<div class="D(ib) Mend(20px)"><fin-streamer class="Fw(b) Fz(36px) Mb(-4px) D(ib)" data-symbol="TTM" data-test="qsp-price" data-field="regularMarketPrice" data-trend="none" data-pricehint="2" value="25.175" active=""><span class="e3b14781 e983cf79">25.18</span></fin-streamer><fin-streamer class="Fw(500) Pstart(8px) Fz(24px)" data-symbol="TTM" data-test="qsp-price-change" data-field="regularMarketChange" data-trend="txt" data-pricehint="2" value="0.8649998" active=""><span class="e3b14781 f4be3290 e983cf79">+0.87</span></fin-streamer> <fin-streamer class="Fw(500) Pstart(8px) Fz(24px)" data-symbol="TTM" data-field="regularMarketChangePercent" data-trend="txt" data-pricehint="2" data-template="({fmt})" value="0.035582058" active=""><span class="e3b14781 f4be3290 f5a023e1">(+3.58%)</span></fin-streamer><fin-streamer class="D(n)" data-symbol="TTM" changeev="regularTimeChange" data-field="regularMarketTime" data-trend="none" value="" active="true"><span class="e3b14781 e983cf79">12:31PM EST</span></fin-streamer><fin-streamer class="D(n)" data-symbol="TTM" changeev="marketState" data-field="marketState" data-trend="none" value="" active="true"><span class="e3b14781">REGULAR</span></fin-streamer><div id="quote-market-notice" class="C($tertiaryColor) D(b) Fz(12px) Fw(n) Mstart(0)--mobpsm Mt(6px)--mobpsm Whs(n)"><span>As of  12:31PM EST. Market open.</span></div></div>
    method = 'D(ib) Mend(20px)'
    web_content_div_one = web_content.find_all('div', {'class': method})[0]
    '''
    method = 'My(6px) Pos(r) smartphone_Mt(6px) W(100%)'
    web_content_div_one = web_content.find_all('div', {'class': method})
    method = 'Fw(b) Fz(36px) Mb(-4px) D(ib)'
    spans = web_content_div_one[0].find_all('fin-streamer', {'class': method})
    texts = [span.get_text() for span in spans]

    method = 'Fw(b) Fz(36px) Mb(-4px) D(ib)'
    web_content_div_one = web_content.find_all('fin-streamer', {'class': method})
    texts = [span.get_text() for span in web_content_div_one]
    '''
    print(web_content_div_one)
    c = web_content.find_all('div', {'class': 'value'})

    a = web_content_div_one.find_all_next('value')

    print(c)

def real_time_price_new_():
    import yfinance
    tata = yfinance.Ticker('TTM')

    print(tata.history())


def real_time_price_new_one():
    import requests

    # Define the website you want to retrieve data from
    website = "https://www.moneycontrol.com/stocks/hist_stock_result.php?sc_id=TEL&pno=2&hdn=daily&fdt=2011-01-01&todt=2023-01-01&ex=B"

    # Define the Common Crawl index you want to search through
    index = "CC-MAIN-2021-23"

    # Build the query string
    query_string = f"http://index.commoncrawl.org/{index}-index?url={website}/*&output=json"

    # Send a GET request to the Common Crawl index
    response = requests.get(query_string)

    # Get the JSON response
    data = response.json()

    # Iterate through the results and print the URLs
    for record in data['results']:
        print(record['url'])


def real_time_price_new_two():
    from comcrawl import IndexClient
    client = IndexClient()
    client.search("reddit.com/r/MachineLearning/*")

    client.results = (pd.DataFrame(client.results)
                      .sort_values(by="timestamp")
                      .drop_duplicates("urlkey", keep="last")
                      .to_dict("records"))

    pd.DataFrame(client.results).to_csv("results.csv")



stock = ['RELIANCE.NS']
#print(real_time_price(stock_code=stock[0]))

#real_time_price_new()
#real_time_price_new_()
#real_time_price_new_one()
real_time_price_new_two()


#<fin-streamer class="Fw(b) Fz(36px) Mb(-4px) D(ib)" data-symbol="RELIANCE.NS" data-test="qsp-price" data-field="regularMarketPrice" data-trend="none" data-pricehint="2" value="2472.05" active="">2,472.05</fin-streamer>