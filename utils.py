import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Union

def generate_mock_historical_data(symbol: str, days: int = 180) -> pd.DataFrame:
    """Generate mock historical price data for a given symbol."""
    dates = pd.date_range(end=datetime.now(), periods=days)
    np.random.seed(hash(symbol) % 2**32)
    
    # Generate base price and daily returns
    base_price = np.random.uniform(50, 500)
    daily_returns = np.random.normal(0.0005, 0.02, days)
    
    # Calculate prices
    prices = base_price * (1 + daily_returns).cumprod()
    volume = np.random.randint(100000, 10000000, size=days)
    
    df = pd.DataFrame({
        'Date': dates,
        'Open': prices * (1 + np.random.normal(0, 0.002, days)),
        'High': prices * (1 + np.abs(np.random.normal(0, 0.003, days))),
        'Low': prices * (1 - np.abs(np.random.normal(0, 0.003, days))),
        'Close': prices,
        'Volume': volume,
        'Adj Close': prices
    })
    
    return df.set_index('Date')

def generate_mock_financials() -> Dict[str, pd.DataFrame]:
    """Generate mock financial statements."""
    # Income Statement
    income_statement = pd.DataFrame({
        'Revenue': [10000, 12000, 15000, 18000],
        'Cost of Revenue': [6000, 7000, 8500, 10000],
        'Gross Profit': [4000, 5000, 6500, 8000],
        'Operating Expenses': [2500, 3000, 3500, 4000],
        'Operating Income': [1500, 2000, 3000, 4000],
        'Net Income': [1200, 1600, 2400, 3200]
    }, index=pd.date_range(end=datetime.now(), periods=4, freq='Q'))
    
    # Balance Sheet
    balance_sheet = pd.DataFrame({
        'Cash': [5000, 6000, 7000, 8000],
        'Total Assets': [20000, 22000, 25000, 28000],
        'Total Liabilities': [10000, 11000, 12000, 13000],
        'Total Equity': [10000, 11000, 13000, 15000]
    }, index=pd.date_range(end=datetime.now(), periods=4, freq='Q'))
    
    # Cash Flow Statement
    cash_flow = pd.DataFrame({
        'Operating Cash Flow': [2000, 2500, 3000, 3500],
        'Investing Cash Flow': [-1000, -1200, -1500, -1800],
        'Financing Cash Flow': [-800, -1000, -1200, -1400],
        'Net Cash Flow': [200, 300, 300, 300]
    }, index=pd.date_range(end=datetime.now(), periods=4, freq='Q'))
    
    return {
        'income_statement': income_statement,
        'balance_sheet': balance_sheet,
        'cash_flow': cash_flow
    }

def calculate_financial_metrics(financials: Dict[str, pd.DataFrame]) -> Dict[str, float]:
    """Calculate key financial metrics from financial statements."""
    latest_income = financials['income_statement'].iloc[-1]
    latest_balance = financials['balance_sheet'].iloc[-1]
    latest_cash_flow = financials['cash_flow'].iloc[-1]
    
    metrics = {
        'Gross Margin': (latest_income['Gross Profit'] / latest_income['Revenue']) * 100,
        'Operating Margin': (latest_income['Operating Income'] / latest_income['Revenue']) * 100,
        'Net Margin': (latest_income['Net Income'] / latest_income['Revenue']) * 100,
        'ROE': (latest_income['Net Income'] / latest_balance['Total Equity']) * 100,
        'ROA': (latest_income['Net Income'] / latest_balance['Total Assets']) * 100,
        'Current Ratio': latest_balance['Cash'] / (latest_balance['Total Liabilities'] * 0.3),  # Assuming 30% are current liabilities
        'Operating Cash Flow Ratio': latest_cash_flow['Operating Cash Flow'] / latest_income['Revenue']
    }
    
    return metrics

def get_mock_company_info(symbol: str) -> Dict[str, str]:
    """Get mock company information."""
    companies = {
        'AAPL': {
            'name': 'Apple Inc.',
            'sector': 'Technology',
            'industry': 'Consumer Electronics',
            'description': 'Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide.'
        },
        'MSFT': {
            'name': 'Microsoft Corporation',
            'sector': 'Technology',
            'industry': 'Software',
            'description': 'Microsoft Corporation develops, licenses, and supports software, services, devices, and solutions worldwide.'
        },
        'GOOGL': {
            'name': 'Alphabet Inc.',
            'sector': 'Technology',
            'industry': 'Internet Content & Information',
            'description': 'Alphabet Inc. provides various products and platforms in the United States, Europe, the Middle East, Africa, and Asia Pacific.'
        }
    }
    
    return companies.get(symbol, {
        'name': f'{symbol} Corp',
        'sector': 'Technology',
        'industry': 'Software',
        'description': f'Mock description for {symbol}'
    }) 