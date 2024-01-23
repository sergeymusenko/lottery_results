#!/usr/bin/env python3
"""\
scrapers.py - This is Lottery results scrapping, custom functions for each lottery

"""
__project__	= "Lotteries Results Scrapper"
__part__	= 'Custom functions'
__author__	= "Sergey V Musenko"
__email__	= "sergey@musenko.com"
__license__	= "MIT"
__copyright__= "© 2024, musenko.com"
__credits__	= ["Sergey Musenko"]
__date__	= "2024-01-15"
__version__	= "0.1"
__status__	= "dev"

from config import Lotteries
from lib.functions import _dtfmt, ordinal
import requests
from datetime import datetime, timedelta
import time
import os.path, os
import re
import json
from bs4 import BeautifulSoup


# scrape functions ---
_timeOut = 10 # this is a fuse
_headers = {'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'}
_scrapeCache = {} # save HTML here, do not fetch it twice
_sdebug = True
_saveDB = False
#_tmpfile = 'tmp.dat' # False means do not use local data copy for debugging
_tmpfile = False

# call custom function to get results and save to DB
def scrapeLottoRes(DB, aliasRrc, alias, drawDt, ztShort, url, urlType, gameID, EnW):
	global _gameID;
	_gameID = gameID # save to global so no need to pass it as a parameter (for few lotteries)
	start_time = time.time()
	elapsed_time = ret = 0

	# call custom scrapper/parser
	# it returns [result, resDate] or [False, False]
	cutomFunc = 'custom_' + aliasRrc
	if cutomFunc in globals():
		result, resDate = eval(cutomFunc + '(aliasRrc, drawDt, url, urlType)')
		if isinstance(result, list): # an error, exception text returned
			message = f'\t{cutomFunc}() scrapper failed, '+result[0]
			EnW['e'].append(message)
			if _sdebug: print(f"\t{message}")
			return False
		elif not result: # a warning
			message = f'"{aliasRrc}" no data found'
			EnW['w'].append(message)
			if _sdebug: print(f"\t{message}")
			# notify/log scrape error ??? ############################################### <<<
			return False

	else: # an error, there is no custom scrapper function
		message = f'"{cutomFunc}" function does not exist'
		EnW['e'].append(message)
		if _sdebug: print(message)
		return False

	#save to DB
	if _saveDB:
		DB.insert(f"""
			REPLACE INTO lotto_rrc_results_archive (
				lotteryname, alias, datetime, winnumbers,
				timezone, jackpotamount, jackpotcurrency, jackpotcurrencysign )
			VALUES ( '{aliasRrc}', '{alias}', '{drawDt}', '{result}', '{ztShort}','0','-','-' )
		""")
	if not _saveDB or DB.rowcount:
		ret = True # SUCCESS finally
	else: # DB error
		message = f"{aliasRrc} saving to DB failed"
		EnW['e'].append(message)
		if _sdebug: print(message)

	# time elapsed
	elapsed_time = round(time.time() - start_time, 3)
	return ret


# get with cache
def getSourceWithCahe(cacheKey, aliasRrc, url, urlType):
	# check cached HTML
	if aliasRrc in _scrapeCache:
		html = _scrapeCache[cacheKey]
	else:
		# scrape HTML
		if _tmpfile and os.path.isfile(_tmpfile): # get local copy
			with open(_tmpfile, "r", encoding='utf-8-sig') as _log: html = _log.read()
		else:
			# get data from the net:
			html = getSource(url, urlType)
			if _tmpfile and html: # save local copy
				with open(_tmpfile, "wb") as _log: _log.write(html)
		# save cache
		_scrapeCache[cacheKey] = html
	return html


# get page source from the net
def getSource(url, urlType):
	res = False
	if urlType == 'HTML':
		page = requests.get(url, timeout=_timeOut, headers=_headers)
		res = page.content
	elif urlType == 'JSON':
		page = requests.get(url, timeout=_timeOut, headers=_headers)
		res = page.content
	elif urlType == 'REACT':
		True # not implemented yet
	return res


# CUSTOM SCRAPPING FUNCTIONS
# note: kenyalotto and tatua3 reloads pages

