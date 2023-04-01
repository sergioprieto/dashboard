import yahoo_fin.stock_info as si
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def tab1():
    
    st.title("Summary")
    st.write("Select ticker")
    st.write(ticker)

    def getsummary(ticker):
            table = si.get_quote_table(ticker, dict_result = False)
            return table 
        
    c1, c2 = st.columns((1,1))
    with c1:        
        if ticker != '-':
            summary = getsummary(ticker)
            summary['value'] = summary['value'].astype(str)
            showsummary = summary.iloc[[14, 12, 5, 2, 6, 1, 16, 3],]
            showsummary.set_index('attribute', inplace=True)
            st.dataframe(showsummary)
            
            
    with c2:        
        if ticker != '-':
            summary = getsummary(ticker)
            summary['value'] = summary['value'].astype(str)
            showsummary = summary.iloc[[11, 4, 13, 7, 8, 10, 9, 0],]
            showsummary.set_index('attribute', inplace=True)
            st.dataframe(showsummary)
            
        
    @st.cache_data 
    def getstockdata(ticker):
        stockdata = yf.download(ticker, period = 'MAX')
        return stockdata
        
    if ticker != '-':
            chartdata = getstockdata(ticker) 
                       
            fig = px.area(chartdata, chartdata.index, chartdata['Close'])
            
                     

            fig.update_xaxes(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1M", step="month", stepmode="backward"),
                        dict(count=3, label="3M", step="month", stepmode="backward"),
                        dict(count=6, label="6M", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1Y", step="year", stepmode="backward"),
                        dict(count=3, label="3Y", step="year", stepmode="backward"),
                        dict(count=5, label="5Y", step="year", stepmode="backward"),
                        dict(label = "MAX", step="all")
                    ])
                )
            )
            st.plotly_chart(fig)
            
     

def tab2():
    st.title("Chart")
    st.write(ticker)
    
    st.write("Set duration to '-' to select date range")
    
    c1, c2, c3, c4,c5 = st.columns((1,1,1,1,1))
    
    with c1:
        
        start_date = st.date_input("Start date", datetime.today().date() - timedelta(days=30))
        
    with c2:
        
        end_date = st.date_input("End date", datetime.today().date())        
        
    with c3:
        
        duration = st.selectbox("Select duration", ['-', '1Mo', '3Mo', '6Mo', 'YTD','1Y', '3Y','5Y', 'MAX'])          
        
    with c4: 
        
        inter = st.selectbox("Select interval", ['1d', '1mo'])
        
    with c5:
        
        plot = st.selectbox("Select Plot", ['Line', 'Candle'])
             
    @st.cache_data             
    def getchartdata(ticker):
        SMA = yf.download(ticker, period = 'MAX')
        SMA['SMA'] = SMA['Close'].rolling(50).mean()
        SMA = SMA.reset_index()
        SMA = SMA[['Date', 'SMA']]
        
        if duration != '-':        
            chartdata1 = yf.download(ticker, period = duration, interval = inter)
            chartdata1 = chartdata1.reset_index()
            chartdata1 = chartdata1.merge(SMA, on='Date', how='left')
            return chartdata1
        else:
            chartdata2 = yf.download(ticker, start_date, end_date, interval = inter)
            chartdata2 = chartdata2.reset_index()
            chartdata2 = chartdata2.merge(SMA, on='Date', how='left')                             
            return chartdata2
          
        
    if ticker != '-':
            chartdata = getchartdata(ticker) 
            
                       
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            if plot == 'Line':
                fig.add_trace(go.Scatter(x=chartdata['Date'], y=chartdata['Close'], mode='lines', 
                                         name = 'Close'), secondary_y = False)
            else:
                fig.add_trace(go.Candlestick(x = chartdata['Date'], open = chartdata['Open'], 
                                             high = chartdata['High'], low = chartdata['Low'], close = chartdata['Close'], name = 'Candle'))
              
                    
            fig.add_trace(go.Scatter(x=chartdata['Date'], y=chartdata['SMA'], mode='lines', name = '50-day SMA'), secondary_y = False)
            
            fig.add_trace(go.Bar(x = chartdata['Date'], y = chartdata['Volume'], name = 'Volume'), secondary_y = True)

            fig.update_yaxes(range=[0, chartdata['Volume'].max()*3], showticklabels=False, secondary_y=True)
        
      
            st.plotly_chart(fig)
           

