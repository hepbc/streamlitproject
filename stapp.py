# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 08:53:02 2021

@author: hepbc
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
#import string
#from sklearn.metrics.pairwise import cosine_similarity
#import quandl as ql
import datetime
import matplotlib.pyplot as plt
#import pickle
#import torch
#from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
#from transformers import BertTokenizer, BertForTokenClassification##, AdamW

#ql.ApiConfig.api_key = "-QR-L74dEexC6-BXVm2P"

#model_name = "bert-base-uncased"
#DIR = "./MFportfoliodata/"
#ek.set_app_key(APP_KEY)
benchmark_dict = {"Nifty 50": "^NSEI", "Nifty 500": "^CRSLDX", "Nifty Midcap 100": "NIFTY_MIDCAP_100.NS"}
#years = mdates.YearLocator()   # every year
#months = mdates.MonthLocator(interval=6, bymonthday=28)  # qtr end month
#yearsFmt = mdates.DateFormatter('%Y')
#monthsFmt = mdates.DateFormatter('%b%y')
#CurrQ = 3
#CurrY = 2020

def main():
    
    s = ["Thousands", "Ten thousands", "Lakhs", "Millions", "Crores", "Ten crores", "Billions"]
    scale = {}
    for i in range(3, 10):
        scale[i]=s[i-3]
    d1 = np.nan
    d2 = np.nan      
    
    stocks = pd.read_excel("codes.xlsx", sheet_name="Stocks")
    benchmarks = pd.read_excel("codes.xlsx", sheet_name="Index")
    st.title("Toy deployment")
    st.sidebar.header("Configuration")
    #country = st.sidebar.selectbox("Select country:", ["India", "USA"])
    country = "India"
    #FX = st.sidebar.selectbox("Select currency:", ["INR", "USD"])
    FX="INR"
    perFlag = st.sidebar.radio("Select performance type", ["Absolute", "Point to point"])
    if perFlag == "Absolute":
        Abs = True
        d1 = datetime.date(2016, 6, 1)
        d2 = datetime.date(2021, 5, 31)
    else:
        Abs = False
    if Abs == False:
        d1 = st.sidebar.date_input("Select start date for performance period")
        d2 = st.sidebar.date_input("Select end date for performance period")
        if d1 > d2:
            st.sidebar.write("Start date should be earlier than end date")
        if d2 > datetime.date(2021, 5, 31):
            d2 = datetime.date(2021, 5, 31)

    stock = st.sidebar.radio("Select stock", stocks["Company"].tolist())
    benchmark = st.sidebar.radio("Select benchmark", benchmarks["Index"].tolist())
    Scale = st.sidebar.slider("Scale:", min_value=3, max_value=9, value=6)
    st.sidebar.markdown(FX + " " + scale[Scale])
    st.write(stock, benchmark)
    stock_code = stocks[stocks["Company"]==stock].iloc[0,1]
    benchmark_code = benchmark_dict[benchmark]
    st.write(stock_code, benchmark_code)

    stock_price = yf.download(stock_code, start=d1, end=d2)
    index_price = yf.download(benchmark_code, start=d1, end=d2)
    fig, ax = plt.subplots()
    ax.plot(stock_price["Adj Close"], color="red")
    ax2=ax.twinx()
    ax2.plot(index_price["Adj Close"])
    st.pyplot(fig)
if __name__ == "__main__":
    main()