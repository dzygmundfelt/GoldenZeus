import requests
import json
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

hdr = {'User-Agent': 'Mac:r/bitcoin-ethereum.sentiment.analysis:v1.0' +
       '(by /u/jmhaas821'}
utc_start = 1499558400
utc_end = 1499731200
url = 'https://www.reddit.com/r/Bitcoin/search.json?q=timestamp%3A' + str(utc_start) + '..' + str(utc_end) + '&sort=new&restrict_sr=on&limit=100&rank=title&syntax=cloudsearch#'
req = requests.get(url, headers=hdr)
json_data = json.loads(req.text)
data_all = json_data['data']['children']

for post in data_all:
	print(post)

data_by_day = []
utc_day_break = utc_end - 86400
daily_total = 0
daily_post_counter = 1
sia = SIA()

while len(data_all) > 0:
	for post in data_all:
		res = sia.polarity_scores(post['data']['title'])
		print(res)
		print(post['data']['created_utc'])
		post_utc = post['data']['created_utc']
		if post_utc > utc_day_break:
			daily_total += res['compound']
			daily_post_counter += 1
			print('A')
		else:
			utc_day_break -= 86400
			while post_utc <= utc_day_break:
				utc_day_break -= 86400
				print(str(daily_total) + 'is the total, ' + str(daily_post_counter) + ' is the counter.')
				data_by_day.append(daily_total / daily_post_counter)
				daily_post_counter = 1
				daily_total = 0
				if post_utc > utc_day_break:
					break
			daily_total = res['compound']
			print('B')
	time.sleep(2)
	last = data_all[-1]['data']['name']
	req = requests.get(url+last, headers=hdr)
	json_data = json.loads(req.text)
 	data_all = json_data['data']['children']		

data_by_day.append(daily_total / daily_post_counter)

print(data_by_day)