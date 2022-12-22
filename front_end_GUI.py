import win32api
from win10toast import ToastNotifier
# use this website: https://www.geeksforgeeks.org/python-gui-tkinter/

# info i need to get from the user are:
# stock symbols(for every stock in the array, and it should come with which market it's on), 用Entry
# MA date(均线天数), 用Entry
# reminding interval(in minutes), 用Entry
# need to add a window to show the current selected stocks, MA dates, and the current reminding interval用Listbox/Text
# need to add a feature to add/remove stocks, MA dates, and the reminding interval用scrollbar????
# 最后要加一个button，点击后开始运行程序
from tkinter import *
master = Tk()
master.title('均线提醒器')
master.geometry("600x600")

T = Text(root, height=2, width=30)
T.pack()
T.insert(END, 'GeeksforGeeks\nBEST WEBSITE\n')

Label(master, text='股票代码').grid(row=0)
Label(master, text='Last Name').grid(row=1)
Label(master, text='Last Name').grid(row=1)
e1 = Entry(master)
e2 = Entry(master)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

button = Button(master, text='确认', width=25, command=master.quit)
button.grid(row=3, column=0, sticky=W, pady=4)

mainloop()

# win32api.MessageBox(0, "hello", "test")

# toast = ToastNotifier()

# toast.show_toast(
#     "test title",
#     "test body",
#     duration = 5,
#     icon_path = "notification_icon.png",
#     threaded = True
# )

