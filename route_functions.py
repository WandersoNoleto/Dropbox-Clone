
from os import getenv

import aiohttp

from fastapi import HTTPException

ALPHAVANTAGE_APIKEY = getenv('ALPHAVANTAGE_APIKEY')


async def async_converter(from_currency: str, to_currency: str, price: float):
    url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={ALPHAVANTAGE_APIKEY}'
    print(to_currency, from_currency, price, ALPHAVANTAGE_APIKEY)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url = url) as response:
                data = await response.json()

    except Exception as error:
        raise HTTPException(status_code = 400, detail = error)
    
    print(data)
    if "Realtime Currency Exchange Rate" not in data:
        raise HTTPException(status_code = 400, detail = "Realtime Currency Exchange Rate not in response")
    
    exchange_rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    return {to_currency: price * exchange_rate}

async def close_exchange_date(from_currency: str, to_currencies: str, date: str):
    url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={from_currency}&to_symbol={to_currencies}&&apikey={ALPHAVANTAGE_APIKEY}'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url = url) as response:
                data = await response.json()

    except Exception as error:
        raise HTTPException(status_code = 400, detail = error)
    

    if "Time Series FX (Daily)" not in data:
        raise HTTPException(status_code = 400, detail = "Time Series FX (Daily) not in response")
    
    exchange_date = float(data['Time Series FX (Daily)'][date]["4. close"])
    
    return exchange_date