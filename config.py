#!/usr/bin/env python3
"""\
config.py - This is a config file
	Lotteries settings array
	DB connection

Config includes: game id, alias, timezone and local times of draw, sources URL and source type
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


# DB CONFIG:
import socket
if socket.gethostname() == 'sereno':
	DBconf = { # home dev server
		'host':		'localhost',
		'user':		'mserg',
		'password':	'MSerg',
		'db':		'24lottos',
	}
else:
	DBconf = { # production server
		'host':		'localhost',
		'user':		'u2_u24lotom',
		'password':	'9iUoMfF-_Lpu',
		'db':		'db1_u24lotom',
	}


# notify via Telegram, bot: t.me/notifier_24lottos_bot
TapiToken = '6571417860:AAH1gPK78DvjJeruLMcu8-HJ7Mp87fYGJUo' # '' means do not send
TchatID = '-4122674827' # to Private Group
#TchatID = '723039352' # to Sergey personally
#TchatID = '' # '' means DO NOT SEND


Lotteries = { # { alias-rrc: {settings} }; drawTimeList: [ dow 1..7, localTZtime ]
	# empty url means do not proceed it

	'hoosierlotto': {
		'id':		19,
		'name':		'Hoosier Lotto',
		'alias': 	'hoosier-lotto',
		'timezone':	'America/Indianapolis',
		'drawTimeList': [
			[3, '23:00'],
			[6, '23:00']
		],
		'url':		'https://hoosierlottery.com/games/draw/past-game-results/1/{}/',
		'urlType':	'HTML'
	},

	'kenyalotto': {
		'id':		26,
		'name':		'Kenya Lotto',
		'alias': 	'kenya-lotto',
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
		'id':		33,
		'name':		'Lotto 6/42',
		'alias-rrc':'philippineslotto',
		'alias': 	'philippines-lotto-6-42',
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
		'id':		34,
		'name':		'Megalotto 6/45',
		'alias': 	'philippines-megalotto-6-45',
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
		'id':		35,
		'name':		'UltraLotto 6/58',
		'alias': 	'philippines-ultralotto-6-58',
		'timezone':	'Asia/Manila',
		'drawTimeList': [
			[5, '21:00'],
			[7, '21:00']
		],
		'url':		'https://www.lottopcso.com/6-58-lotto-result-history-and-summary/',
		'urlType':	'HTML'
	},

	'philippinessuper': {
		'id':		36,
		'name':		'SuperLotto 6/49',
		'alias': 	'philippines-superlotto-6-49',
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
		'id':		37,
		'name':		'GrandLotto 6/55',
		'alias': 	'philippines-grandlotto-6-55',
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
		'id':		38,
		'name':		'Mark 6',
		'alias': 	'hong-kong-mark-6-lotto',
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
		'id':		39,
		'name':		'Lotto 6',
		'alias': 	'japan-loto-6',
		'timezone':	'Japan',
		'drawTimeList': [
			[1, '19:00'], # 2?
			[4, '19:00']  # 5?
		],
#		'url':		'https://www.mizuhobank.co.jp/takarakuji/loto/loto6/index.html', # REACT
		'url':		'https://yesplay.bet/lucky-numbers/japan_loto_6/results', # HTML
		'urlType':	'HTML'
	},

	'taiwanlotto649': {
		'id':		40,
		'name':		'Lotto 6/49',
		'alias': 	'taiwan-lotto-6-49',
		'timezone':	'Asia/Taipei',
		'drawTimeList': [
			[2, '23:00'],
			[5, '23:00']
		],
#		'url':		'https://www.taiwanlottery.com.tw/lotto/Lotto649/history.aspx', # DEAD!
		'url':		'https://api.taiwanlottery.com/TLCAPIWeB/Lottery/Lotto649Result?period&month={}&pageNum=1&pageSize=50', # like month=2024-01
		'urlType':	'JSON'
	},

	'nigeriagoldenchancelotto': { # each day 7 times a day!
		'id':		71,
		'name':		'Golden Chance Lotto',
		'alias': 	'nigeriagoldenchancelotto', # GOLDENVOGUEFRI, main5 + more5
		'timezone':	'Africa/Lagos',
		'drawTimeList': [ # here we have game ID added
			[1, '8:15', 62],
			[2, '8:00', 64],
			[3, '8:00', 66],
			[4, '8:00', 68],
			[5, '8:00', 69],
			[6, '8:00', 71],
			[7, '8:00', 61],
		],
		'url':		'https://goldenchancelotto.com/backend/api/DailyGameResult/AllGamesPerPeriodPerGame?GameId={}&StartDate={}', # gameID, date[Y-m-d]
		'urlType':	'JSON'
	},

	'uk49slotto': { # each day, 2 times a day but not clear
		'id':		76,
		'name':		'UK 49s',
		'alias': 	'uk49s',
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
		'id':		77,
		'name':		'Sportloto 7/49',
		'alias': 	'sportloto-749',
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
		'id':		28,
		'name':		'Bingo',
		'alias': 	'baba-ijebu',
		'timezone':	'Africa/Lagos',
		'drawTimeList': [
			[1, '15:45'],
			[4, '22:45']
		],
		'url':		'https://www.magayo.com/lotto/nigeria/baba-ijebu-bingo-lotto-results/',
		'urlType':	'HTML'
	},
	'africaenugu': {
		'id':		28,
		'name':		'Enugu',
		'alias': 	'baba-ijebu',
		'timezone':	'Africa/Lagos',
		'drawTimeList': [
			[3, '19:15'],
			[7, '15:45']
		],
		'url':		'https://www.magayo.com/lotto/nigeria/baba-ijebu-enugu-lotto-results/',
		'urlType':	'HTML'
	},
	'africainternational': {
		'id':		28,
		'name':		'International',
		'alias': 	'baba-ijebu',
		'timezone':	'Africa/Lagos',
		'drawTimeList': [
			[1, '22:45'],
			[4, '19:45']
		],
		'url':		'https://www.magayo.com/lotto/nigeria/baba-ijebu-international-lotto-results/',
		'urlType':	'HTML'
	},
	'africalucky': {
		'id':		28,
		'name':		'Lucky',
		'alias': 	'baba-ijebu',
		'timezone':	'Africa/Lagos',
		'drawTimeList': [
			[3, '22:45'],
			[7, '19:15']
		],
		'url':		'https://www.magayo.com/lotto/nigeria/baba-ijebu-lucky-lotto-results/',
		'urlType':	'HTML'
	},
	'africapeoples': {
		'id':		28,
		'name':		'Peoples',
		'alias': 	'baba-ijebu',
		'timezone':	'Africa/Lagos',
		'drawTimeList': [
			[1, '12:45'],
			[4, '09:45'],
		],
		'url':		'https://www.magayo.com/lotto/nigeria/baba-ijebu-peoples-lotto-results/',
		'urlType':	'HTML'
	},

	'tatua3': {
		'id':		28,
		'name':		'Tatua 3',
		'alias': 	'tatua-3',
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
		'id':		28,
		'name':		'Maroc Loto',
		'alias': 	'morocco-lotto',
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
		'id':		59,
		'name':		'Canada Lotto Max',
		'alias': 	'lotto-max-ca',
		'timezone':	'Canada/Eastern', # Ontario
		'drawTimeList': [ # 7 numbers
			[2, '22:30'],
			[5, '22:30'],
		],
		'url':		'https://www.magayo.com/lotto/canada/lotto-max-results/',
		'urlType':	'HTML'
	},

	'malawilotto': { # this is Mega Jackpot Malawi
		'id':		27,
		'name':		'Malawi Lotto',
		'alias': 	'malawi-national-lottery',
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
