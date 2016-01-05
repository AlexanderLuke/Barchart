import csv
import math
import time

csvfile1 = "2015-12-30_portfolio.csv"
csvfile2 = "2015-12-29_portfolio.csv"

r1 = csv.reader(open(csvfile1,"r"))
r2 = csv.reader(open(csvfile2,"r"))

r1.next()
r1.next()
r2.next()
r2.next()
same = False

for row1 in r1:
	stock1 = str(row1[0])
	print type(stock1)
	print stock1[0:len(stock1)]
	time.sleep(2)

	for row2 in r2:
		stock2 = str(row2[0])
		print type(stock2)
		print stock2[0:len(stock2)]
		time.sleep(2)
		print stock1 is stock2
		if stock1 is stock2:
			print stock1 + "--------------------"
			same = True

print same

