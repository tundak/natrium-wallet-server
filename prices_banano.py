import redis
import urllib3
import certifi
import socket
import rapidjson as json
import time
import os
import sys
import requests

rdata = redis.StrictRedis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, db=int(os.getenv('REDIS_DB', '2')))

currency_list = ["ARS", "AUD", "BRL", "BTC", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR",
                 "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "USD", "ZAR", "SAR", "AED", "KWD"]

#coingecko_url = 'https://api.coingecko.com/api/v3/coins/banano?localization=false&tickers=true&market_data=true&community_data=false&developer_data=false&sparkline=false'
coingecko_url = 'http://api.currencylayer.com/live?access_key=';
#coingecko_url = 'http://localhost/test/curlayer.json';

def coingecko():
    response = requests.get(url=coingecko_url).json()
    if 'quotes' not in response:
        return
    for currency in currency_list:
        try:
            data_name = 'USD'+currency.upper()
            data_name2 = currency.lower()
            #1 BCB price is 0.01 USD (USD value calculated based on IEO price)
            #1USD == 100BCB coins
            if(data_name == 'USDUSD'):
                price_currency = float(0.01)
            else:
                price_currency = float(response['quotes'][data_name])
                price_currency = price_currency*0.01

            print(rdata.hset("prices", "coingecko:banano-"+data_name2,
                             f"{price_currency:.16f}"), "Coingecko BANANO-"+currency, f"{price_currency:.16f}")
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print('exception', exc_type, exc_obj, exc_tb.tb_lineno)
            print("Failed to get price for BCB-"+currency.upper()+" Error")
    # Convert to VES
    usdprice = float(rdata.hget(
        "prices", "coingecko:banano-usd").decode('utf-8'))
    bolivarprice = float(rdata.hget(
        "prices", "dolartoday:usd-ves").decode('utf-8'))
    convertedves = usdprice * bolivarprice
    rdata.hset("prices", "coingecko:banano-ves", f"{convertedves:.16f}")
    print("Coingecko BANANO-VES", rdata.hget("prices",
                                             "coingecko:banano-ves").decode('utf-8'))
    # Convert to NANO
    xrb_prices = []
    for t in response['tickers']:
        if t['target'] == 'XRB':
            xrb_prices.append(float(t['last']))
    nanoprice = sum(xrb_prices) / len(xrb_prices)
    rdata.hset("prices", "coingecko:banano-nano", f"{nanoprice:.16f}")
    print(rdata.hset("prices", "coingecko:lastupdate",
                     int(time.time())), int(time.time()))


coingecko()

print("Coingecko BANANO-USD:", rdata.hget("prices",
                                          "coingecko:banano-usd").decode('utf-8'))
print("Coingecko BANANO-BTC:", rdata.hget("prices",
                                          "coingecko:banano-btc").decode('utf-8'))
print("Coingecko BANANO-NANO:", rdata.hget("prices",
                                           "coingecko:banano-nano").decode('utf-8'))
print("Last Update:          ", rdata.hget(
    "prices", "coingecko:lastupdate").decode('utf-8'))
