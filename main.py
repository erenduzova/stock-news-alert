from dotenv import load_dotenv
import os
import requests

load_dotenv()

# API KEYS
API_KEY_STOCK = os.getenv("API_KEY_ALPHAVANTAGE")

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Stock parameters
URL_STOCK = "https://www.alphavantage.co/query"
ALPHAVANTAGE_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_STOCK
}


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


# TODO 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

last_closes = get_last_two_stock_close()
compare = compare_closes(closes=last_closes)
print(compare)

# TODO 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.



# TODO 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
