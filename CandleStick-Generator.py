import pandas as pd
from mpl_finance import candlestick_ohlc

import matplotlib

matplotlib.use('Agg')  # Bypass the need to install Tkinter GUI framework
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Avoid FutureWarning: Pandas will require you to explicitly register matplotlib converters.
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Load data from CSV file.
##########################
my_headers = ['date', 'open', 'high', 'low', 'close','adj close','volume']
my_dtypes = {'date': 'str', 'open': 'float', 'high': 'float', 'low': 'float',
             'close': 'float', 'volume': 'int'}
my_parse_dates = ['date']
name = 'AAPL_test'
loaded_data = pd.read_csv('Data/' + name+ '.csv', sep=',', header=1, names=my_headers,
                          dtype=my_dtypes, parse_dates=my_parse_dates)

# Convert 'Timestamp' to 'float'.
#   candlestick_ohlc needs time to be in float days format - see date2num().
loaded_data['date'] = [mdates.date2num(d) for d in loaded_data['date']]

# Re-arrange data so that each row contains values of a day: 'date','open','high','low','close'.
y_label = []
quotes = [tuple(x) for x in loaded_data[['date', 'open', 'high', 'low', 'close']].values]
chunk = 20
dimension = 50
for i in range(0,len(quotes) - chunk,1):
    my_dpi = 96
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(dimension / my_dpi,
                              dimension / my_dpi), dpi=my_dpi)
    ax1 = fig.add_subplot(1, 1, 1)
    candlestick_ohlc(ax1, quotes[i:i + chunk], width=1, colorup='#77d879', colordown='#db3f3f', )
    ax1.grid(False)
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    ax1.xaxis.set_visible(False)
    ax1.yaxis.set_visible(False)
    ax1.axis('off')
    # if (quotes[i+2*chunk-1][4]   >= quotes[i + chunk - 1][4] * 1.15):
    #     plt.savefig('N_train/0/' + name +'-PIC' + str(i) + '.png',pad_inches = 0,Transparent = 'False')
    # elif (quotes[i+2*chunk-1][4]   < quotes[i + chunk - 1][4] * 1.15 and quotes[i+2*chunk-1][4] >= quotes[i + chunk - 1][4]):
    #     plt.savefig('N_train/1/' + name +'-PIC' + str(i) + '.png',pad_inches = 0,Transparent = 'False')
    # elif (quotes[i + 2 * chunk - 1][4] > quotes[i + chunk - 1][4] * 0.85 and quotes[i + 2 * chunk - 1][4] <
    #           quotes[i + chunk - 1][4]):
    #     plt.savefig('N_train/2/' + name + '-PIC' + str(i) + '.png', pad_inches=0, Transparent='False')
    # else:
    #     plt.savefig('N_train/3/' + name + '-PIC' + str(i) + '.png', pad_inches=0, Transparent='False')
    if (quotes[i+chunk-1][4] < quotes[i + 2*chunk-1][4]):
        plt.savefig('N_test/1/' + name +'-PIC' + str(i) + '.png',pad_inches = 0,Transparent = 'False')
    else:
        plt.savefig('N_test/0/' + name + '-PIC' + str(i) + '.png', pad_inches=0, Transparent='False')

    # if (quotes[i][4] < quotes[i + chunk][4]):
    #     plt.savefig('Test/1/' + name +'-PIC' + str(i) + '.png',pad_inches = 0,Transparent = 'False')
    # else:
    #     plt.savefig('Test/0/' + name + '-PIC' + str(i) + '.png', pad_inches=0, Transparent='False')
    plt.close(fig)
