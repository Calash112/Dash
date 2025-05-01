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

# Load stock data with improved error handling
@st.cache_data(ttl=1800)  # Cache for 30 minutes
def load_stock_data(symbol, period, max_retries=3, retry_delay=2):
    for attempt in range(max_retries):
        try:
            # Create Ticker object
            stock = yf.Ticker(symbol)
            
            # Verify the symbol exists by checking info
            info = stock.info
            if not info or 'regularMarketPrice' not in info:
                raise ValueError(f"No data available for symbol {symbol}")
            
            # Get historical data
            hist = stock.history(period=period)
            if hist.empty:
                raise ValueError(f"No historical data found for symbol {symbol}")
            
            return stock, hist, info
            
        except Exception as e:
            if "Too Many Requests" in str(e):
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
            elif attempt < max_retries - 1:
                time.sleep(1)  # Brief delay between retries
                continue
            raise e

try:
    with st.spinner('Loading stock data...'):
        stock, hist, info = load_stock_data(ticker, period)
    
    # Display company info
    st.subheader(f"{info.get('longName', ticker)} ({ticker})")
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
    with col_info2:
        st.write(f"**Currency:** {info.get('currency', 'USD')}")
        st.write(f"**Market Cap:** ${info.get('marketCap', 0):,.0f}")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        current_price = info.get('regularMarketPrice', hist['Close'][-1])
        prev_close = info.get('previousClose', hist['Close'][-2])
        price_change = ((current_price - prev_close)/prev_close*100)
        st.metric(
            "Current Price", 
            f"${current_price:.2f}", 
            f"{price_change:.2f}%"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Volume", f"{info.get('volume', hist['Volume'][-1]):,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("52W High", f"${info.get('fiftyTwoWeekHigh', hist['High'].max()):.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("52W Low", f"${info.get('fiftyTwoWeekLow', hist['Low'].min()):.2f}")
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

except ValueError as ve:
    st.error(str(ve))
    st.info("Please check if the stock symbol is correct and try again.")
except Exception as e:
    if "Too Many Requests" in str(e):
        st.error("We're experiencing high traffic. Please wait a few seconds and try again.")
    else:
        st.error(f"Error loading data: {str(e)}")
    st.info("Try refreshing the page or using a different stock symbol.") 