# hoosierlotto ----------------------------------------
def custom_hoosierlotto(aliasRrc, drawDt, url, urlType):
	result = resDate = False
	# prepare url and cache key
	xdate = drawDt[0:10]
	xurl = url.format(xdate) # hoosier URL has date on tail
	cacheKey = f"{aliasRrc}/{xdate}"
	try:
		html = getSourceWithCahe(cacheKey, aliasRrc, xurl, urlType)
		# parse results
		if html:
			# result as '{"numbers":[..],"numbers_extra":[..],"numbers_option":[]}' 
			# resDate confirming draws data from source, not in use yet
			soup = BeautifulSoup(html, "html.parser")
			datas = soup.find("table", id='past-results-table').find('tbody').find('tr', class_='main-row').find_all('td')
			resDate = str(datetime.strptime(datas[0].text, "%m/%d/%y"))[0:11] + '12:00:00'
			result = json.dumps({
				"numbers": [x.strip() for x in datas[1].text.split('-')],
				"numbers_extra": [x.strip() for x in datas[2].text.split('-')],
				"numbers_option": []
			}).replace(' ','')
	except Exception as e:
		result = [str(e)]
	return [result, resDate]


# kenyalotto -- PAGES! --------------------------------------
def custom_kenyalotto(aliasRrc, drawDt, url, urlType, page=1):
	result = resDate = False
	# prepare url and cache key
	cacheKey = xurl = url.format(page) # hoosier URL has date on tail
	try:
		html = getSourceWithCahe(cacheKey, aliasRrc, xurl, urlType)
		# parse results
		if html:
			# make date to search in format like "Thu 14 Dec 2023&nbsp;&nbsp;06:00pm"
			findDate = '{:%a %-d %b %Y %I:%M%p}'.format(datetime.strptime(drawDt,'%Y-%m-%d %H:%M:%S')).lower()
			soup = BeautifulSoup(html, "html.parser")
			datas = soup.find('div', class_='results_table').find_all('tr') # all rows of results table as list
			for tr in datas:
				TDs = tr.findAll('td')
				if TDs:
					resDate = TDs[1].text.replace(u'\xa0\xa0', ' ').lower().strip()
					if resDate == findDate:
						xNumbers = TDs[2].text.replace(' , ', ',')
						resDate = drawDt
						result = json.dumps({
							"numbers": [x.strip() for x in xNumbers.split(',')],
							"numbers_extra": [],
							"numbers_option": [] # AlexF sent something here, I do not know what
						}).replace(' ','')
						return [result, drawDt] # found, return it
			# not found at current page, go deeper
			page += 1
			if page <= 8: # no more then N pages deeper
				result, drawDt = custom_kenyalotto(aliasRrc, drawDt, url, urlType, page)
	except Exception as e:
		result = [str(e)]
	return [result, resDate]


# marksix -----------------------------------------
def custom_marksix(aliasRrc, drawDt, url, urlType): # JSON
	result = resDate = False
	# prepare url and cache key
	cacheKey = aliasRrc
	try:
		jsons = getSourceWithCahe(cacheKey, aliasRrc, url, urlType)
		datas = json.loads(jsons)
		findDate = '{:%d/%m/%Y}'.format(datetime.strptime(drawDt,'%Y-%m-%d %H:%M:%S')).lower()
		# parse json results
		if datas:
			for tr in datas: # json like [["date":"14/12/2023", "no":"3+4+11+37+44+48", ...]]
				resDate = tr['date'].strip()
				if findDate == resDate:
					resDate = drawDt
					result = json.dumps({
						"numbers": [x.strip() for x in tr['no'].split('+')],
						"numbers_extra": [],
						"numbers_option": []
					}).replace(' ','')
					break
	except Exception as e:
		result = [str(e)]
	return [result, resDate]


