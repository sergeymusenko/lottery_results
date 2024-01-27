# lottery_results
Lottery Results scrapper.

Lotteries and data sources in `config.py`.<br/>
Saves results into `JSON` file or to `MySQL BD` (disabled by default).<br/>
Note: results are storing for all times so using of JSON file is not good idea. It is just for demonstration.
For production please use DB.<br/>
Sends notification to Telegram. See ./lib/simple_telegram.py how to setup it.

In Python. Uses BeautifulSoup and simple Pymysql wrapper.

https://github.com/sergeymusenko/lottery_results

If you see `Errors` in report: probably data source markup changed or sourse URL not responding any more.<br/>
If you see `Warnings` in report: probably data source is ok but it still not having required draws date. Try later.

**Lotteries:**
> Hoosier Lotto <br/>
Kenya Lotto <br/>
Philippines Lotto 6/42 <br/>
Philippines Megalotto 6/45 <br/>
Philippines UltraLotto 6/58 <br/>
Philippines SuperLotto 6/49 <br/>
Philippines GrandLotto 6/55 <br/>
Hong Kong Mark 6 <br/>
Japan Lotto 6 <br/>
Taiwan Lotto 6/49 <br/>
UK 49s <br/>
Sportloto 7/49 <br/>
Baba Ijebu Bingo <br/>
Baba Ijebu Enugu <br/>
Baba Ijebu International <br/>
Baba Ijebu Lucky <br/>
Baba Ijebu Peoples <br/>
Tatua 3 <br/>
Maroc Loto <br/>
Canada Lotto Max <br/>
Malawi Lotto

**Installation:**
> pip install bs4<br/>
> pip install pymysql
