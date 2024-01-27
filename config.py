#!/usr/bin/env python3
"""\
config.py - This is a config file
	DB connection
	telegram settings
	Lotteries settings array

Config includes: alias, timezone, local time of draws, sources URL and type
"""

__project__	= "Lotteries Results Scrapper"
__part__	= 'Config'
__author__	= "Sergey V Musenko"
__email__	= "sergey@musenko.com"
__license__	= "MIT"
__copyright__= "© 2024, musenko.com"
__credits__	= ["Sergey Musenko"]
__date__	= "2024-01-15"
__version__	= "0.1"
__status__	= "dev"


# DB config, {} means do not use DB
DBconf = {
#	'host':		'localhost',
#	'user':		'user',
#	'password':	'pswd',
#	'db':		'lottos',
}


JSON_file = 'results.json' # instaed of DB saving/restoring


# notify via Telegram
# see ,.lib/simple_telegram.py how to setup IDs
TapiToken = '' # '' means do not send
TchatID = '' # '' means DO NOT SEND


Lotteries = { # { alias: {settings} }; drawTimeList: [ dow 1..7, localTZtime ]
	# empty url means do not proceed it

	'hoosierlotto': {
		'name':		'Hoosier Lotto',
		'timezone':	'America/Indianapolis',
		'drawTimeList': [
			[3, '23:00'],
			[6, '23:00']
		],
		'url':		'https://hoosierlottery.com/games/draw/past-game-results/1/{}/',
		'urlType':	'HTML'
	},

	'kenyalotto': {
		'name':		'Kenya Lotto',
		'timezone':	'Africa/Nairobi',
		'drawTimeList': [ # draws each hour indeed
			[1, '22:00'],
			[2, '22:00'],
			[3, '22:00'],
			[4, '22:00'],
			[5, '22:00'],
			[6, '22:00'],
			[7, '22:00']
		],
		'url':		'https://mylottokenya.co.ke/results/{}', # official website
		'urlType':	'HTML'
	},

	'philippineslotto': {
		'name':		'Lotto 6/42',
		'timezone':	'Asia/Manila',
		'drawTimeList': [
			[2, '21:00'],
			[4, '21:00'],
			[6, '21:00']
		],
		'url':		'https://www.lottopcso.com/6-42-lotto-result-history-and-summary/',
		'urlType':	'HTML'
	},

	'philippinesmega': {
		'name':		'Megalotto 6/45',
		'timezone':	'Asia/Manila',
		'drawTimeList': [
			[1, '21:00'],
			[3, '21:00'],
			[5, '21:00']
		],
		'url':		'https://www.lottopcso.com/6-45-lotto-result-history-and-summary/',
		'urlType':	'HTML'
	},

	'philippinesultra': {
		'name':		'UltraLotto 6/58',
		'timezone':	'Asia/Manila',
		'drawTimeList': [
			[5, '21:00'],
			[7, '21:00']
		],
		'url':		'https://www.lottopcso.com/6-58-lotto-result-history-and-summary/',
		'urlType':	'HTML'
	},

	'philippinessuper': {
		'name':		'SuperLotto 6/49',
		'timezone':	'Asia/Manila',
		'drawTimeList': [
			[2, '21:00'],
			[4, '21:00'],
			[7, '21:00']
		],
		'url':		'https://www.lottopcso.com/6-49-lotto-result-history-and-summary/',
		'urlType':	'HTML'
	},

	'philippinesgrand': {
		'name':		'GrandLotto 6/55',
		'timezone':	'Asia/Manila',
		'drawTimeList': [
			[1, '21:00'],
			[3, '21:00'],
			[6, '21:00']
		],
		'url':		'https://www.lottopcso.com/6-55-lotto-result-history-and-summary/',
		'urlType':	'HTML'
	},

	'marksix': {
		'name':		'Mark 6',
		'timezone':	'Asia/Hong_Kong',
		'drawTimeList': [
			[2, '21:30'],
			[4, '21:30'],
			[6, '21:30']
		],
		'url':		'https://bet.hkjc.com/contentserver/jcbw/cmc/last30draw.json',
		'urlType':	'JSON'
	},

	'japanlotto6': {
		'name':		'Lotto 6',
		'timezone':	'Japan',
		'drawTimeList': [
			[1, '19:00'], # 2?
			[4, '19:00']  # 5?
		],
		'url':		'https://yesplay.bet/lucky-numbers/japan_loto_6/results', # HTML
		'urlType':	'HTML'
	},

	'taiwanlotto649': {
		'name':		'Lotto 6/49',
		'timezone':	'Asia/Taipei',
		'drawTimeList': [
			[2, '23:00'],
			[5, '23:00']
		],
		'url':		'https://api.taiwanlottery.com/TLCAPIWeB/Lottery/Lotto649Result?period&month={}&pageNum=1&pageSize=50', # like month=2024-01
		'urlType':	'JSON'
	},

	'uk49slotto': { # each day, 2 times a day but not clear
		'name':		'UK 49s',
		'timezone':	'GMT',
		'drawTimeList': [
			[1, '19:49'],
			[2, '19:49'],
			[3, '19:49'],
			[4, '19:49'],
			[5, '19:49'],
			[6, '19:49'],
			[7, '19:49']
		],
		'url':		'https://49s-api.production.sis.onpacegroup.com/numbers/49/games/recent?limit=8', # get last 8 days
		'urlType':	'JSON'
	},

	'goslotto749': { # each day, 7 time a day
		'name':		'Sportloto 7/49',
		'timezone':	'Europe/Moscow',
		'drawTimeList': [
			[1, '22:30'],
			[2, '22:30'],
			[3, '22:30'],
			[4, '22:30'],
			[5, '22:30'],
			[6, '22:30'],
			[7, '22:30']
		],
		'url':		'https://www.stoloto.ru/7x49/archive?mode=date&from={}&to={}', # date[d.m.Y]
		'urlType':	'HTML'
	},

	# Baba Ijebu set: see full list by key "Nigeria" here https://www.magayo.com/lottery-results/
	'africabingo': { # baba-ijebu set:
		'name':		'Bingo',
		'timezone':	'Africa/Lagos',
		'drawTimeList': [
			[1, '15:45'],
			[4, '22:45']
		],
		'url':		'https://www.magayo.com/lotto/nigeria/baba-ijebu-bingo-lotto-results/',
		'urlType':	'HTML'
	},
	'africaenugu': {
		'name':		'Enugu',
		'timezone':	'Africa/Lagos',
		'drawTimeList': [
			[3, '19:15'],
			[7, '15:45']
		],
		'url':		'https://www.magayo.com/lotto/nigeria/baba-ijebu-enugu-lotto-results/',
		'urlType':	'HTML'
	},
	'africainternational': {
		'name':		'International',
		'timezone':	'Africa/Lagos',
		'drawTimeList': [
			[1, '22:45'],
			[4, '19:45']
		],
		'url':		'https://www.magayo.com/lotto/nigeria/baba-ijebu-international-lotto-results/',
		'urlType':	'HTML'
	},
	'africalucky': {
		'name':		'Lucky',
		'timezone':	'Africa/Lagos',
		'drawTimeList': [
			[3, '22:45'],
			[7, '19:15']
		],
		'url':		'https://www.magayo.com/lotto/nigeria/baba-ijebu-lucky-lotto-results/',
		'urlType':	'HTML'
	},
	'africapeoples': {
		'name':		'Peoples',
		'timezone':	'Africa/Lagos',
		'drawTimeList': [
			[1, '12:45'],
			[4, '09:45'],
		],
		'url':		'https://www.magayo.com/lotto/nigeria/baba-ijebu-peoples-lotto-results/',
		'urlType':	'HTML'
	},

	'tatua3': {
		'name':		'Tatua 3',
		'timezone':	'Africa/Nairobi',
		'drawTimeList': [ # it plays each 30 minutes but we use only 21:00 daily
			[1, '21:00'],
			[2, '21:00'],
			[3, '21:00'],
			[4, '21:00'],
			[5, '21:00'],
			[6, '21:00'],
			[7, '21:00'],
		],
		'url':		'http://www.tatuatatu.co.ke/results/{}', # using pages
		'urlType':	'HTML'
	},

	'moroccolotto': {
		'name':		'Maroc Loto',
		'timezone':	'Africa/Lagos', # there is no Marocco tz
		'drawTimeList': [ # 6main + 1more
			[1, '21:00'],
			[3, '21:00'],
			[6, '21:00'],
		],
		'url':		'https://www.magayo.com/lotto/morocco/loto-results/',
		'urlType':	'HTML'
	},

	'lottomaxca': {
		'name':		'Canada Lotto Max',
		'timezone':	'Canada/Eastern', # Ontario
		'drawTimeList': [ # 7 numbers
			[2, '22:30'],
			[5, '22:30'],
		],
		'url':		'https://www.magayo.com/lotto/canada/lotto-max-results/',
		'urlType':	'HTML'
	},

	'malawilotto': { # this is Mega Jackpot Malawi
		'name':		'Malawi Lotto',
		'timezone':	'Africa/Harare',
		'drawTimeList': [
			[2, '21:45'],
			[5, '21:45'],
		],
		'url':		'https://premierloto.mw/last-results/all/mega-jackpot-malawi?date={}', # as 26-12-2023
		'urlType':	'JSON'
	},
}


if __name__ == '__main__':
	print(f'{__project__}. {__part__}')
