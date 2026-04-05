import config
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import json
import statistics
import yfinance as yf


def transform_to_df(ticker):
    """Takes in historical data as json and returns it as a df"""
    data = yf.download(ticker, start="2022-01-01", end="2026-04-01")
    print(data.head())
    return data


def stategy(history):
    """Calculate MA lines based on current day we are on, so history reflects the data all up until the current day we are on"""
    long_ma = round(history.iloc[-50:].mean(), 2)
    short_ma = round(history.iloc[-20:].mean(), 2)

    # decision
    if short_ma > long_ma:
        return "BUY"
    if short_ma < long_ma:
        return "SELL" 

def Backtester(close, date):
    cash = 100000
    shares = 0
    equity = []
    dates_data = date[49:]
    """Takes in a series of closing prices and applies stategy to each tick"""
    for i in range(49, len(close)):
        # get history up until current day
        history = close.iloc[:i+1]
        res = stategy(history=history)
        price = close.iloc[i]
        
        # buy if no shares
        if res == 'BUY' and shares == 0:
            shares = int(cash / price)
            spent = shares * price
            cash = round(cash - spent,2)

        # sell if we have shares
        elif res == 'SELL' and shares > 0:
            cash += price * shares
            shares = 0

        equity.append(cash + (shares * price))

    plt.plot(dates_data, equity)
    plt.show



        

def run():
    ticker = 'AAPL'
    data = transform_to_df(ticker)
    close_data = data["Close"].squeeze() # turn to series
    dates_data = data.index
    Backtester(close_data,dates_data)
    plt.xticks(rotation=45)
    plt.show()

run()
