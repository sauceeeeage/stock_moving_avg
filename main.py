from pandas_datareader import data as pdr
import yfinance as yf
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date
from enum import Enum
import time
from tkinter import *
from tkinter.scrolledtext import *
import win32api
from win10toast import ToastNotifier


# TODO: may need to add GUI for input and output
# TODO: need to add notification system
# TODO: options: WeChat, QQ, email, SMS, GUI, or some combination of them

inputed_stock = ""
remind_interval = 0
remind_times = 0
stock_list = []
MA_date_list = []
count = 0

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



def getting_input_GUI():
    def click():
        text1_input = text1.get('1.0', 'end-1c')
        ri_input = remind_interval_sp.get()
        rt_input = remind_times_sp.get()
        global inputed_stock 
        inputed_stock = text1_input
        global remind_interval 
        remind_interval = ri_input
        global remind_times 
        remind_times = rt_input
        window.destroy()
    window = Tk()
    window.geometry("600x440")
    window.title("均线提醒器")
    text1_label = Label(window,text="股票代码+均线天数",fg="black", font="微软雅黑").place(x=20,y=5)
    text1 = ScrolledText(window,bg="white", width=50,font="Arial 10")
    text1.place(x=20,y=30)
    ri_label = Label(window,text="提醒间隔(分钟)",fg="black", font="微软雅黑").place(x=410,y=175)
    remind_interval_sp = Spinbox(window,from_=1,to=1000,width=20)
    remind_interval_sp.place(x=410,y=200)
    rt_label = Label(window,text="提醒次数",fg="black", font="微软雅黑").place(x=410,y=275)
    remind_times_sp = Spinbox(window,from_=1,to=1000,width=20)
    remind_times_sp.place(x=410,y=300)
    Button(window, text="保存并关闭",heigh=2,width=20,command=click).place(x=410,y=50)
    window.mainloop()

def remind(title, body):
    win32api.MessageBox(0, body, title)

    toast = ToastNotifier()
    toast.show_toast(
        title,
        body,
        duration = 5,
        icon_path = "notification_icon.png",
        threaded = True
    )

if __name__ == '__main__':
    # start the GUI to get input
    getting_input_GUI()
    # get the input from GUI
    combin_list = []
    split = inputed_stock.split("\n")
    for i in split:
        if i == "":
            continue
        temp = i.strip().split("+")
        combin_list.append(temp)
    
    while count < remind_times:
        for i in combin_list:
            stock_name = i[0]
            MA_date = int(i[1])
            start_date = date.today() - relativedelta(years=1)
            end_date = date.today()
            df = get_stock_data(stock_name, start_date, end_date)
            df = get_stock_MA(df, MA_date)
            close_last = df['Adj Close'][-1]
            close_second_last = df['Adj Close'][-2]
            ma_last = df['MA'][-1]
            crossing_status = get_MA_crossing(close_last, close_second_last, ma_last)
            if crossing == crossing.buy:
                title = "买入提醒"
                body = "股票" + stock_name + "均线交叉提醒：买入"
                remind(title, body)
            elif crossing == crossing.sell:
                title = "卖出提醒"
                body = "股票" + stock_name + "均线交叉提醒：卖出"
                remind(title, body)
            elif crossing == crossing.already_above:
                title = "横穿均线上方提醒"
                body = "股票" + stock_name + "均线交叉提醒：已经在均线上方"
                remind(title, body)
            elif crossing == crossing.already_below:
                title = "横穿均线下方提醒"
                body = "股票" + stock_name + "均线交叉提醒：已经在均线下方"
                remind(title, body)
            else:
                title = "未知情况提醒"
                body = "股票" + stock_name + "均线交叉提醒：出现未知情况"
                remind(title, body)
            count += 1
        time.sleep(remind_interval * 60)
                


    
