import json
import os
import sys
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

main_path = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(main_path, 'app_config.json')
dir_path = os.path.join(main_path, 'data_model\\')
sys.path.insert(0, dir_path)

import data_model.stock_model as sm


def main():
    # Loading the json file
    with open(config_file, "r") as f:
        conf = json.load(f)

        # Loading the database model with the database configuration in the json file
        db_stock = sm.StockModel(conf['database'].format(main_path))
        
        # Setting start and end date
        start_date = datetime(2021,10,13)
        end_date = start_date + timedelta(days=365)

        # Retrieving data from the database
        df_prices = db_stock.get_symbol_prices('MMM', start_date, end_date)
        print(df_prices.head)

        # Calling plotting routines
        gen_plot(df_prices, 'MMM Price', col_labels='day', col_values='close')
        gen_candle_plot(df_prices, 'MMM Price and Candlestick', col_labels='day')


def gen_plot(data, title, col_labels, col_values):
    # clearing any other graph in the plane
    plt.clf()

    # creating the figure with its axes
    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))

    # Setting the title of the figure
    fig.suptitle(title)

    # Plotting the data
    ax1.plot(data[col_labels], data[col_values], label='Close Price')

    # Setting the data legend
    ax1.legend(loc="upper right")
    plt.show()
    

def gen_candle_plot(data, title, col_labels):
    # clearing any other graph in the plane
    plt.clf()

    # creating the figure with its axes
    fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(10, 8), gridspec_kw={'hspace': 0})

    # Setting the title of the figure
    fig.suptitle(title)

    # Plotting the data in the first axes
    ax1.plot(data[col_labels], data['close'], label='Close Price')
    # Setting the data legend in 1st axes
    ax1.legend(loc="upper right")

    # Copying data to a new data frame to add a color column depending on either the price has risen or dropped
    data2 = data.copy()
    data2['color'] = np.where(data['open'] > data['close'], 'tab:red', 'tab:green')

    # Plotting the high v low lines in 2nd axes
    ax2.vlines(data2['day'], data2['high'], data2['low'], color=data2['color'], linewidth=1, label='High | Low')

    # Plotting the open v close lines in 2nd axes
    ax2.vlines(data2['day'], data2['open'], data2['close'], color=data2['color'], linewidth=2, label='Open | Close')
    
    # Setting the data legend in 2nd axes
    ax2.legend(loc="upper right")

    plt.show()


if __name__ == '__main__':
    main()

