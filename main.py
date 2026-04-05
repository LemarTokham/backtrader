import config
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import json



ticker = 'AAPL'

# def fetchData(ticker):
#     """Returns historical data of a given ticker in the form of a pandas dataframe"""
#     # url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={config.API_KEY}'
#     # response = requests.get(url)
#     # data = response.json()['Time Series (Daily)']
#     return data


def transform_to_df():
    """Takes in historical data as json and returns it as a df"""
    with open('data.json') as f:
        data = json.load(f)['Time Series (Daily)']

    df = pd.DataFrame(data)
    df = df.T
    df.reset_index(inplace=True)
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volums']
    df['date'] = pd.to_datetime(df['date'])
    df['close'] = pd.to_numeric(df['close'])
    return df


def plot_data(data):
    sns.set_theme(style='darkgrid')
    sns.lineplot(x='date', y='close', data=data)


def run():
    data = transform_to_df()
    plot_data(data)
    plt.show()

run()
