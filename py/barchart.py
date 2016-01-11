#!/usr/bin/python

from lxml import html
import time
import requests
from yahoo_finance import Share
import csv
import datetime
import math

def update(csvfile):
    r = csv.reader(open(csvfile,"r"))
    final_rows = []
    first_row = r.next()
    final_rows.append(first_row)

    date_row = r.next()
    date_row.append(time + " Price")
    date_row.append(time + " Profit")
    final_rows.append(date_row)

    difference_list = []

    for item in r:
        stock = item[0]
        open_price = float(item[1])
        if Share(stock).get_price() is None:
            profit_row = item
            profit_row.append(time + " Net Profit")
            profit_row.append(float("{0:.2f}".format(sum(difference_list))))
            final_rows.append(profit_row)
            break
        else:
            new_price = float(Share(stock).get_price())
            difference = float("{0:.2f}".format(new_price - open_price))
            difference_list.append(difference)
            item.append(new_price)
            item.append(difference)
            final_rows.append(item)

    w = csv.writer(open(csvfile,"w"))
    for row in final_rows:
        w.writerow(row)

URL = 'http://www.barchart.com/stocks/signals/top100?mode=I&view=main'
page = requests.get(URL)
text_of_page = str(page.text)
tree = html.fromstring(page.text)

start_list_index = text_of_page.find('<table class="datatable js" id="dt1"')
end_list_index = text_of_page.find('>',start_list_index)

total_list = text_of_page[start_list_index:end_list_index]
reduced_list = total_list[total_list.find('symbols=')+8:total_list.find(';')]

name_list = reduced_list.split(',')

portfolio = []
investment = 0
net_profit = 0
buy_threshold = 55

for stock in name_list:
    if Share(stock).get_open() is not None:
	print Share(stock).get_open()
        open_price = float(Share(stock).get_open())
        current_price = float(Share(stock).get_price())
    if open_price < buy_threshold:
        investment = float("{0:.2f}".format(investment + open_price))
        difference = float("{0:.2f}".format(current_price - open_price))
        net_profit = net_profit + float("{0:.2f}".format(current_price - open_price))
        row = [stock, open_price, current_price, difference]
        portfolio.append(row)

currentTime = str(datetime.datetime.now())
day = currentTime[0:10]
time = currentTime[11:16]
hour = int(currentTime[11:13])
csv_name = "/home/pi/" + day + "_portfolio.csv"

w = csv.writer(open(csv_name, "w"))
w.writerow(["Buy threshold = $" + str(buy_threshold)])
w.writerow(["Stock", "Open Price", time + " Price", time + " Profit"])

for row in portfolio:
    w.writerow(row)

w.writerow(["Investment", investment, time + " Net Profit", net_profit])

while hour < 17:
    time.sleep(3600)
    update(csv_name)


