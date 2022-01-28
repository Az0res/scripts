from datetime import date, timedelta
from time import sleep

import pandas as pd
import yfinance as yf


ticker="AAPL"


#we start 5 years ago
year = timedelta(days=365)
years_ago = year * 5
INTERVAL = timedelta(days= 50)

START_DATE_d = date.today() - years_ago
END_DATE_d = START_DATE_d + INTERVAL

while END_DATE_d < date.today():
    df = yf.download(ticker, start=START_DATE_d.strftime("%Y-%m-%d"), end=END_DATE_d.strftime("%Y-%m-%d"), interval="90m")
    START_DATE_d = END_DATE_d
    END_DATE_d = START_DATE_d + INTERVAL
    sleep(2)
