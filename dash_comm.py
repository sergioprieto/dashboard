#import yahoo_fin.stock_info as si
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

    #BASIC INFO
    st.title("Summary")
    st.write(ticker)
  
    st.write(summ.info)

    #YTD PERFORMANCE
    st.title("YTD Performance")
    st.write(summ.history(period="ytd"))
    
   
            
def tab2():
    if ticker != '-': 
        st.title("Chart")
        st.write(summ.info['shortName'])
    else:
        st.write('Please select a commodity')
    
    c1, c2 = st.columns((1,1))
    
    with c1:    
        duration = st.selectbox("Select duration", 
            ['-', '1Mo', '3Mo', '6Mo', 'YTD','1Y', '3Y','5Y', 'MAX'])          
        
    with c2:
        plot = st.selectbox("Select Plot", ['Line', 'Candle'])
                      
    def getchartdata(ticker):

        SMA = yf.download(ticker, period = 'MAX')
        SMA['SMA'] = SMA['Close'].rolling(50).mean()
        SMA = SMA.reset_index()
        SMA = SMA[['Date', 'SMA']]
        
        if duration != '-':        
            chartdata1 = yf.download(ticker, period = duration)
            chartdata1 = chartdata1.reset_index()
            chartdata1 = chartdata1.merge(SMA, on='Date', how='left')
            return chartdata1

          
        
    if ticker != '-' and duration != '-':

            chartdata = getchartdata(ticker) 
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            #if True:
            if plot == 'Line':
                fig.add_trace(go.Scatter(x=chartdata['Date'], y=chartdata['Close'], mode='lines', 
                                         name = 'Close'), secondary_y = False)
            else:
                fig.add_trace(go.Candlestick(x = chartdata['Date'], open = chartdata['Open'], 
                                             high = chartdata['High'], low = chartdata['Low'], 
                                             close = chartdata['Close'], name = 'Candle'))

            fig.add_trace(go.Scatter(x=chartdata['Date'], y=chartdata['SMA'], 
                mode='lines', name = '50-day SMA'), secondary_y = False)

            fig.add_trace(go.Bar(x = chartdata['Date'], y = chartdata['Volume'], 
                name = 'Volume'), secondary_y = True)

            fig.update_yaxes(range=[0, chartdata['Volume'].max()*3], 
                showticklabels=False, secondary_y=True)
        
            st.plotly_chart(fig)
           
def run():

    comms = [
        'ES=F','YM=F','NQ=F','RTY=F','ZB=F','ZN=F','ZF=F','ZT=F','GC=F','MGC=F'       
        'SI=F','SIL=F','PL=F','HG=F','PA=F','CL=F','HO=F','NG=F','RB=F','BZ=F',
        'B0=F','ZC=F','ZO=F','KE=F','ZR=F','ZM=F','ZL=F','ZS=F','GF=F','HE=F',        
        'LE=F','CC=F','KC=F','CT=F','LBS=F','OJ=F','SB=F']
    ticker_list = ['-'] + comms
    
    global ticker
    ticker = st.sidebar.selectbox("Select a commodity", ticker_list)
    select_tab = st.sidebar.radio("Select tab", ['Summary', 'Chart'])

    global summ
    summ = yf.Ticker(ticker)

    if select_tab == 'Summary':
        tab1()
    elif select_tab == 'Chart':
        tab2()
    
if __name__ == "__main__":
    run()    