# japanlotto6 ----------------------------------------
def custom_japanlotto6(aliasRrc, drawDt, url, urlType):
	result = resDate = False
	cacheKey = aliasRrc # 2 weeks in 1 HTML file
	# make date to search in format like "Thu 14 Dec 2023&nbsp;&nbsp;06:00pm"
	findDate = '{:%d-%m-%Y}'.format(datetime.strptime(drawDt,'%Y-%m-%d %H:%M:%S')).lower()
	try:
		html = getSourceWithCahe(cacheKey, aliasRrc, url, urlType)
		# parse results
		if html:
			soup = BeautifulSoup(html, "html.parser")
			datas = soup.find_all("scp-draw-result-single-item")
			if datas:
				for item in datas:
					drDate = item.find('div', class_="scp-draw-result-singe-item__date").find('div').text[0:10].strip()
					if drDate == findDate: # right draws date
						scpBalls = item.find('scp-balls').find_all('span')
						if scpBalls:
							resDate = drawDt
							result = json.dumps({
								"numbers": [x.text for x in scpBalls[0:6]],
								"numbers_extra": [scpBalls[6].text],
								"numbers_option": []
							}).replace(' ','')
	except Exception as e:
		result = [str(e)]
	return [result, resDate]


# taiwanlotto649 ----------------------------------------
def custom_taiwanlotto649(aliasRrc, drawDt, url, urlType):
	result = resDate = False
	cacheKey = aliasRrc
	xurl = url.format('{:%Y-%m}'.format(datetime.strptime(drawDt,'%Y-%m-%d %H:%M:%S')))
	# ChinaY from GrigorianY: chinaY = year - 1911, data like "112/12/08"
	_drDt = datetime.strptime(drawDt,'%Y-%m-%d %H:%M:%S')
	findDate = '{:%Y-%m-%d}'.format(datetime.strptime(drawDt,'%Y-%m-%d %H:%M:%S')).lower()
	try:
		jsons = getSourceWithCahe(cacheKey, aliasRrc, xurl, urlType)
		datas = json.loads(jsons)
		# parse json results
		if datas and datas['content']['lotto649Res']:
			for draws in datas['content']['lotto649Res']:
				if findDate == draws['lotteryDate'][0:10]:
					main = draws['drawNumberSize'][0:6]
					more = draws['drawNumberSize'][-1]
					resDate = drawDt
					result = json.dumps({
						"numbers": sorted(main),
						"numbers_extra": [more],
						"numbers_option": []
					}).replace(' ','')
					break
	except Exception as e:
		result = [str(e)]
	return [result, resDate]


# philippinesgrand ----------------------------------------
def custom_philippinesgrand(aliasRrc, drawDt, url, urlType):
	return custom_philippineslotto(aliasRrc, drawDt, url, urlType)

# philippinessuper ----------------------------------------
def custom_philippinessuper(aliasRrc, drawDt, url, urlType):
	return custom_philippineslotto(aliasRrc, drawDt, url, urlType)

# philippinesultra ----------------------------------------
def custom_philippinesultra(aliasRrc, drawDt, url, urlType):
	return custom_philippineslotto(aliasRrc, drawDt, url, urlType)

# philippinesmega ----------------------------------------
def custom_philippinesmega(aliasRrc, drawDt, url, urlType):
	return custom_philippineslotto(aliasRrc, drawDt, url, urlType)

# philippineslotto ----------------------------------------
def custom_philippineslotto(aliasRrc, drawDt, url, urlType):
	result = resDate = False
	cacheKey = aliasRrc
	xurl = url
	findDate = '{:%b %-d, %Y}'.format(datetime.strptime(drawDt,'%Y-%m-%d %H:%M:%S'))
	try:
		html = getSourceWithCahe(cacheKey, aliasRrc, xurl, urlType)
		# parse results
		if html:
			soup = BeautifulSoup(html, "html.parser")
			datas = soup.find('figure').find_all('tr')[1:]
			for item in datas:
				tds = item.find_all('td')
				resDate = tds[0].text.strip()
				if resDate == findDate:
					resDate = drawDt
					result = json.dumps({
						"numbers": [x.strip() for x in tds[1].text.split('-')],
						"numbers_extra": [],
						"numbers_option": []
					}).replace(' ','')
	except Exception as e:
		result = [str(e)]
	return [result, resDate]


