
#%%
import requests
import simplejson as json
import datetime
import numpy as np
import pandas as pd


def load_dat(ticker):
    my_api_key = 'hkyex-7j959_k-uz_KnH'
    
    def func_dateRange(my_api_key):
        ## Load the metadata to find the latest time
        meta_url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES/metadata.json'
        meta_url += '?api_key=%s' %my_api_key
        r = requests.get(meta_url)
        endTime_string = r.json()['datatable']['status']['refreshed_at']
        
        ## Choose start date to be a month earlier than the latest time
        endTime = datetime.datetime.strptime(endTime_string,'%Y-%m-%dT%H:%M:%S.000Z')
        startTime = endTime - datetime.timedelta(days=31)
        
        startDate_s = startTime.strftime('%Y%m%d')
        endDate_s = endTime.strftime('%Y%m%d')
        return startDate_s, endDate_s
    
    startDate_s, endDate_s = func_dateRange(my_api_key)
    
    api_url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json'
    api_url += '?date.gte=%s&date.lt=%s&ticker=%s&api_key=%s' %(startDate_s, endDate_s, ticker, my_api_key)
    ## Perform the request of the url
    r = requests.get(api_url)
    
    ## Put data into a pandas dataframe
    dat = r.json()['datatable']['data']
    col = [x['name'] for x in r.json()['datatable']['columns']]
    df = pd.DataFrame(dat, columns=col)
    
    return df, api_url
    

#%%
from bokeh.plotting import figure, show, output_file
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)

def create_plot(ticker):
    df, __ = load_dat(ticker)
    df['date'] = pd.to_datetime(df['date'])
    
    output_file("templates/line.html")
    
    p = figure(x_axis_type="datetime")
    p.line(df.date, df.close,
           line_width = 2)
    p.circle(df.date, df.close,
             fill_color="white", size=8)
    
    p.title.text = "Closing price of %s for the past month" %ticker
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Closing price'
    
    # return file_html(p, CDN, "my plot")
    show(p)
    
def test():
    ticker = 'GOOG'
    html = create_plot(ticker)
    return html

#%%
