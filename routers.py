from asyncio import gather
from datetime import date

from fastapi import APIRouter, Path, Query

from route_functions import (async_converter, close_exchange_date,
                             sync_converter)
from schemas import ConverterInput, ConvertOutput

router = APIRouter(prefix='/converter')


@router.get('/{from_currency}')
def converter(from_currency: str, to_currencies: str, price: float):
    to_currencies = to_currencies.split(',')

    result = []

    for currency in to_currencies:
        response = sync_converter(
            from_currency = from_currency,
            to_currency = currency,
            price = price
        )

        result.append(response)

    return result

@router.get('/async/{from_currency}')
async def async_converter_router(
    from_currency: str = Path(max_length = 3, regex = '^[A-Z]{3}$'), 
    to_currencies: str = Query(max_length = 60, regex = '^[A-Z]{3}(,[A-Z]{3})*$'), 
    price: float = Query(gt=0)
    ):
    to_currencies = to_currencies.split(',')

    coroutines = []

    for currency in to_currencies:
        coro = async_converter(
            from_currency = from_currency,
            to_currency = currency,
            price = price
        )

        coroutines.append(coro)

    result = await gather(*coroutines)
    return result

@router.get('/async/v2/{from_currency}', response_model=ConvertOutput)
async def async_converter_router(
    body: ConverterInput,
    from_currency: str = Path(max_length = 3, regex = '^[A-Z]{3}$'), 
):
    to_currencies = body.to_currencies
    price = body.price

    coroutines = []

    for currency in to_currencies:
        coro = async_converter(
            from_currency = from_currency,
            to_currency = currency,
            price = price
        )

        coroutines.append(coro)

    result = await gather(*coroutines)
    return ConvertOutput(
        message='success',
        data=result
       )


@router.get('/close_daily/{from_currency}$to={to_currency}$in={date}')
async def close_exchange_date_router(
    from_currency: str = Path(max_length = 3, regex = '^[A-Z]{3}$'), 
    to_currency: str = Path(max_length = 60, regex = '^[A-Z]{3}(,[A-Z]{3})*$'), 
    date: str = Path(max_length=10, regex = '^(?:\d{4})-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])$'
) 
    ):

    coroutines = []

    coro = close_exchange_date(
        from_currency = from_currency,
        to_currencies = to_currency,
        date = date
    )

    coroutines.append(coro)

    result = await gather(*coroutines)
    return result