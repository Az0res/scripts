from datetime import date, timedelta
from time import sleep

import pandas as pd
import yfinance as yf

ticker = "AAPL"

# we start 5 years ago
year = timedelta(days=365)
years_ago = year * 5
DOWNLOAD_INTERVAL = timedelta(days=55)
TICKER_DATA_INTERVAL = "90m"

START_DATE_d = date.today() - years_ago
END_DATE_d = START_DATE_d + DOWNLOAD_INTERVAL

def get_column_from_csv(file, col_name):
    # Try to get the file and if it doesn't exist issue a warning
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        print("File Doesn't Exist")
    else:
        return df[col_name]


# get all tickers
#tickers = get_column_from_csv("D:/Python for Finance/Wilshire-5000-Stocks.csv", "Ticker")
tickers=["AAPL","GOOG","TSL"]
print(len(tickers))
failed_tickers=[]

for t in tickers:
    the_file = "tickers" + ticker.replace(".", "_") + '.csv'
    try:
        print("Get Data for : ", ticker)
        stock = yf.Ticker(ticker)
        # get all data for each ticker
        tmp_st_date=START_DATE_d
        tmp_end_date=END_DATE_d

        while tmp_end_date < date.today():
            df = stock.history(ticker, start=tmp_st_date.strftime("%Y-%m-%d"), end=tmp_end_date.strftime("%Y-%m-%d"),
                               interval=TICKER_DATA_INTERVAL)
            tmp_st_date = tmp_end_date
            tmp_end_date = tmp_st_date + DOWNLOAD_INTERVAL
            df.to_csv(the_file, mode='a')
            sleep(2)
        print(the_file, " Saved")
    except Exception as e:
        print("Could not download ticker {}: \t{}".format(t, e))
        failed_tickers.append(t)

print(failed_tickers)