def tab3():
     st.title("Statistics")
     st.write(ticker)
     c1, c2 = st.columns(2)
     
     with c1:
         st.header("Valuation Measures")
         def getvaluation(ticker):
                 return si.get_stats_valuation(ticker)
    
         if ticker != '-':
                valuation = getvaluation(ticker)
                valuation[1] = valuation[1].astype(str)
                valuation = valuation.rename(columns = {0: 'Attribute', 1: ''})
                valuation.set_index('Attribute', inplace=True)
                st.table(valuation)
                
        
         st.header("Financial Highlights")
         st.subheader("Fiscal Year")
         
         def getstats(ticker):
                 return si.get_stats(ticker)
         
         if ticker != '-':
                stats = getstats(ticker)
                stats['Value'] = stats['Value'].astype(str)
                stats.set_index('Attribute', inplace=True)
                st.table(stats.iloc[29:31,])
                
        
         st.subheader("Profitability")
         
         if ticker != '-':
                stats = getstats(ticker)
                stats['Value'] = stats['Value'].astype(str)
                stats.set_index('Attribute', inplace=True)
                st.table(stats.iloc[31:33,])
                    
                
         st.subheader("Management Effectiveness")
         
         if ticker != '-':
                stats = getstats(ticker)
                stats['Value'] = stats['Value'].astype(str)
                stats.set_index('Attribute', inplace=True)
                st.table(stats.iloc[33:35,])
         
         
                
         st.subheader("Income Statement")
         
         if ticker != '-':
                stats = getstats(ticker)
                stats['Value'] = stats['Value'].astype(str)
                stats.set_index('Attribute', inplace=True)
                st.table(stats.iloc[35:43,])  
            
         
         st.subheader("Balance Sheet")
         
         if ticker != '-':
                stats = getstats(ticker)
                stats['Value'] = stats['Value'].astype(str)
                stats.set_index('Attribute', inplace=True)
                st.table(stats.iloc[43:49,])
         
         st.subheader("Cash Flow Statement")
         
         if ticker != '-':
                stats = getstats(ticker)
                stats['Value'] = stats['Value'].astype(str)
                stats.set_index('Attribute', inplace=True)
                st.table(stats.iloc[49:,])
         
                      
     with c2:
         st.header("Trading Information")
         
         
         st.subheader("Stock Price History")
                  
         if ticker != '-':
                stats = getstats(ticker)
                stats['Value'] = stats['Value'].astype(str)
                stats.set_index('Attribute', inplace=True)
                st.table(stats.iloc[:7,])
         
         st.subheader("Share Statistics")
                  
         if ticker != '-':
                stats = getstats(ticker)
                stats['Value'] = stats['Value'].astype(str)
                stats.set_index('Attribute', inplace=True)
                st.table(stats.iloc[7:19,])
         
         st.subheader("Dividends & Splits")
                  
         if ticker != '-':
                stats = getstats(ticker)
                stats['Value'] = stats['Value'].astype(str)
                stats.set_index('Attribute', inplace=True)
                st.table(stats.iloc[19:29,])
         
  
def run():

    ticker_list = ['-'] + si.tickers_sp500()
    
    global ticker
    ticker = st.sidebar.selectbox("Select a ticker", ticker_list)
    
    select_tab = st.sidebar.radio("Select tab", ['Summary', 'Chart', 'Statistics'])

    if select_tab == 'Summary':
        tab1()
    elif select_tab == 'Chart':
        tab2()
    elif select_tab == 'Statistics':
        tab3()
    
if __name__ == "__main__":
    run()    