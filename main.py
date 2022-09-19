from dotenv import load_dotenv
import os

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# TODO 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
API_KEY_ALPVAN = os.getenv("API_KEY_ALPHAVANTAGE")


# TODO 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.



# TODO 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
