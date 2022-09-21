from dotenv import load_dotenv
import os
import requests
from twilio.rest import Client

load_dotenv()

# API KEYS
API_KEY_STOCK = os.getenv("API_KEY_ALPHAVANTAGE")
API_KEY_NEWS = os.getenv("API_KEY_NEWSAPI")

# Company Info
STOCK = "SHC"  # For testing, change to TSLA for tesla
COMPANY_NAME = "Tesla Inc"

# Stock parameters
URL_STOCK = "https://www.alphavantage.co/query"
ALPHAVANTAGE_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_STOCK
}

# News parameters
URL_NEWS = "https://newsapi.org/v2/everything"
NEWS_PARAMETERS = {
    "q": COMPANY_NAME,
    "sortBy": "publishedAt",
    "apiKey": API_KEY_NEWS,
    "pageSize": 3,
    "page": 1
}

# Twilio parameters
TW_AC_SID = os.getenv("TWILIO_SID")
TW_TOKEN = os.getenv("TWILIO_TOKEN")
TW_PHONE = os.getenv("TWILIO_PHONE")
TO_PHONE = os.getenv("TO_PHONE")


def get_last_two_stock_close():
    """
    This function gets the last two day's closing data.
    Returns a tuple of this data.

    :return: last_close, before_last_close
    """
    response = requests.get(url=URL_STOCK, params=ALPHAVANTAGE_PARAMETERS)
    response.raise_for_status()
    stock_data = response.json()["Time Series (Daily)"]
    last_two_days_data = list(stock_data.values())[:2]
    last_close = float(last_two_days_data[0]["4. close"])
    before_last_close = float(last_two_days_data[1]["4. close"])
    return last_close, before_last_close


def compare_closes(closes):
    """
    Compare two closing data and returns difference in percentage.

    :param closes
    :return: diff_per
    """
    diff = closes[0] - closes[1]
    diff_per = (diff / (closes[1] / 100))

    return float("{:.2f}".format(diff_per))


def get_news():
    response = requests.get(url=URL_NEWS, params=NEWS_PARAMETERS)
    response.raise_for_status()
    news_articles_data = response.json()["articles"]
    return news_articles_data


last_closes = get_last_two_stock_close()
compare = compare_closes(closes=last_closes)
if compare <= -5 or compare >= 5:
    print(f"Difference: %{compare}  Get News")
    news_data = get_news()
    print(news_data)
    client = Client(TW_AC_SID, TW_TOKEN)

# TODO 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
