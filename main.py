from dotenv import load_dotenv
import os
import requests
from twilio.rest import Client

load_dotenv()

# API KEYS
API_KEY_STOCK = os.getenv("API_KEY_ALPHAVANTAGE")
API_KEY_NEWS = os.getenv("API_KEY_NEWSAPI")

# Company Info
STOCK = "TSLA"
COMPANY_NAME = "tesla"

# Control Percentage
CONTROL_PER = 5

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
    Compare two closing data and returns difference in percentage and symbol for direction of difference.

    :param closes
    :return: diff_per, diff_direction
    """
    diff = closes[0] - closes[1]
    diff_per = (diff / (closes[1] / 100))
    diff_direction = "-"
    if diff < 0:
        diff_direction = "🔻"
        diff_per = -diff_per
    elif diff > 0:
        diff_direction = "🔺"

    return float("{:.2f}".format(diff_per)), diff_direction


def get_news():
    """
    Gets news data using newsapi and returns news articles data in json format.

    :return: news_articles_data
    """
    response = requests.get(url=URL_NEWS, params=NEWS_PARAMETERS)
    response.raise_for_status()
    news_articles_data = response.json()["articles"]
    return news_articles_data


def create_msg_body(news_func):
    """
    Creates and returns message body(string) for sms.

    :param news_func:
    :return: msg_body_func
    """
    headline = news_func["title"]
    brief = news_func["description"]
    msg_body_func = f"{STOCK}: {diff_symbol} {diff_perc}%\nHeadline: {headline}\nBrief: {brief}"
    return msg_body_func


def send_sms(sms_msg_body):
    """
    This function takes message body and sends sms through twilio api.

    :param sms_msg_body:
    """
    message = client.messages \
        .create(
            body=sms_msg_body,
            from_=TW_PHONE,
            to=TO_PHONE
        )


last_closes = get_last_two_stock_close()
compare = compare_closes(closes=last_closes)
diff_perc = compare[0]
diff_symbol = compare[1]
if diff_perc >= CONTROL_PER:
    news_data = get_news()
    client = Client(TW_AC_SID, TW_TOKEN)
    for news in news_data:
        msg_body = create_msg_body(news_func=news)
        send_sms(sms_msg_body=msg_body)
