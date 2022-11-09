from bs4 import BeautifulSoup
import requests
from pandas_datareader import data as pdr
import yfinance as yf
import csv
import matplotlib.pyplot as plt
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date

if __name__ == '__main__':
    # #get the stock data from sina finance
    # url = 'https://finance.sina.com.cn/realstock/company/sz300813/nc.shtml'
    url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sz300813&scale=5&ma=10&datalen=200'
    # 在url中（参数为：symbol=【股票编号】&scale=【分钟间隔（5、15、30、60）】&ma=【均值（5、10、15、20、25）】&datalen=【查询个数点（最大值1023）】）
    r = requests.get(url)
    print("finished scraping data from sina finance")
    yf.pdr_override()
    code = '300813.sz'
    end_date = date.today()+ relativedelta(days=+1)
    start_date = date.today() + relativedelta(days=-11)
    stock = pdr.get_data_yahoo(code, start_date, end_date)  # got 6 months worth of data
    print(stock)  # 输出内容
    print("successfullly got stock data from yahoo finance")
    # 保存为csv文件
    stock.to_csv('CSV_stock_data_' + code + '.csv')
    print("successfullly saved stock data to csv file")

    # 读取csv文件
    df = pd.read_csv('CSV_stock_data_' + code + '.csv')
    # read Close column
    close = df['Close']
    print(close)
    # calculate moving average of 5 days
    ma5 = close.rolling(5).mean()
    print(ma5)
    # calculate moving average of 10 days
    # ma10 = close.rolling(window=10).mean()
    # print(ma10)

    f1 = open('stock_data.txt', 'w')
    f1.write(r.text)
    f1.close()
    print("finished writing stock data to txt")

    # write stock data to csv file
    with open('stock.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'open', 'high', 'low', 'close', 'volume'])
        for item in r.json():
            writer.writerow([item['day'], item['open'], item['high'], item['low'], item['close'], item['volume']])
            # item name need to match exactly the name in the json file
    print("finished writing stock data to csv")



    # f2 = open('stock_data.txt', 'r')
    # data = f2.read()
    # f2.close()
    # print("finished reading stock data from file")