# nigeriagoldenchancelotto ----------------------------------------
# this is 7 games indeed, use _gameID
def custom_nigeriagoldenchancelotto(aliasRrc, drawDt, url, urlType):
	global _gameID;
	result = resDate = False
	xdate = drawDt[0:10]
	xurl = url.format(_gameID, xdate) # hoosier URL has date on tail
	cacheKey = f"{aliasRrc}/{xdate}"
	try:
		jsons = getSourceWithCahe(cacheKey, aliasRrc, xurl, urlType) # note, we requesting only 1 day result set
		datas = json.loads(jsons)
		# parse json results
		if datas and 'result' in datas[0]:
			main = []
			more = []
			for key in datas[0]['result']:
				val = datas[0]['result'][key]
				if key[0:3] == 'win':
					main.append(val)
				else:
					more.append(val)
			resDate = drawDt
			result = json.dumps({
				"numbers": sorted(main),
				"numbers_extra": sorted(more),
				"numbers_option": []
			}).replace(' ','')
	except Exception as e:
		result = [str(e)]
	return [result, resDate]


# uk49slotto ----------------------------------------
def custom_uk49slotto(aliasRrc, drawDt, url, urlType):
	result = resDate = False
	xdate = drawDt[0:10]
	cacheKey = f"{aliasRrc}"
	try:
		jsons = getSourceWithCahe(cacheKey, aliasRrc, url, urlType) # note, we requesting only 1 day result set
		datas = json.loads(jsons)
		# parse json results
		if datas and 'games' in datas:
			for event in datas['games']:
				if xdate == event['date'] and 'events' in event: # date found, now get "event_number":2
					for draw in event['events']:
						if draw['event_number'] == 2: # found, now get main and more
							main = []
							more = []
							for number in draw['drawns']:
								val = number['number']
								if not number['bonus']:
									main.append(val)
								else:
									more.append(val)
							resDate = drawDt
							result = json.dumps({
								"numbers": sorted(main),
								"numbers_extra": sorted(more),
								"numbers_option": []
							}).replace(' ','')
	except Exception as e:
		result = [str(e)]
	return [result, resDate]


# goslotto749 ----------------------------------------
def custom_goslotto749(aliasRrc, drawDt, url, urlType):
	result = resDate = False
	xnow = datetime.now() # then get 1 page with last 8 days results
	xfrom = (xnow + timedelta(days=-7)).strftime('%d.%m.%Y')
	xto = xnow.strftime('%d.%m.%Y')
	xurl = url.format(xfrom, xto) # hoosier URL has date on tail
	findDate = '{:%d.%m.%Y %H:}'.format(datetime.strptime(drawDt,'%Y-%m-%d %H:%M:%S')).lower() # not sure about minutes!
	cacheKey = f"{aliasRrc}"
	try:
		html = getSourceWithCahe(cacheKey, aliasRrc, xurl, urlType)
		# parse results
		if html:
			soup = BeautifulSoup(html, "html.parser")
			datas = soup.find("div", class_='drawings_data').find_all('div', class_='elem')
			if datas:
				for elem in datas:
					resDate = elem.find('div', class_='draw_date').text[0:14]
					numbers = elem.find('span', class_='zone').text.replace(u'\xa0', '').strip().split('\n')
					if findDate == resDate and numbers:
						result = json.dumps({
							"numbers": numbers,
							"numbers_extra": [],
							"numbers_option": []
						}).replace(' ','')
	except Exception as e: # network error
		result = [str(e)]
	return [result, resDate]


# africaenugu ----------------------------------------
def custom_africaenugu(aliasRrc, drawDt, url, urlType):
	return custom_africabingo(aliasRrc, drawDt, url, urlType)

# africainternational ----------------------------------------
def custom_africainternational(aliasRrc, drawDt, url, urlType):
	return custom_africabingo(aliasRrc, drawDt, url, urlType)

# africalucky ----------------------------------------
def custom_africalucky(aliasRrc, drawDt, url, urlType):
	return custom_africabingo(aliasRrc, drawDt, url, urlType)

# africapeoples ----------------------------------------
def custom_africapeoples(aliasRrc, drawDt, url, urlType):
	return custom_africabingo(aliasRrc, drawDt, url, urlType)

