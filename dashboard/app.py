import streamlit as st
import polars as pl
import plotly.graph_objects as go

ticker = "AAPL"
df = pl.read_ipc(f"./data/gold/{ticker}_signals.feather").to_pandas()

st.set_page_config(layout="wide")

st.title(f"{ticker} Dashboard")

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name="Close Price"))
fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_20'], name="SMA 20"))
fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], name="SMA 50"))
st.plotly_chart(fig)

st.subheader(f"Relative Strength Index (RSI)")
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=df['Date'], y=df[f"RSI"], name="RSI"))
fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
st.plotly_chart(fig_rsi)

st.write("Most Recent RSI Signals")
st.write(df[(df["Oversold_Signal"] == True) | (df["Overbought_Signal"] == True)][["Date", "RSI", "Oversold_Signal", "Overbought_Signal"]].tail(10))

