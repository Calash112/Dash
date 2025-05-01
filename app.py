import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
import pandas as pd
import time

# Page configuration
st.set_page_config(
    page_title="Financial Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .chart-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Dashboard Settings")
    ticker = st.text_input("Enter Stock Symbol", value="AAPL").upper()
    period = st.select_slider(
        "Time Period",
        options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"],
        value="1y"
    )

# Main content
st.markdown('<h1 class="main-header">Financial Dashboard</h1>', unsafe_allow_html=True)

# Load stock data with retry mechanism
@st.cache_data(ttl=3600)
def load_stock_data(symbol, period, max_retries=3, retry_delay=2):
    for attempt in range(max_retries):
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period)
            
            if hist.empty:
                raise ValueError(f"No data found for symbol {symbol}")
                
            return stock, hist
            
        except Exception as e:
            if "Too Many Requests" in str(e):
                if attempt < max_retries - 1:  # Don't sleep on the last attempt
                    time.sleep(retry_delay)
                    continue
            raise e
    
    raise Exception("Failed to fetch data after multiple attempts")

try:
    with st.spinner('Loading stock data...'):
        stock, hist = load_stock_data(ticker, period)
    
    if len(hist) > 0:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            current_price = hist['Close'][-1]
            prev_price = hist['Close'][-2]
            price_change = ((current_price - prev_price)/prev_price*100)
            st.metric(
                "Current Price", 
                f"${current_price:.2f}", 
                f"{price_change:.2f}%"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Volume", f"{hist['Volume'][-1]:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("52W High", f"${hist['High'].max():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("52W Low", f"${hist['Low'].min():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

        # Price Chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Price Chart")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            name='OHLC'
        ))
        fig.update_layout(
            template='plotly_white',
            xaxis_rangeslider_visible=False,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Volume Chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Volume Analysis")
        fig_volume = go.Figure()
        fig_volume.add_trace(go.Bar(
            x=hist.index,
            y=hist['Volume'],
            name='Volume'
        ))
        fig_volume.update_layout(
            template='plotly_white',
            height=300
        )
        st.plotly_chart(fig_volume, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning(f"No data available for {ticker}. Please check if the symbol is correct.")

except Exception as e:
    if "Too Many Requests" in str(e):
        st.error("We're experiencing high traffic. Please wait a few seconds and try again.")
    elif "Invalid API call" in str(e):
        st.error(f"Invalid stock symbol: {ticker}. Please enter a valid stock symbol.")
    else:
        st.error(f"Error loading data: {str(e)}")
    st.info("Try refreshing the page or using a different stock symbol.") 