import requests
import json
import numpy as np
import tensorflow as tf
from datetime import datetime

apiKey = ''

def getDateRangeFromUser():
	from_date = raw_input("Enter start date (YYYY, MM, DD):\n")
	to_date = raw_input("Enter end date (YYYY, MM, DD):\n")
	try:
		fd = datetime.strptime(from_date, '%Y, %m, %d')
		td = datetime.strptime(to_date, '%Y, %m, %d')
	except ValueError:
		print "Incorrect format"
	return fd, td

def convertRangeToUTC(from_date, to_date):
	from_timestamp = (from_date - datetime(1970, 1, 1)).total_seconds()
	to_timestamp = (to_date - datetime(1970, 1, 1)).total_seconds()
	return from_timestamp, to_timestamp

def createPoloniexURL(from_timestamp, to_timestamp, period):
	return "https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start=" + str(from_timestamp) + "&end=" + str(to_timestamp) + "&period=" + period

def getData(url):
	response = requests.get(url, auth=(apiKey))
	return json.loads(response._content)

