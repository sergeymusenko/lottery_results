#!/usr/bin/env python3
"""\
This is Scrapper main file

Start each hour :00 bewfore cron_draws (it will fill last_results table)
We checking all missing results for last 7 days see config.py
Send notification to Telegram chat.
User must be added to group "24Lottos log", open https://t.me/+pgoDy1JxwXFlZTgy

pip3 install pymysql
pip3 install pytz
pip3 install bs4
"""

__project__	= "Lotteries Results Scrapper"
__part__	= 'Scrapper main file'
__author__	= "Sergey V Musenko"
__email__	= "sergey@musenko.com"
__license__	= "MIT"
__copyright__= "© 2024, musenko.com"
__credits__	= ["Sergey Musenko"]
__date__	= "2024-01-15"
__version__	= "0.1"
__status__	= "dev"

from config import *
from lib.pymysqlwrapper import *
from lib.functions import *
from lib.scrapers import *
from lib.simple_telegram import *

if __name__ == '__main__':
	# init
	scrapeOnly = '' # '' - means proceed ALL
	l = r = 0
	nowDtUTC = get_now_utc() # UTC
	weekStart = week_start_date()[:11] # date only
	message = f'🚀 {nowDtUTC}. Lottery Results Scrapper #Start'
	print(message.replace('#', ''))
	send_to_telegram(TapiToken, TchatID, message) # send to Telegram
	main_start = time.time()

	# connect DB
	DB = pyMySQL(DBconf);
	# get results datetimess and save to Lotteries
	getLatestResTime(DB) # check last week only!

	# find outdated/absent results and scrape
	EnW = {'e':[], 'w':[]} # errors and warnings
	for aliasRrc in Lotteries: # lotteries loop

		# get lottery config
		alias = Lotteries[aliasRrc]['alias'] # 24lottos alias
		url = Lotteries[aliasRrc]['url']
		urlType = Lotteries[aliasRrc]['urlType'].upper()
		drawTimezone = Lotteries[aliasRrc]['timezone']
		lastresults = Lotteries[aliasRrc]['lastresults'] # from DB, list, in UTC !!!
		if not url: continue # do not check this lottery
		if scrapeOnly and aliasRrc != scrapeOnly: continue

		l += 1 # lottery counter
		print(f"{l}. {aliasRrc}:") #  {lastresults}

		# loop all draw times for a lottery
		for draw in Lotteries[aliasRrc]['drawTimeList']: # draws loop
			if len(draw) == 3:
				drawDow, drawTime, gameID = draw
			else:
				drawDow, drawTime = draw
				gameID = 0
			if len(drawTime) < 6: drawTime += ':00' # if draws time has no seconds

			# exact draws datetime
			drawDt = delta_days(weekStart + drawTime, drawDow - 1)
			ztShort = get_tz_short(drawDt, drawTimezone)
			drawDtUTC = local_to_utc(drawDt, drawTimezone)
			if nowDtUTC < drawDtUTC: # draw date is in the future - make it in week ago
				drawDt = delta_days(weekStart + drawTime, drawDow - 7 - 1) # week ago
				drawDtUTC = local_to_utc(drawDt, drawTimezone)
			# having results already? no, run it
			if not lastresults or drawDt not in lastresults: # scrape and save to DB
				print(f"\tScrape: {aliasRrc} on {drawDt} {ztShort}, {drawDtUTC}")
				res = scrapeLottoRes(DB, aliasRrc, alias, drawDt, ztShort, url, urlType, gameID, EnW)
				if res:
					r += 1 # results added counter
			# else: print(f"\tskip {aliasRrc} on {drawDt}")
		# draws loop -- end
	# lotteries loop -- end

	# print summary, warnings, errors
	error_level = 0
	message = f"Total: {l} lotteries checked, {r} results added"
	if len(EnW['w']):
		error_level = 1
		message = "🔔 " + message
		message += "\n{} #Warnings:".format(len(EnW['w']))
		for e in EnW['w']: 	message += f"\n• {e}"
	if len(EnW['e']):
		error_level = 2
		message = "🆘 " + message
		message += "\n{} #Errors:".format(len(EnW['e']))
		for e in EnW['e']: 	message += f"\n• {e}"
	if not error_level:
		message = "🔥 " + message
	print(message.replace('#', ''))
	if error_level or r > 0:
		send_to_telegram(TapiToken, TchatID, message) # send to Telegram

	# timing
	main_elapsed = round(time.time() - main_start, 3)
	print(f"Elapsed time: {main_elapsed}s")

# that's all folks!
