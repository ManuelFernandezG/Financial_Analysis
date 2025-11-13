# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 01:02:46 2025

@author: manny
"""

import sys

# First, let's check what packages are available
try:
    import pandas as pd
    print("pandas imported successfully")
except ImportError:
    print("pandas not installed")

try:
    import matplotlib.pyplot as plt
    print("matplotlib imported successfully")
except ImportError:
    print("matplotlib not installed")

try:
    import yfinance as yf
    print("yfinance imported successfully")
except ImportError:
    print("yfinance not installed")

try:
    import seaborn as sns
    print("seaborn imported successfully")
except ImportError:
    print("seaborn not installed")

print("\n" + "="*50)

# If any packages are missing, show installation instructions
missing_packages = []

try:
    import yfinance
except ImportError:
    missing_packages.append("yfinance")

try:
    import matplotlib
except ImportError:
    missing_packages.append("matplotlib")

try:
    import seaborn
except ImportError:
    missing_packages.append("seaborn")

if missing_packages:
    print("MISSING PACKAGES DETECTED!")
    print("Please install missing packages using one of these methods:")
    print("\nMethod 1 - Using pip (recommended):")
    for package in missing_packages:
        print(f"  pip install {package}")
    
    print("\nMethod 2 - Using conda:")
    for package in missing_packages:
        if package == "yfinance":
            print("  conda install -c conda-forge yfinance")
        else:
            print(f"  conda install {package}")
    
    print("\nAfter installing, restart Spyder and run this code again.")
    sys.exit(1)  # Use sys.exit() instead of exit()

print("All required packages are available!")
print("Starting stock analysis...")
print("="*50)

def fetch_stock_data(ticker="AAPL", period="6mo"):
    """Fetch stock data from Yahoo Finance"""
    try:
        print(f"Fetching {ticker} data for {period}...")
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        
        if data.empty:
            print(f"No data found for {ticker}")
            return None
            
        print(f"Success! Retrieved {len(data)} trading days of data")
        return data
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_metrics(data):
    """Calculate moving averages and metrics"""
    if data is None:
        return None
        
    data = data.copy()
    
    # Calculate moving averages
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    
    return data

def plot_stock_analysis(data, ticker):
    """Create comprehensive stock analysis plot"""
    if data is None:
        return
        
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), 
                                   gridspec_kw={'height_ratios': [3, 1]})
    
    # Plot 1: Price and Moving Averages
    ax1.plot(data.index, data['Close'], label='Close Price', 
             linewidth=2, color='blue', alpha=0.8)
    ax1.plot(data.index, data['SMA_20'], label='20-day MA', 
             linestyle='--', color='red', alpha=0.7)
    ax1.plot(data.index, data['SMA_50'], label='50-day MA', 
             linestyle='--', color='green', alpha=0.7)
    
    ax1.set_title(f'{ticker} Stock Analysis', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Price ($)', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Volume
    ax2.bar(data.index, data['Volume'], color='orange', alpha=0.6)
    ax2.set_ylabel('Volume', fontsize=12)
    ax2.set_xlabel('Date', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def display_statistics(data, ticker):
    """Display key statistics"""
    if data is None:
        return
        
    current = data['Close'].iloc[-1]
    high = data['High'].max()
    low = data['Low'].min()
    change = current - data['Close'].iloc[0]
    change_pct = (change / data['Close'].iloc[0]) * 100
    
    print(f"\n{ticker} STATISTICS")
    print("=" * 40)
    print(f"Current Price:   ${current:.2f}")
    print(f"Period High:     ${high:.2f}")
    print(f"Period Low:      ${low:.2f}")
    print(f"Price Change:    ${change:+.2f} ({change_pct:+.2f}%)")
    print(f"20-day MA:       ${data['SMA_20'].iloc[-1]:.2f}")
    print(f"50-day MA:       ${data['SMA_50'].iloc[-1]:.2f}")
    print(f"Avg Volume:      {data['Volume'].mean():,.0f}")

def get_user_input():
    """Get stock ticker and period from user input"""
    print("Stock Price Analysis in Spyder")
    print("=" * 40)
    
    # Get stock ticker
    while True:
        ticker = input("Enter stock ticker symbol (e.g., AAPL, GOOGL, MSFT, TSLA): ").strip().upper()
        if ticker:
            break
        print("Please enter a valid ticker symbol.")
    
    # Get time period
    period_options = {"1": "1mo", "2": "3mo", "3": "6mo", "4": "1y", "5": "2y"}
    print("\nSelect time period:")
    print("1. 1 Month")
    print("2. 3 Months")
    print("3. 6 Months (Default)")
    print("4. 1 Year")
    print("5. 2 Years")
    
    period_choice = input("Enter choice (1-5) or press Enter for 6 Months: ").strip()
    period = period_options.get(period_choice, "6mo")
    
    return ticker, period

# Main execution
if __name__ == "__main__":
    # Get user input for stock and period
    TICKER, PERIOD = get_user_input()
    
    print(f"\nAnalyzing {TICKER} for period: {PERIOD}")
    print("-" * 40)
    
    # Get data
    stock_data = fetch_stock_data(TICKER, PERIOD)
    
    if stock_data is not None:
        # Calculate metrics
        analyzed_data = calculate_metrics(stock_data)
        
        # Display statistics
        display_statistics(analyzed_data, TICKER)
        
        # Create plot
        plot_stock_analysis(analyzed_data, TICKER)
        
        # Show recent data
        print(f"\nRecent data for {TICKER}:")
        print(analyzed_data[['Close', 'Volume', 'SMA_20', 'SMA_50']].tail())
    else:
        print("Failed to fetch stock data. Please check:")
        print("1. Your internet connection")
        print("2. The stock ticker symbol is correct")
        print("3. Try again with a different ticker")