"""
Testing out intraday data

"""
import datetime

from alpha_vantage.timeseries import TimeSeries


ts = TimeSeries(key='G9V53KVNRI8KMSXH', output_format='pandas')
wmt_price, meta_data = ts.get_intraday(symbol='WMT', interval = '5min', outputsize='full') #get all historic prices
print(wmt_price)