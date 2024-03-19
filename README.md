# MonetaryExchangeAPI
## About

This is a microservice that uses the Alpha Vantage API to get real-time currency quotes and perform currency conversions. By entering a specific amount along with the source and destination currencies, the service quickly calculates the converted amount based on current exchange rates

### :clipboard: Tecnologies and Tolls
* Python
* FastAPI
* Alpha Vantage API | [click here](https://www.alphavantage.co/documentation/) for more details
  
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 



What things you need to install the software and how to install them

First, clone the repository
```
git clone https://github.com/WandersoNoleto/MonetaryExchangeAPI.git
```
Install poetry 
```
pip install poetry
```
Activate your virtual environment using Poetry
```
poetry shell
```
Install the dependencies
```
poetry install
```
###### :key: Before starting the service, go to [Alpha Vantage](https://www.alphavantage.co/support/#api-key) to generate your key, create a .env file with an ALPHAVANTAGE_APIKEY variable and put your key there
Use the command to run the service using uvicorn
```
uvicorn main:app --reload
```


# :world_map: ROUTES

## Convert the value from one currency to another

### Request

`GET /converter/{from_currency}?to_currencies={one or more currencies}&price{float}&apikey={ALPHAVANTAGE_APIKEY}`

## Convert the value from one currency to another via JSON

### Request

`GET /converter/v2/{from_currency}`

JSON example:
```
{
  "price": 0,
  "to_currencies": [
    "string"
  ]
}
```

## To know the exchange rate of one currency to another on a particular day

### Request

`GET /converter/close_daily/{from_currency}$to={to_currency}$in={date}`