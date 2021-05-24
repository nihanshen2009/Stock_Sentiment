import pandas as pd
import quandl, math, datetime
import numpy as np
from sklearn import preprocessing, svm
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style


from alpha_vantage.timeseries import TimeSeries

# ts = TimeSeries(key='G9V53KVNRI8KMSXH', output_format='pandas')
# df, meta_data = ts.get_daily(symbol='GOOGL') #get all historic prices

style.use('ggplot')

quandl.ApiConfig.api_key = "tMzM9MFfUH9zMUxEpNxq"
df = quandl.get('WIKI/GOOGL')

df = df[['Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume',]]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

df = df[['Adj. Close','HL_PCT','PCT_change', 'Adj. Volume']]


forcast_col = 'Adj. Close'
df.fillna(-99999, inplace=True)

# number of days out
forcast_out = int(math.ceil(0.01*len(df)))

df['label'] = df[forcast_col].shift(-forcast_out)


# X: features, y: labels
X = np.array(df.drop(['label'],1))
X = preprocessing.scale(X)
X = X[:-forcast_out]
X_lately = X[-forcast_out:]
df.dropna(inplace=True)
y = np.array(df['label']) 
y = np.array(df['label'])

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

clf = LinearRegression(n_jobs=-1)
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)

forcast_set = clf.predict(X_lately)
# print(forcast_set, accuracy, forcast_out)

df['Forcast'] = np.nan
last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
#print(last_unix)
one_day = 86400
next_unix = last_unix + one_day

for i in forcast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]
    print([np.nan for _ in range(len(df.columns)-1)] + [i])

df['Adj. Close'].plot()
df['Forcast'].plot()
plt.title('GOOGL Backtest Forcast')
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
# plt.show()
