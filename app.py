import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Advanced Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        padding: 1rem 0;
        text-align: center;
        background: linear-gradient(120deg, #DBEAFE 0%, #EFF6FF 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .technical-section {
        margin-top: 2rem;
        padding: 1.5rem;
        border-radius: 10px;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
    }
    .stSelectbox {
        background-color: white;
        border-radius: 5px;
        padding: 2px;
    }
    .stock-metrics {
        display: flex;
        justify-content: space-between;
        padding: 10px;
        background: #F1F5F9;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Generate sample data for Apple and Microsoft
def generate_sample_data(symbol, start_price, volatility, days=90):
    np.random.seed(42 if symbol == "AAPL" else 24)
    dates = pd.date_range(end=datetime.now(), periods=days)
    prices = [start_price]
    
    for _ in range(days-1):
        change = np.random.normal(0, volatility)
        prices.append(prices[-1] * (1 + change))
    
    df = pd.DataFrame({
        'Date': dates,
        'Open': prices,
        'Close': [p * (1 + np.random.normal(0, 0.002)) for p in prices],
        'High': [p * (1 + abs(np.random.normal(0, 0.003))) for p in prices],
        'Low': [p * (1 - abs(np.random.normal(0, 0.003))) for p in prices],
        'Volume': [int(np.random.normal(1000000, 200000)) for _ in prices]
    })
    
    df.set_index('Date', inplace=True)
    return df

# Technical Analysis Functions
def calculate_sma(data, window):
    return data.rolling(window=window).mean()

def calculate_ema(data, window):
    return data.ewm(span=window, adjust=False).mean()

def calculate_rsi(data, periods=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_bollinger_bands(data, window=20):
    sma = calculate_sma(data, window)
    std = data.rolling(window=window).std()
    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2)
    return upper_band, sma, lower_band

# Sample company info
SAMPLE_DATA = {
    "AAPL": {
        "name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "market_cap": "2.5T",
        "pe_ratio": 28.5,
        "dividend_yield": 0.65,
        "price": 175.0,
        "volatility": 0.015
    },
    "MSFT": {
        "name": "Microsoft Corporation",
        "sector": "Technology",
        "industry": "Software",
        "market_cap": "2.8T",
        "pe_ratio": 32.1,
        "dividend_yield": 0.85,
        "price": 330.0,
        "volatility": 0.012
    }
}

# Sidebar
st.sidebar.markdown("## Dashboard Controls")
selected_stock = st.sidebar.selectbox(
    "Select Stock",
    options=["AAPL", "MSFT"],
    format_func=lambda x: f"{x} - {SAMPLE_DATA[x]['name']}"
)

time_period = st.sidebar.select_slider(
    "Time Period",
    options=[30, 60, 90],
    value=90,
    format_func=lambda x: f"{x} Days"
)

# Generate data for selected stock
stock_info = SAMPLE_DATA[selected_stock]
hist_data = generate_sample_data(
    selected_stock,
    stock_info["price"],
    stock_info["volatility"],
    time_period
)

# Main content
st.markdown(f'<h1 class="main-header">{stock_info["name"]} ({selected_stock}) Analysis</h1>', unsafe_allow_html=True)

# Company Overview
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>Company Overview</h3>
            <p><strong>Sector:</strong> {stock_info['sector']}</p>
            <p><strong>Industry:</strong> {stock_info['industry']}</p>
            <p><strong>Market Cap:</strong> ${stock_info['market_cap']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>Key Metrics</h3>
            <p><strong>P/E Ratio:</strong> {stock_info['pe_ratio']:.2f}</p>
            <p><strong>Dividend Yield:</strong> {stock_info['dividend_yield']}%</p>
            <p><strong>Current Price:</strong> ${hist_data['Close'][-1]:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>Performance</h3>
            <p><strong>Daily Change:</strong> {((hist_data['Close'][-1] / hist_data['Close'][-2] - 1) * 100):.2f}%</p>
            <p><strong>30-Day Return:</strong> {((hist_data['Close'][-1] / hist_data['Close'][0] - 1) * 100):.2f}%</p>
            <p><strong>Volume:</strong> {hist_data['Volume'][-1]:,.0f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Technical Analysis Section
st.markdown("## Technical Analysis")

# Price and Volume Chart
fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=hist_data.index,
    open=hist_data['Open'],
    high=hist_data['High'],
    low=hist_data['Low'],
    close=hist_data['Close'],
    name="OHLC"
))

# Add Bollinger Bands
upper, middle, lower = calculate_bollinger_bands(hist_data['Close'])
fig.add_trace(go.Scatter(x=hist_data.index, y=upper, name='Upper BB', line=dict(color='gray', dash='dash')))
fig.add_trace(go.Scatter(x=hist_data.index, y=middle, name='Middle BB', line=dict(color='blue', dash='dash')))
fig.add_trace(go.Scatter(x=hist_data.index, y=lower, name='Lower BB', line=dict(color='gray', dash='dash')))

fig.update_layout(
    title=f"{selected_stock} Price Chart with Bollinger Bands",
    yaxis_title="Price",
    xaxis_title="Date",
    template="plotly_white",
    height=600,
)

st.plotly_chart(fig, use_container_width=True)

# Technical Indicators
col1, col2 = st.columns(2)

with col1:
    # RSI Chart
    rsi = calculate_rsi(hist_data['Close'])
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=hist_data.index, y=rsi, name='RSI'))
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
    fig_rsi.update_layout(title="Relative Strength Index (RSI)", height=300)
    st.plotly_chart(fig_rsi, use_container_width=True)

with col2:
    # Moving Averages
    sma_20 = calculate_sma(hist_data['Close'], 20)
    ema_50 = calculate_ema(hist_data['Close'], 50)
    
    fig_ma = go.Figure()
    fig_ma.add_trace(go.Scatter(x=hist_data.index, y=sma_20, name='SMA 20'))
    fig_ma.add_trace(go.Scatter(x=hist_data.index, y=ema_50, name='EMA 50'))
    fig_ma.update_layout(title="Moving Averages", height=300)
    st.plotly_chart(fig_ma, use_container_width=True)

# Trading Signals
st.markdown("## Trading Signals")
current_rsi = rsi[-1]
sma_signal = "Bullish" if sma_20[-1] > ema_50[-1] else "Bearish"
rsi_signal = "Overbought" if current_rsi > 70 else "Oversold" if current_rsi < 30 else "Neutral"

signal_col1, signal_col2, signal_col3 = st.columns(3)
with signal_col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>RSI Signal</h3>
            <p><strong>Current RSI:</strong> {current_rsi:.2f}</p>
            <p><strong>Signal:</strong> {rsi_signal}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with signal_col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>Moving Average Signal</h3>
            <p><strong>SMA(20):</strong> ${sma_20[-1]:.2f}</p>
            <p><strong>Signal:</strong> {sma_signal}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with signal_col3:
    bb_position = (hist_data['Close'][-1] - lower[-1]) / (upper[-1] - lower[-1]) * 100
    bb_signal = "Oversold" if bb_position < 20 else "Overbought" if bb_position > 80 else "Neutral"
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>Bollinger Bands Signal</h3>
            <p><strong>Position:</strong> {bb_position:.2f}%</p>
            <p><strong>Signal:</strong> {bb_signal}</p>
        </div>
        """,
        unsafe_allow_html=True
    ) 