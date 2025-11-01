import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt


#aapl=yf.Ticker("AAPL") #Ticker object for Apple Inc.アップルの社名の略したもの
days=20
tickers={
    'apple':'AAPL',
     'microsoft':'MSFT',
     'amazon' : 'AMZN',
     'alphabet':'GOOGL',
    'meta':'META'   
}
def get_data(days,tickers):
    df=pd.DataFrame()
    for company in tickers.keys():


        tkr=yf.Ticker(tickers[company])

        hist=tkr.history(period=f'{days}d')#株価の履歴データを取得するメソッド
        hist.index=hist.index.strftime('%d %B %Y')
        hist=hist[['Close']]#取得したいindexを指定する
        hist.columns=[company]
        hist=hist.T
        hist.index.name='Name'
        df=pd.concat([df,hist])
    return df





#print(get_data(days,tickers))#reset_index グラフを正しい表示にする
df=get_data(days,tickers)
compiles=['apple','meta']
data=df.loc[compiles]
data=data.T.reset_index()
data=data.rename(columns={'index':'Date'})
data['Date']=pd.to_datetime(data['Date'])

data= pd.melt(data,id_vars=['Date'],var_name='Name',value_name='Stock Prices(USD)'
).sort_values('Date')
data.sort_index()
print(data)

chart=(
    alt.Chart(data)
    .mark_line(opacity=0.8)
    .encode(
        x="Date:T",
        y=alt.Y("Stock Prices(USD):Q",stack=None),
        color='Name:N')
)

chart

