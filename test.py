#test.py
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

ts = TimeSeries(key='G9V53KVNRI8KMSXH', output_format='pandas')
data, meta_data = ts.get_daily(symbol='AAPL')
print(data)
data['4. close'].plot()
plt.title('AAPL')
plt.show()
