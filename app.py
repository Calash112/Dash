import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Global Markets Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS styling
st.markdown("""
<style>
    /* Main styles */
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
    
    /* Navigation Banner */
    .stNavigationMenu {
        background-color: #1E3A8A;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .nav-link {
        color: white;
        padding: 0.5rem 1rem;
        text-decoration: none;
        border-radius: 5px;
        margin: 0 0.5rem;
    }
    .nav-link:hover {
        background-color: #2563EB;
    }
    
    /* Market Index Cards */
    .market-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .market-card:hover {
        transform: translateY(-2px);
        transition: transform 0.2s;
    }
    .positive-change {
        color: #10B981;
        font-weight: bold;
    }
    .negative-change {
        color: #EF4444;
        font-weight: bold;
    }
    
    /* Footer */
    .footer {
        background: #F3F4F6;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 3rem;
    }
    .footer-link {
        color: #374151;
        text-decoration: none;
        margin: 0 1rem;
    }
    .footer-link:hover {
        color: #2563EB;
    }
    
    /* Metrics and Charts */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Mock market data
MARKET_INDICES = {
    "US Markets": {
        "S&P 500": {"value": "4,927.25", "change": "+1.25%", "positive": True},
        "Dow Jones": {"value": "38,654.42", "change": "-0.32%", "positive": False},
        "NASDAQ": {"value": "15,990.66", "change": "+1.75%", "positive": True}
    },
    "European Markets": {
        "FTSE 100": {"value": "7,615.35", "change": "+0.45%", "positive": True},
        "DAX": {"value": "16,918.21", "change": "-0.72%", "positive": False},
        "CAC 40": {"value": "7,592.26", "change": "+0.89%", "positive": True}
    },
    "Australian Markets": {
        "ASX 200": {"value": "7,642.80", "change": "+0.95%", "positive": True},
        "All Ordinaries": {"value": "7,875.20", "change": "+0.88%", "positive": True},
        "ASX 300": {"value": "7,525.40", "change": "+0.92%", "positive": True}
    }
}

# Navigation Banner
st.markdown("""
<div class="stNavigationMenu">
    <a href="#" class="nav-link">My Portfolio</a>
    <a href="#" class="nav-link">Markets</a>
    <a href="#" class="nav-link">News</a>
    <a href="#" class="nav-link">Analysis</a>
    <a href="#" class="nav-link">Watchlist</a>
</div>
""", unsafe_allow_html=True)

# Main content area
col_main, col_markets = st.columns([2, 1])

with col_markets:
    st.markdown("### Global Markets")
    
    # Market selection
    selected_region = st.selectbox(
        "Select Region",
        options=list(MARKET_INDICES.keys()),
        index=0
    )
    
    # Display market indices for selected region
    for index, data in MARKET_INDICES[selected_region].items():
        st.markdown(f"""
        <div class="market-card">
            <h4>{index}</h4>
            <p style="font-size: 1.2rem;">{data['value']}</p>
            <p class="{'positive-change' if data['positive'] else 'negative-change'}">{data['change']}</p>
        </div>
        """, unsafe_allow_html=True)

with col_main:
    # Your existing main dashboard content here
    st.markdown("## Market Analysis")
    
    # Sample stock selection
    selected_stock = st.selectbox(
        "Select Stock",
        options=["AAPL", "MSFT"],
        format_func=lambda x: f"{x} - {SAMPLE_DATA[x]['name']}"
    )
    
    # Generate and display stock data
    stock_info = SAMPLE_DATA[selected_stock]
    hist_data = generate_sample_data(
        selected_stock,
        stock_info["price"],
        stock_info["volatility"],
        90
    )
    
    # Display stock chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=hist_data.index,
        open=hist_data['Open'],
        high=hist_data['High'],
        low=hist_data['Low'],
        close=hist_data['Close'],
        name="OHLC"
    ))
    
    fig.update_layout(
        title=f"{selected_stock} Price Chart",
        yaxis_title="Price",
        xaxis_title="Date",
        template="plotly_white",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("""
<div class="footer">
    <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
        <a href="#" class="footer-link">About Us</a>
        <a href="#" class="footer-link">Help Center</a>
        <a href="#" class="footer-link">Contact</a>
        <a href="#" class="footer-link">Feedback</a>
    </div>
    <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
        <a href="#" class="footer-link">Terms & Conditions</a>
        <a href="#" class="footer-link">Privacy Policy</a>
        <a href="#" class="footer-link">Security</a>
        <a href="#" class="footer-link">Cookies</a>
    </div>
    <div style="text-align: center; color: #6B7280; font-size: 0.875rem;">
        © 2024 Global Markets Dashboard. All rights reserved.
    </div>
</div>
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