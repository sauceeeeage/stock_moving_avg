from bs4 import BeautifulSoup
import requests
from pandas_datareader import data as pdr
import yfinance as yf
import csv
import matplotlib.pyplot as plt
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date
from enum import Enum
from wxpy import *
import time


# TODO: may need to add GUI for input and output
# TODO: need to add notification system
# TODO: options: WeChat, QQ, email, SMS, GUI, or some combination of them

class crossing(Enum):
    buy = 1
    sell = 2
    already_above = 3
    already_below = 4
    wierd = 5


def get_stock_data(stock_name, start_date, end_date):
    yf.pdr_override()
    df = pdr.get_data_yahoo(stock_name, start=start_date, end=end_date+3)# add 3 days to make sure the last day is included
    return df


def get_stock_MA(df, MA_date):
    df['MA'] = df['Adj Close'].rolling(window=MA_date).mean()
    return df


def get_MA_crossing(close_last, close_second_last, ma_last):
    if close_last >= ma_last and close_second_last < ma_last:
        return crossing.buy
    elif close_last >= ma_last and close_second_last >= ma_last:
        return crossing.already_above
    elif close_last < ma_last and close_second_last > ma_last:
        return crossing.sell
    elif close_last < ma_last and close_second_last <= ma_last:
        return crossing.already_below
    else:
        return crossing.wierd  # i dont think this will ever happen


if __name__ == '__main__':
    bot = Bot()
    my_friend = bot.friends().search('大隐于市')[0]
    my_friend.send('均线交叉提醒机器人已启动')
    my_friend.send('请输入追踪股票个数')
    stock_num = int(my_friend.get_msg())# idk if this works
    stock_name_list = []
    MA_date_list = []
    for i in range(stock_num):
        my_friend.send('请输入第'+str(i+1)+'个股票代码')
        my_friend.send('例如，输入000001.sz(深股) 或者 600000.ss(沪股) 或者 0002.hk(港股) 或者 AAPL(美股)')
        stock_name_list.append(my_friend.get_msg())
        my_friend.send('已收到股票代码')
        my_friend.send('请输入第'+str(i+1)+'个股票均线天数')
        my_friend.send('例如，输入5')
        MA_date_list.append(int(my_friend.get_msg()))
        my_friend.send('已收到均线天数')
    my_friend.send('已收到所有股票信息')
    my_friend.send('请输入提醒间隔时长(单位：分钟)')
    my_friend.send('例如，输入5')
    interval = Message.text
    my_friend.send('已收到提醒间隔时长')
    my_friend.send('请输入最高提醒次数')
    my_friend.send('例如，输入5')
    max_remind = Message.text
    my_friend.send('已收到最高提醒次数')
    count = 0

    while count < max_remind:
        for i in range(stock_num):
            stock_name = stock_name_list[i]
            MA_date = MA_date_list[i]
            today = date.today()
            start_date = today - relativedelta(months=6)
            df = get_stock_data(stock_name, start_date, today)
            df = get_stock_MA(df, MA_date)
            close_last = df['Adj Close'][-1]
            close_second_last = df['Adj Close'][-2]
            ma_last = df['MA'][-1]
            crossing = get_MA_crossing(close_last, close_second_last, ma_last)
            if crossing == crossing.buy:
                my_friend.send('股票' + stock_name + '均线交叉提醒：买入')
            elif crossing == crossing.sell:
                my_friend.send('股票' + stock_name + '均线交叉提醒：卖出')
            elif crossing == crossing.already_above:
                my_friend.send('股票' + stock_name + '均线交叉提醒：已经在均线上方')
            elif crossing == crossing.already_below:
                my_friend.send('股票' + stock_name + '均线交叉提醒：已经在均线下方')
            else:
                my_friend.send('股票' + stock_name + '均线交叉提醒：出现未知情况')
            count += 1
        embed()
        time.sleep(interval*60)



# embed()
#
# # #get the stock data from sina finance
# url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sz300813&scale=5&ma=10&datalen=200'# FIXME: the url need to change to support more stocks
# # 在url中（参数为：symbol=【股票编号】&scale=【分钟间隔（5、15、30、60）】&ma=【均值（5、10、15、20、25）】&datalen=【查询个数点（最大值1023）】）
# r = requests.get(url)
# print("finished scraping data from sina finance")
# yf.pdr_override()
# code = '300813.sz'# FIXME: the code need to change to support more stocks, and .ss的后缀，这表示该代码是沪股的。此外，还能通过.sz的后缀来表示深股，通过.hk的后缀表示港股。如果要获取美股的数据，则直接用美股的股票代码即可
# end_date = date.today() + relativedelta(days=+3)# FIXME: this code might break, or not working as expected due to this data will only be updated after the market close(i think)
# start_date = date.today() + relativedelta(days=-11)
# stock = pdr.get_data_yahoo(code, start_date, end_date)  # got 6 months worth of data
# print(stock)  # 输出内容
# print("successfullly got stock data from yahoo finance")
# # 保存为csv文件
# stock.to_csv('CSV_stock_data_' + code + '.csv')
# print("successfullly saved stock data to csv file")
#
# # 读取csv文件
# df = pd.read_csv('CSV_stock_data_' + code + '.csv')
# # read Close column
# close = df['Close']
# print(close)
# # calculate moving average of 5 days
# ma5 = close.rolling(5).mean()
# print(ma5)
# # get the last element of the moving average
# ma5_last = ma5.iloc[-1]
# print(ma5_last)
# # get the last element of the close price
# close_last = close.iloc[-1]
# print(close_last)
# # get the second to last element of the close price
# close_second_last = close.iloc[-2]
#
# # calculate moving average of 10 days
# # ma10 = close.rolling(window=10).mean()
# # print(ma10)
#
#
# f1 = open('stock_data.txt', 'w')
# f1.write(r.text)
# f1.close()
# print("finished writing stock data to txt")
#
# # write stock data to csv file
# with open('stock.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['date', 'open', 'high', 'low', 'close', 'volume'])
#     for item in r.json():
#         writer.writerow([item['day'], item['open'], item['high'], item['low'], item['close'], item['volume']])
#         # item name need to match exactly the name in the json file
# print("finished writing stock data to csv")
#
# # f2 = open('stock_data.txt', 'r')
# # data = f2.read()
# # f2.close()
# # print("finished reading stock data from file")
