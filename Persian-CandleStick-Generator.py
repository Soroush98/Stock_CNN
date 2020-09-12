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
my_headers = [ 'PDate','PriceFirst', 'PriceMax', 'PriceMin', 'ClosePrice']
my_dtypes = {'PriceFirst': 'float', 'PriceMax': 'float', 'PriceMin': 'float',
             'ClosePrice': 'float'}
name = 'wabmelat_test'
loaded_data = pd.read_csv('Data/' + name+ '.csv', sep=',', header=1, names=my_headers,
                          dtype=my_dtypes)
loaded_data = loaded_data.iloc[::-1]
# Convert 'Timestamp' to 'float'.
#   candlestick_ohlc needs time to be in float days format - see date2num().

# Re-arrange data so that each row contains values of a day: 'date','open','high','low','close'.
y_label = []
quotes = [tuple(x) for x in loaded_data[[ 'PDate','PriceFirst', 'PriceMax', 'PriceMin', 'ClosePrice']].values]
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
    # if (quotes[i+chunk][4]   >= quotes[i][4] * 1.10):
    #     plt.savefig('N_test/0/' + name +'-PIC' + str(i) + '.png',pad_inches = 0,Transparent = 'False')
    # elif (quotes[i+chunk][4]   < quotes[i ][4] * 1.10 and quotes[i+chunk][4] >= quotes[i][4]):
    #     plt.savefig('N_test/1/' + name +'-PIC' + str(i) + '.png',pad_inches = 0,Transparent = 'False')
    # elif (quotes[i +  chunk ][4] > quotes[i][4] * 0.90 and quotes[i + chunk ][4] <
    #           quotes[i][4]):
    #     plt.savefig('N_test/2/' + name + '-PIC' + str(i) + '.png', pad_inches=0, Transparent='False')
    # else:
    #     plt.savefig('N_test/3/' + name + '-PIC' + str(i) + '.png', pad_inches=0, Transparent='False')
    # if (quotes[i+chunk-1][4] < quotes[i + chunk-1 + 7][4]):
    #     plt.savefig('N_test/1/' + name +'-PIC' + str(i) + '.png',pad_inches = 0,Transparent = 'False')
    # else:
    #     plt.savefig('N_test/0/' + name + '-PIC' + str(i) + '.png', pad_inches=0, Transparent='False')

    if (quotes[i][4] < quotes[i + chunk][4]):
        plt.savefig('Per_test/1/' + name +'-PIC' + str(i) + '.png',pad_inches = 0,Transparent = 'False')
    else:
        plt.savefig('Per_test/0/' + name + '-PIC' + str(i) + '.png', pad_inches=0, Transparent='False')
    plt.close(fig)
