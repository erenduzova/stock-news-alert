# rain-alert
SMS alert app for stock news monitoring.

## Table of Contents
* [General Info](#general-info)
* [Built With](#built-with)
* [Environment Variables](#environment-variables)
* [Control Percentage](#control-percentage)
* [Company Info](#company-info)

## General Info
This project is a simple alert app which sends sms the last 3 news about company if stock changes more than specified value (default = %5).

## Built With
Project is created with:
* Python version: 3.10
* python-dotenv version: 0.21.0
* requests version: 2.28.1
* twilio version: 7.14.0

## Environment Variables
I used ".env" file for environment variables for security reasons.<br />
In this file I stored my API keys and some personal information.<br />
You should create this file with your information or write yours to the main.py and do not use ".env" file.<br />
```
API_KEY_ALPHAVANTAGE=***********
API_KEY_NEWSAPI=****************
TWILIO_SID=*********************
TWILIO_TOKEN=*******************
TWILIO_PHONE=*******************
TO_PHONE=***********************
```

## Control Percentage
Control percentage for alert system default value = 5
```
# Control Percentage
CONTROL_PER = 5
```

## Company Info
STOCK variable is used for getting data of the stock; COMPANY_NAME variable is used for getting news of the company.<br />
Change these variables if you want to look for another company.<br />
```
# Company Info
STOCK = "TSLA"
COMPANY_NAME = "tesla"
```
