#!usr/bin/python

import csv
from yahoo_finance import Share
import datetime
import math

currentTime = str(datetime.datetime.now())
day = currentTime[0:10]
time = currentTime[11:16]
csvfile = "/home/pi/" day + "_portfolio.csv"

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
