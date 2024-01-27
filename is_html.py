#!/usr/bin/env python3
"""\
This is for testing if URL returns a plain HTML/JSON or
it is a REACT website (hard to use or useless)
"""

__project__	= "Lotteries Results Scrapper"
__part__	= 'Test URL if it returns data'
__author__	= "Sergey V Musenko"
__email__	= "sergey@musenko.com"
__license__	= "MIT"
__copyright__= "© 2024, musenko.com"
__credits__	= ["Sergey Musenko"]
__date__	= "2024-01-15"
__version__	= "0.1"

import requests
import time

url2test = 'https://lottolyzer.com/home/taiwan/lotto-649/number-view'
logfile = 'is_html.html'

start = time.time()
print(f'URL: {url2test}')

headers = {'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'}
page = requests.get(url2test, timeout=5, headers=headers)
print(f"HTTP: {page.status_code}")

html = page.content
with open(logfile, "wb") as _log: _log.write(html)

passed = round(time.time() - start, 3)
print(f'Time: {passed} s')
print(f'See: {logfile}')
