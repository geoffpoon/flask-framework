from flask import Flask, render_template, request, redirect
# import stockTicker
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import Line
from bokeh.models.markers import Circle
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, CDSView
from bokeh.plotting import figure, show, output_file
from bokeh.resources import CDN
from bokeh.embed import file_html

import requests
import simplejson as json
import datetime
import numpy as np
import pandas as pd


app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

# @app.route('/<ticker>')
# def ticker_result(ticker):
#     stockTicker.create_plot(ticker)
#     return render_template("line.html")


####################

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

def create_plot(ticker):
    df, __ = load_dat(ticker)
    df['date'] = pd.to_datetime(df['date'])
    
    # output_file("templates/line.html")
    
    p = figure(x_axis_type="datetime")
    p.line(df.date, df.close,
           line_width = 2)
    p.circle(df.date, df.close,
             fill_color="white", size=8)
    
    p.title.text = "Closing price of %s for the past month" %ticker
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Closing price'
    
    return file_html(p, CDN, "my plot")



# def create_plot(ticker, hover_tool=None,
#                 width=1200, height=300):
#     df, __ = load_dat(ticker)
#     df['date'] = pd.to_datetime(df['date'])


#     plot_dat = {'date': df.date.tolist(), 'close': df.close.tolist()}
#     source = ColumnDataSource(plot_dat)

#     # tools = []
#     # if hover_tool:
#     #     tools = [hover_tool,]
#     # p = figure(x_axis_type="datetime", tools=tools, responsive=True)

#     p = figure(x_axis_type="datetime")    
#     glyph = Line(x='date', y='close', line_width=2)
#     p.add_glyph(source, glyph)
#     glyph = Circle(x='date', y='close', fill_color="white", size=8)
#     p.add_glyph(source, glyph)
    
    
#     p.title.text = "Closing price of %s for the past month" %ticker
#     p.xaxis.axis_label = 'Date'
#     p.yaxis.axis_label = 'Closing price'
    
#     # return file_html(p, CDN, "my plot")
#     return p

# def create_hover_tool():
#     """Generates the HTML for the Bokeh's hover data tool on our graph."""
#     hover_html = """
#       <div>
#         <span class="hover-tooltip">DATE: @date</span>
#       </div>
#       <div>
#         <span class="hover-tooltip">open: @open</span>
#       </div>
#       <div>
#         <span class="hover-tooltip">high: @high</span>
#       </div>
#       <div>
#         <span class="hover-tooltip">low: @low</span>
#       </div>
#       <div>
#         <span class="hover-tooltip">close: @close</span>
#       </div>
#     """
#     return HoverTool(tooltips=hover_html)

####################

@app.route('/<ticker>')
def ticker_result(ticker):
    return create_plot(ticker)


# @app.route('/<ticker>')
# def ticker_result(ticker):
#     # hover = create_hover_tool()
#     # plot = create_plot(ticker, hover_tool=hover)
#     plot = create_plot(ticker)
#     script, div = components(plot)

#     return render_template("chart.html", ticker=ticker, the_div=div, the_script=script)


if __name__ == '__main__':
  app.run(port=33507)
