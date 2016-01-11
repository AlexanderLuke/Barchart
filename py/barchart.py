#!/usr/bin/python

from lxml import html
import time
import requests
from yahoo_finance import Share
import csv
import datetime
import math

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

csv_name = day + "_portfolio.csv"

w = csv.writer(open(csv_name, "w"))
w.writerow(["Buy threshold = $" + str(buy_threshold)])
w.writerow(["Stock", "Open Price", time + " Price", time + " Profit"])

for row in portfolio:
    w.writerow(row)

w.writerow(["Investment", investment, time + " Net Profit", net_profit])


