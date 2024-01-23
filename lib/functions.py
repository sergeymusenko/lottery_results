#!/usr/bin/env python3
"""\
functions.py - This is Lottery functions

"""
__project__	= "Lotteries Results Scrapper"
__part__	= 'Functions lib'
__author__	= "Sergey V Musenko"
__email__	= "sergey@musenko.com"
__license__	= "MIT"
__copyright__= "© 2024, musenko.com"
__credits__	= ["Sergey Musenko"]
__date__	= "2024-01-15"
__version__	= "0.1"
__status__	= "dev"

from config import Lotteries
from datetime import datetime, timedelta #, timezone
import pytz


# get latest result date from DB, save to Lotteries,
# to know results are outdated and needs scrapping
def getLatestResTime(DB):
	# first set None to all
	for _aliasRrc in Lotteries:
		Lotteries[_aliasRrc]['lastresults'] = []
	# then load real datetime
	rows = DB.query("""
		SELECT lotteryname, datetime
		  FROM lotto_rrc_results_archive
		 WHERE datetime>=NOW() - INTERVAL 8 day
		 ORDER by lotteryname, datetime desc
	""")
	if DB.rowcount:
		for r in rows:
			_aliasRrc = r['lotteryname']
			_datetime = r['datetime']
			if _aliasRrc in Lotteries:
				Lotteries[_aliasRrc]['lastresults'].append(str(_datetime))


# date time functions ---
_dtfmt = '%Y-%m-%d %H:%M:%S'
# get now date time as UTC
def get_now_utc():
	return datetime.utcnow().astimezone().strftime(_dtfmt)

# get timezone abbreviation
def get_tz_short(tm, tz):
	localtz = pytz.timezone(tz)
	naive = datetime.strptime(tm, _dtfmt)
	localdt = localtz.localize(naive)
	return localdt.tzname()

# convert time local->UTC
def local_to_utc(tm, tz):
	localtz = pytz.timezone(tz)
	naive = datetime.strptime(tm, _dtfmt)
	localdt = localtz.localize(naive)
	utcdt = localdt.astimezone(pytz.utc).strftime(_dtfmt)
	return utcdt

# convert time UTC->local
def utc_to_local(tm, tz):
	localtz = pytz.timezone(tz)
	naive = datetime.strptime(tm, tfmt)
	dt = pytz.utc.localize(naive).astimezone(localtz).strftime(_dtfmt)
	return dt

# get first day of week date
def week_start_date():
	dt = datetime.utcnow().astimezone()
	weekstart = (dt - timedelta(days=dt.weekday())).replace(hour=0, minute=0, second=0).strftime(_dtfmt)
	return weekstart

# get day of week number of date, Monday=1 so 1..7 (it is not standard!)
def get_dt_dow(dt=False):
	if not dt:
		naive = datetime.today()
	else:
		naive = datetime.strptime(dt, _dtfmt)
	return naive.weekday() + 1

# add delta days to a date
def delta_days(dt, delta):
	added = datetime.strptime(dt, _dtfmt) + timedelta(days=delta)
	return added.strftime(_dtfmt)

# add 1st 2nd 3rd or Nth to day number
def ordinal(n):
	n = int(n)
	date_suffix = ["th", "st", "nd", "rd"]
	if n % 10 in [1, 2, 3] and n not in [11, 12, 13]:
		return str(n) + date_suffix[n % 10]
	else:
		return str(n) + date_suffix[0]
# date time functions --- end

if __name__ == '__main__':
	print(f'{__project__}. {__part__}')