# africabingo ----------------------------------------
def custom_africabingo(aliasRrc, drawDt, url, urlType):
	result = resDate = numbers = False
	cacheKey = f"{aliasRrc}"
	findDate = '{:%-d %B %Y}'.format(datetime.strptime(drawDt,'%Y-%m-%d %H:%M:%S')).lower()
	findLen = len(findDate)
	try:
		html = getSourceWithCahe(cacheKey, aliasRrc, url, urlType) # note, we requesting only 1 day result set
		soup = BeautifulSoup(html, "html.parser")

		# 1. try to get from top
		datas = soup.find("div", class_='pb-5').find('div', class_='mt-3')
		if datas:
			resDate = datas.find('h5').text[0:findLen].lower()
			if findDate == resDate: # match
				numberSet = datas.find_all('img')
				numbers = [x['src'].split('p2=')[1].strip() for x in numberSet]

		# 2. try to get from big table
		if not numbers:
			datas = soup.find_all("div", class_='py-3')
			if datas:
				for row in datas:
					divs = row.find_all('div')
					resDate = divs[0].text.lower()
					if findDate == resDate: # match
						numbers = divs[2].text.lower().split(u'\u2002') # split by strange entity '&ensp;' that equals to '\u2002'
		if numbers:
			result = json.dumps({
				"numbers": sorted(numbers),
				"numbers_extra": [],
				"numbers_option": []
			}).replace(' ','')
	except Exception as e: # network error
		result = [str(e)]
	return [result, resDate]


# moroccolotto ----------------------------------------
def custom_moroccolotto(aliasRrc, drawDt, url, urlType): # similar to Baba Ijebu but having 6+1 balls
	result = resDate = numbers = False
	cacheKey = f"{aliasRrc}"
	findDate = '{:%-d %B %Y}'.format(datetime.strptime(drawDt,'%Y-%m-%d %H:%M:%S')).lower()
	findLen = len(findDate)
	try:
		html = getSourceWithCahe(cacheKey, aliasRrc, url, urlType) # note, we requesting only 1 day result set
		soup = BeautifulSoup(html, "html.parser")

		# 1. try to get from top
		datas = soup.find("div", class_='pb-5').find('div', class_='mt-3')
		if datas:
			resDate = datas.find('h5').text[0:findLen].lower()
			if findDate == resDate: # match
				numberSet = datas.find_all('img')
				numbers = [x['src'].split('p2=')[1].strip() for x in numberSet] # 6main + 1more
				moreNumbers = [numbers.pop()]

		# 2. try to get from big table
		if not numbers:
			datas = soup.find_all("div", class_='py-3')
			if datas:
				for row in datas:
					divs = row.find_all('div')
					resDate = divs[0].text.lower()
					if findDate == resDate: # match
						numbers = divs[2].text.lower().split(u'\u2002') # split by strange entity '&ensp;' that equals to '\u2002'
						moreNumbers = [numbers.pop()]
						numbers.pop() # delete word 'complementaire'
		if numbers:
			result = json.dumps({
				"numbers": sorted(numbers),
				"numbers_extra": moreNumbers,
				"numbers_option": []
			}).replace(' ','')
	except Exception as e: # network error
		result = [str(e)]
	return [result, resDate]


# lottomaxca ----------------------------------------
def custom_lottomaxca(aliasRrc, drawDt, url, urlType): # similar to Baba Ijebu but having 7+1 balls
	result = resDate = numbers = False
	cacheKey = f"{aliasRrc}"
	findDate = '{:%-d %B %Y}'.format(datetime.strptime(drawDt,'%Y-%m-%d %H:%M:%S')).lower()
	findLen = len(findDate)
	try:
		html = getSourceWithCahe(cacheKey, aliasRrc, url, urlType) # note, we requesting only 1 day result set
		soup = BeautifulSoup(html, "html.parser")

		# 1. try to get from top
		datas = soup.find("div", class_='pb-5').find('div', class_='mt-3')
		if datas:
			resDate = datas.find('h5').text[0:findLen].lower()
			if findDate == resDate: # match
				numberSet = datas.find_all('img')
				numbers = [x['src'].split('p2=')[1].strip() for x in numberSet] # 6main + 1more
				moreNumbers = [numbers.pop()]

		# 2. try to get from big table
		if not numbers:
			datas = soup.find_all("div", class_='py-3')
			if datas:
				for row in datas:
					divs = row.find_all('div')
					resDate = divs[0].text.lower()
					if findDate == resDate: # match
						numbers = divs[2].text.lower().split(u'\u2002') # split by strange entity '&ensp;' that equals to '\u2002'
						moreNumbers = [numbers.pop()]
						numbers.pop() # delete word 'complementaire'
		if numbers:
			result = json.dumps({
				"numbers": sorted(numbers),
				"numbers_extra": moreNumbers,
				"numbers_option": []
			}).replace(' ','')
	except Exception as e: # network error
		result = [str(e)]
	return [result, resDate]

