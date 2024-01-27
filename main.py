#!/usr/bin/env python3
"""\
This is Lottery Results Scrapper main file

Start it each hour :00
We checking all missing results for last 7 days, see draws in config.py
Send notification to Telegram chat if configured

Installation:
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
__date__	= "2024-01-27"
__version__	= "0.1"
__status__	= "prod"

from config import *
from lib.pymysqlwrapper import *
from lib.functions import *
from lib.scrapers import *
from lib.simple_telegram import *


scrape_only = '' # '' - means proceed ALL

if __name__ == '__main__':
	# init
	main_start = time.time()
	nowDtUTC = get_now_utc() # UTC
	weekStart = week_start_date()[:11] # date only
	message = f'🚀 {nowDtUTC}. Lottery Results Scrapper #Start'
	print(message.replace('#', ''))
	send_to_telegram(TapiToken, TchatID, message) # send to Telegram

	# connect to DB and get latest results datetimes, store them to Lotteries
	DB = False if not DBconf else pyMySQL(DBconf); # OR use JSON_file as source
	getLatestResTime(DB) # last week only!

	# counters
	EnW = {'e':[], 'w':[]} # errors and warnings counter
	CnR = {'c':0, 'r':0} # checked and result counter

	# find outdated/absent results and scrape
	for alias in Lotteries: # lotteries loop

		# get lottery config
		url = Lotteries[alias]['url']
		urlType = Lotteries[alias]['urlType'].upper()
		drawTimezone = Lotteries[alias]['timezone']
		lastresults = Lotteries[alias]['lastresults'] # from DB, list, in UTC !!!

		if not url: continue # do not check this lottery
		if scrape_only and alias != scrape_only: continue # check single lottery


		CnR['c'] += 1 # lottery counter
		print(f"{CnR['c']}. {alias}:")

		# loop all draw times for a lottery
		for draw in Lotteries[alias]['drawTimeList']: # draws loop
			drawDow, drawTime = draw
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
				print(f"\tScrape: {alias} on {drawDt} {ztShort}, {drawDtUTC}")
				res = 1
				res = scrapeLottoRes(DB, alias, drawDt, ztShort, url, urlType, EnW)
				if res:
					CnR['r'] += 1 # results added counter
			# else: print(f"\tskip {alias} on {drawDt}")
		# draws loop -- end
	# lotteries loop -- end

	saveResultsToFile()

	# print summary, warnings, errors
	error_level = 0
	message = f"Total: {CnR['c']} lotteries checked, {CnR['r']} results added"
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
	if error_level or CnR['r'] > 0:
		send_to_telegram(TapiToken, TchatID, message) # send to Telegram

	# timing
	main_elapsed = round(time.time() - main_start, 3)
	print(f"Elapsed time: {main_elapsed}s")

# that's all folks!
