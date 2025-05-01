import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from utils import (
    generate_mock_historical_data,
    generate_mock_financials,
    calculate_financial_metrics,
    get_mock_company_info
)

# Page configuration
st.set_page_config(
    page_title="Financial Dashboard Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom CSS from your existing app
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Base colors */
    :root {
        --bg-color: #f8fafc;
        --text-primary: #2d3748;
        --text-secondary: #4a5568;
        --border-color: #e2e8f0;
        --accent-color: #3b82f6;
        --metric-value: #2563eb;
        --metric-up: #059669;
        --metric-down: #dc2626;
    }

    .main .block-container {
        padding: 2rem 3rem;
        max-width: 100%;
    }

    [data-testid="stSidebar"] .block-container {
        padding: 2rem 1rem;
    }
    
    h1, h2, h3 {
        color: var(--text-primary);
        margin-bottom: 1.5rem;
        font-weight: 600 !important;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid var(--border-color);
    }
    
    .chart-section {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid var(--border-color);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Financial Analysis")
    
    # Stock selection
    selected_symbol = st.selectbox(
        "Select Stock",
        ["AAPL", "MSFT", "GOOGL"],
        index=0
    )
    
    # Analysis type
    analysis_type = st.radio(
        "Analysis Type",
        ["Overview", "Financial Statements", "Technical Analysis", "Ratios & Metrics"]
    )
    
    # Time period
    time_period = st.selectbox(
        "Time Period",
        ["1M", "3M", "6M", "YTD", "1Y", "3Y", "5Y"],
        index=3
    )

# Get data
company_info = get_mock_company_info(selected_symbol)
historical_data = generate_mock_historical_data(selected_symbol)
financials = generate_mock_financials()
metrics = calculate_financial_metrics(financials)

# Main content
if analysis_type == "Overview":
    # Company header
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title(f"{company_info['name']} ({selected_symbol})")
        st.write(f"**Sector:** {company_info['sector']} | **Industry:** {company_info['industry']}")
    with col2:
        latest_price = historical_data['Close'].iloc[-1]
        price_change = historical_data['Close'].iloc[-1] - historical_data['Close'].iloc[-2]
        price_change_pct = (price_change / historical_data['Close'].iloc[-2]) * 100
        
        st.metric(
            "Current Price",
            f"${latest_price:.2f}",
            f"{price_change_pct:+.2f}%"
        )
    
    st.write("---")
    
    # Price chart
    st.subheader("Price History")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=historical_data.index,
        open=historical_data['Open'],
        high=historical_data['High'],
        low=historical_data['Low'],
        close=historical_data['Close'],
        name='OHLC'
    ))
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis_title='Price',
        xaxis_title='Date'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Key metrics
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Gross Margin", f"{metrics['Gross Margin']:.1f}%")
    with col2:
        st.metric("Operating Margin", f"{metrics['Operating Margin']:.1f}%")
    with col3:
        st.metric("ROE", f"{metrics['ROE']:.1f}%")
    with col4:
        st.metric("Current Ratio", f"{metrics['Current Ratio']:.2f}")

elif analysis_type == "Financial Statements":
    st.title("Financial Statements Analysis")
    
    # Tabs for different statements
    tab1, tab2, tab3 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow"])
    
    with tab1:
        st.dataframe(financials['income_statement'])
        
        # Income Statement Visualization
        st.subheader("Revenue vs Net Income Trend")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=financials['income_statement'].index,
            y=financials['income_statement']['Revenue'],
            name='Revenue'
        ))
        fig.add_trace(go.Bar(
            x=financials['income_statement'].index,
            y=financials['income_statement']['Net Income'],
            name='Net Income'
        ))
        fig.update_layout(barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.dataframe(financials['balance_sheet'])
        
        # Balance Sheet Visualization
        st.subheader("Assets vs Liabilities")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=financials['balance_sheet'].index,
            y=financials['balance_sheet']['Total Assets'],
            name='Total Assets'
        ))
        fig.add_trace(go.Bar(
            x=financials['balance_sheet'].index,
            y=financials['balance_sheet']['Total Liabilities'],
            name='Total Liabilities'
        ))
        fig.update_layout(barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.dataframe(financials['cash_flow'])
        
        # Cash Flow Visualization
        st.subheader("Cash Flow Components")
        fig = go.Figure()
        for column in ['Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow']:
            fig.add_trace(go.Bar(
                x=financials['cash_flow'].index,
                y=financials['cash_flow'][column],
                name=column
            ))
        fig.update_layout(barmode='group')
        st.plotly_chart(fig, use_container_width=True)

elif analysis_type == "Technical Analysis":
    st.title("Technical Analysis")
    
    # Calculate technical indicators
    df = historical_data.copy()
    
    # Simple Moving Averages
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df['SMA200'] = df['Close'].rolling(window=200).mean()
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Price and Moving Averages
    st.subheader("Price and Moving Averages")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Close'],
        name='Price',
        line=dict(color='#2563eb', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=df.index, y=df['SMA20'],
        name='SMA20',
        line=dict(color='#059669', width=1.5)
    ))
    fig.add_trace(go.Scatter(
        x=df.index, y=df['SMA50'],
        name='SMA50',
        line=dict(color='#d97706', width=1.5)
    ))
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)
    
    # RSI
    st.subheader("Relative Strength Index (RSI)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df['RSI'],
        name='RSI',
        line=dict(color='#2563eb', width=2)
    ))
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)
    
    # MACD
    st.subheader("MACD")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df['MACD'],
        name='MACD',
        line=dict(color='#2563eb', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Signal Line'],
        name='Signal Line',
        line=dict(color='#d97706', width=2)
    ))
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

else:  # Ratios & Metrics
    st.title("Financial Ratios & Metrics")
    
    # Profitability Metrics
    st.subheader("Profitability Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Gross Margin", f"{metrics['Gross Margin']:.1f}%")
    with col2:
        st.metric("Operating Margin", f"{metrics['Operating Margin']:.1f}%")
    with col3:
        st.metric("Net Margin", f"{metrics['Net Margin']:.1f}%")
    
    # Return Metrics
    st.subheader("Return Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Return on Equity (ROE)", f"{metrics['ROE']:.1f}%")
    with col2:
        st.metric("Return on Assets (ROA)", f"{metrics['ROA']:.1f}%")
    
    # Efficiency Metrics
    st.subheader("Efficiency Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Ratio", f"{metrics['Current Ratio']:.2f}")
    with col2:
        st.metric("Operating Cash Flow Ratio", f"{metrics['Operating Cash Flow Ratio']:.2f}")
    
    # Visualization of metrics over time
    st.subheader("Margin Trends")
    margins_df = pd.DataFrame({
        'Gross Margin': [metrics['Gross Margin']],
        'Operating Margin': [metrics['Operating Margin']],
        'Net Margin': [metrics['Net Margin']]
    })
    
    fig = go.Figure()
    for column in margins_df.columns:
        fig.add_trace(go.Bar(
            x=[column],
            y=margins_df[column],
            name=column
        ))
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True) 