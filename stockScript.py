import datetime as dt
from mpl_finance import candlestick_ohlc
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
from matplotlib import style
register_matplotlib_converters()

style.use('ggplot')

start = dt.datetime(2015, 1, 1)
end = dt.datetime.now()


def getYahoo():
    df = web.DataReader("TSLA", 'yahoo', start, end)
    #print(df.head())
    return df

def writeCsv(df, filename):
    df.to_csv(filename)

def readCsvF(df, filename):
    df = pd.read_csv(filename, parse_dates=True, index_col=0)
    return df

def displayGraph(df):
    df_ohlc = df['Adj Close'].resample('10D').ohlc()
    df_volume = df['Volume'].resample('10D').sum()

    df_ohlc.reset_index(inplace=True)
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
    #print(df_ohlc.head())

    #df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
    #df.dropna(inplace=True)
    print(df.head())
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=5, colspan=1, sharex=ax1)
    ax1.xaxis_date()

    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='green')
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
    plt.show()

def main():
    filename = 'test.csv'
    data = getYahoo()
    writeCsv(data, filename)
    df = readCsvF(data, filename)
    print(df.head())

    displayGraph(df)




    #df[['Open', 'Close']].plot()
    #plt.show()

if __name__ == '__main__':
    main()

#df.reset_index(inplace=True)
#df.set_index("Date", inplace=True)
#df = df.drop("Symbol", axis=1)