# tatua3 -- PAGES! --------------------------------------
def custom_tatua3(aliasRrc, drawDt, url, urlType, page=1):
	result = resDate = False
	# prepare url and cache key
	cacheKey = xurl = url.format(page) # hoosier URL has date on tail
	try:
		html = getSourceWithCahe(cacheKey, aliasRrc, xurl, urlType)
		# parse results
		if html:
			# make date to search in format like "Fri, 22nd Dec 2023 – 09:30". NOTE: it contains 0x2013 char
			dt = datetime.strptime(drawDt,'%Y-%m-%d %H:%M:%S')
			dom = '{:%-d}'.format(dt)
			findDate = '{:%a, NTH %b %Y – %H:%M}'.format(dt).replace('NTH', ordinal(dom)).lower()
			soup = BeautifulSoup(html, "html.parser")
			datas = soup.find('table').find_all('tr') # all rows of results table as list
			for tr in datas:
				TDs = tr.findAll('td')
				if TDs:
					resDate = TDs[1].text.lower().strip()
					if resDate == findDate:
						resDate = drawDt
						result = json.dumps({
							"numbers": [x.strip() for x in TDs[2].text.replace('&nbsp;', '').split('-')],
							"numbers_extra": [],
							"numbers_option": [] # AlexF sent something here, I do not know what
						}).replace(' ','')
						return [result, drawDt] # found, return it
			# not found at current page, go deeper
			page += 1
			if page <= 17: # no more then N pages deeper: 20/page, 48 res/day, 7 days max = 17 pages
				result, drawDt = custom_tatua3(aliasRrc, drawDt, url, urlType, page)
	except Exception as e:
		result = [str(e)]
	return [result, resDate]

# malawilotto ----------------------------------------
def custom_malawilotto(aliasRrc, drawDt, url, urlType):
	result = resDate = False
	# prepare url and cache key
	xdate = '{:%d-%m-%Y}'.format(datetime.strptime(drawDt,'%Y-%m-%d %H:%M:%S')).lower()
	xurl = url.format(xdate) # hoosier URL has date on tail
	cacheKey = f"{aliasRrc}/{xdate}"
	# parse results
	try: # first get draw id
		jsons = getSourceWithCahe(cacheKey, aliasRrc, xurl, urlType)
		datas = json.loads(jsons)
		if datas and datas['allDraws']:
			draw_no = 0
			for dts in datas['allDraws']:
				dt = dts['draw_date'][0:10]
				if dt==drawDt[0:10]: # date found
					draw_no = dts['draw_no']
					break
			if draw_no: # now if id found - get results
				if _tmpfile: os.remove(_tmpfile)
				xurl = url.replace('/all','').replace('?date=','/').format(draw_no) # hoosier URL has date on tail
				cacheKey = f"{aliasRrc}/{draw_no}"
				jsons = getSourceWithCahe(cacheKey, aliasRrc, xurl, urlType)
				datas = json.loads(jsons)
				if datas and datas['results'] and datas['results']['date'][0:10]==drawDt[0:10]:
					resDate = drawDt
					result = json.dumps({
						"numbers": datas['results']['numbers'][0],
						"numbers_extra": datas['results']['numbers'][1],
						"numbers_option": datas['results']['transparency_numbers']
					}).replace(' ','')
				else:
					raise Exception(f"No results returned by draw ID {draw_no}")
		else:
			raise Exception(f"No draw IDs returned for date {drawDt}")
	except Exception as e:
		result = [str(e)]
	return [result, resDate]


if __name__ == '__main__':
	print(f'{__project__}. {__part__}')
