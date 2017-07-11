import requests
import json
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

def get_created_utc(item):
	return item['data']['created_utc']

# hdr = {'User-Agent': 'Mac:r/bitcoin-ethereum.sentiment.analysis:v1.0' +
#        '(by /u/jmhaas821'}
utc_start = 1472688000
utc_end = 1473897600
url = 'https://www.reddit.com/r/Bitcoin/search.json?q=timestamp%3A' + str(utc_start) + '..' + str(utc_end) + '&sort=new&restrict_sr=on&rank=title&syntax=cloudsearch#'
req = requests.get(url)
json_data = json.loads(req.text)
posts = json.dumps(req.text, indent=4, sort_keys=True)

data_all = json_data['data']['children']
sorted(data_all, key=get_created_utc, reverse=True)

data_by_day = []
utc_day_break = utc_start + 86400
daily_total = 0
daily_post_counter = 1
sia = SIA()

for post in data_all:
	res = sia.polarity_scores(post['data']['title'])
	print(res)
	print(post['data']['created_utc'])
	if post['data']['created_utc'] < utc_day_break:
		daily_total += res['compound']
		daily_post_counter += 1
	else:
		while post['data']['created_utc'] >= utc_day_break:
			utc_day_break += 86400
			print(str(daily_total) + 'is the total, ' + str(daily_post_counter) + ' is the counter.')
			data_by_day.append(daily_total / daily_post_counter)
			daily_post_counter = 1
			daily_total = 0
		daily_total += res['compound']

data_by_day.append(daily_total / daily_post_counter)

print(data_by_day)