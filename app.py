import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import altair_viewer
import streamlit as st


st.title("米国株価可視化アプリ")
st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
 """)
st.sidebar.write("""表示日数選択""")
days=st.sidebar.slider('日数',1,50,20)

st.write(f"""
### 過去**{days}日間**のGAFA株価""")
@st.cache_data #同じデータなら再度取得しなくともOK
def get_data(days,tickers):
    df=pd.DataFrame()
    for company in tickers.keys():
        tkr=yf.Ticker(tickers[company]) #Ticker object for Apple Inc.アップルの社名の略したもの
        hist=tkr.history(period=f'{days}d')#株価の履歴データを取得するメソッド
      
        hist=hist[['Close']]
        hist.columns=[company]
        hist= hist.T#行と列を入れ替える
        hist.index.name='Name'
        df=pd.concat([df,hist])
    return df
st.sidebar.write("""
## 株価の指定範囲
                 """)
ymin,ymax=st.sidebar.slider('範囲を指定してください。',0.0,3500.0,(0.0,3500.0))


tickers={'apple':'AAPL',
    'facebook':'META',
    'google':'GOOGL',
    'microsoft':'MSFT',
    'netflix':'NFLX',
    'amazon' : 'AMZN'}
df=get_data(days,tickers)

companies=st.multiselect('会社名を選択してください。',list(df.index),['google','amazon','facebook','apple'])

if not companies:
    st.error('少なくとも一社は選んでください。')
else:
    data= df.loc[companies]#カラム名でデータを取得できる
    st.write("### 株価 （USD） ",data.sort_index())
    data=data.T.reset_index().rename(columns={'index':'Date'})
    data=pd.melt(data,id_vars=['Date'],var_name='Name',value_name='Stock Prices(USD)')
    data['Date']=pd.to_datetime(data['Date'])
#data.sort_index()#降順



    chart=(
        alt.Chart(data)
        .mark_line(opacity=0.8,clip=True)
        .encode(
            x=alt.X("Date:T",title="日付"),
            y=alt.Y("Stock Prices(USD):Q",scale=alt.Scale(domain=[ymin,ymax]),title="株価（ドル）"),
            color=alt.Color('Name:N',title='会社名')
        )
    )

    st.altair_chart(chart,use_container_width=True)

