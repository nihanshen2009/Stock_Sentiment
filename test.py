"""
The original Big Time Billionaires Tester Program

The purpose of this program is to test out api's

@author: Hanshen Ni

"""
import datetime

import matplotlib.pyplot as plt

from alpha_vantage.timeseries import TimeSeries
from newsapi import NewsApiClient
from pytrends.request import TrendReq




"""
google trends data
"""
pytrends = TrendReq(hl='en-US', tz=360)
kw_list = ["walmart stock"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='US', gprop='')

interest_over_time_df = pytrends.interest_over_time()
print(interest_over_time_df)
# int_plot = interest_over_time_df['walmart stock'].plot(label="Google Interest")

"""
price data
"""
ts = TimeSeries(key='G9V53KVNRI8KMSXH', output_format='pandas')
wmt_price, meta_data = ts.get_daily(symbol='WMT', outputsize='full') #get all historic prices
print(wmt_price)
# price_plot = wmt_price['4. close'].plot(label="Price")




"""
news data
"""
newsapi = NewsApiClient(api_key='ff0f41a5f9804ed69aa4e250e0ae9177')
news_data = newsapi.get_everything(q='walmart',
                                    sources='bloomberg, cnn, nbc-news, the-washington-post, the-wall-street-journal, politico',
                                    from_param='2020-11-13',
                                    to='2020-11-20',
                                    language='en',
                                    page_size=100)

variable_name = news_data['articles']

#get sources
#print(newsapi.get_sources())
#print(news_data.keys())
#print(news_data.items())
#print(news_data['totalResults'])
#print(len(variable_name))
# for i in range(news_data['totalResults']):
#print(variable_name[0])

"""
for i in range(len(variable_name)):
    title = variable_name[i]
    print(title['title'])
"""

"""
plotting
"""
fig, ax = plt.subplots()

ax.plot(wmt_price['4. close'], label='Price', color='r')
ax.set_xlabel('Dates')
ax.set_ylabel('Price')
ax.set_xlim([datetime.datetime(2019,12,1), datetime.datetime(2020,12,1)])

ax2 = ax.twinx()
ax2.plot(interest_over_time_df['walmart stock'], label='Google Interest', color='b')
ax2.set_ylabel('Interest')
ax2.set_ylim([0,100])

plt.title('Walmart Stock Analysis')

plt.show()