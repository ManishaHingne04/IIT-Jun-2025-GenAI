import streamlit as st
from crewai.tools import tool
from crewai import Agent, Task, Process, Crew
import yfinance as yf
import pandas as pd

@tool("get stock info")
def get_stock_info(stock_symbol: str) -> pd.DataFrame:
    """
    This function will retrieve the stock information using yahoo finance.
    Args:
        stock_symbol (str): stock symbol used to find the stock information
    Returns:
        DataFrame: contains the information about the stock
    """
    
    # create a ticker
    ticker = yf.Ticker(stock_symbol)
    
    # get the current stock info for the stock label
    info = ticker.info

    # create a dataframe using the stock information we found from yf
    basic_info = pd.DataFrame({
        'Name': [info.get('longName', 'N/A')],
        'Sector': [info.get('sector', 'N/A')],
        'Industry': [info.get('industry', 'N/A')],
        'Market Cap': [info.get('marketCap', 'N/A')],
        'Current Price': [info.get('currentPrice', 'N/A')],
        '52 Week High': [info.get('fiftyTwoWeekHigh', 'N/A')],
        '52 Week Low': [info.get('fiftyTwoWeekLow', 'N/A')],
        'Average Volume': [info.get('averageVolume', 'N/A')]
    })
    
    return basic_info


@tool("fundamental analysis")
def get_fundamental_analysis(ticker: str, period: str = '1y') -> dict:
    """
    Performs fundamental analysis on a given stock for a specific period.
    
    Args:
        ticker: The stock ticker symbol.
        period: The period to consider for historical data (default is 1 year).
    
    Returns: 
        dictionary: with fundamental metrics.
    """
    stock = yf.Ticker(ticker)

    # Fetch historical data for the given period
    history = stock.history(period=period)
    
    # Fetch latest available financial info
    info = stock.info
    
    fundamental_analysis = pd.DataFrame({
        'PE Ratio': [info.get('trailingPE', 'N/A')],
        'Forward PE': [info.get('forwardPE', 'N/A')],
        'PEG Ratio': [info.get('pegRatio', 'N/A')],
        'Price to Book': [info.get('priceToBook', 'N/A')],
        'Dividend Yield': [info.get('dividendYield', 'N/A')],
        'EPS (TTM)': [info.get('trailingEps', 'N/A')],
        'Revenue Growth': [info.get('revenueGrowth', 'N/A')],
        'Profit Margin': [info.get('profitMargins', 'N/A')],
        'Free Cash Flow': [info.get('freeCashflow', 'N/A')],
        'Debt to Equity': [info.get('debtToEquity', 'N/A')],
        'Return on Equity': [info.get('returnOnEquity', 'N/A')],
        'Operating Margin': [info.get('operatingMargins', 'N/A')],
        'Quick Ratio': [info.get('quickRatio', 'N/A')],
        'Current Ratio': [info.get('currentRatio', 'N/A')],
        'Earnings Growth': [info.get('earningsGrowth', 'N/A')],
        'Stock Price Avg (Period)': [history['Close'].mean()],
        'Stock Price Max (Period)': [history['Close'].max()],
        'Stock Price Min (Period)': [history['Close'].min()]
    })
    
    return fundamental_analysis

@tool("technical analysis")
def get_technical_analysis(ticker: str, period: str = "") -> pd.DataFrame:
    """
    Perform technical analysis on a given stock.
    
    Args:
      ticker: The stock ticker symbol.
      period: The time period for historical data (available time-periods: ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]).

    Returns:
        DataFrame: containing technical analysis of a required stock.
    """
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)
    
    # Calculate indicators
    history['SMA_50'] = history['Close'].rolling(window=50).mean()
    history['SMA_200'] = history['Close'].rolling(window=200).mean()
    
    latest = history.iloc[-1]    
    analysis = pd.DataFrame({
        'Indicator': [
            'Current Price',
            '50-day SMA',
            '200-day SMA',
            'RSI (14-day)',
            'MACD',
            'MACD Signal',
            'Trend',
            'MACD Signal',
            'RSI Signal'
        ],
        'Value': [
            f'${latest["Close"]:.2f}',
            f'${latest["SMA_50"]:.2f}',
            f'${latest["SMA_200"]:.2f}',
            f'{latest["RSI"]:.2f}',
            f'{latest["MACD"]:.2f}',
            f'{latest["Signal"]:.2f}'
        ]
    })
    
    return analysis



# create an agent for getting the basic stock information
stock_researcher = Agent(
    llm="ollama/llama3.1",
    role="Stock researcher",
    goal="Identify the stock and the stock ticker, and if you already have the stock ticker and if it's necessary, get basic stock info about the selected stock.",
    backstory="An junior stock researcher with a knack for gathering relevant, basic information about stocks, the relevant company/companies, the industry, and some basic info about stock's performance",
    tools=[get_stock_info],
    verbose=True,
    allow_delegation=False
)


# create an agent for financial analysis
financial_analyst = Agent(
    llm="ollama/llama3.1",
    role="Financial Analyst",
    goal="Perform in-depth fundamental and technical analysis on the stock, focusing on aspects most relevant to the user's query",
    backstory="A seasoned financial analyst with expertise in interpreting complex financial data and translating it into insights tailored to various levels of financial literacy",
    tools=[get_technical_analysis, get_fundamental_analysis],
    verbose=True,
    allow_delegation=False
)

# get all the basic information about the stock
collect_stock_info = Task(
    description="""
    1. Extract the ticker of the stock (or stocks) mentioned in the user query as well as the timeframe (if mentioned). If the ticker is not provided, use the query to identify the stock ticker.
    2. If the query implies a novice user, prepare brief explanations for key financial terms. If nothing is mentioned, assume that the user has an above average understanding of financial terms.
    
    Expect only basic stock info from this task.
    
    User query: {query}.
    
    Your response should be on the basis of:
    Ticker: [identified stock ticker]
    Timeframe: [identified timeframe]
    Analysis Focus: [identified focus of analysis]
    User Expertise: [implied level of financial expertise]
    Key Concerns: [specific concerns or priorities mentioned]
    """,
    expected_output="A summary of stock's key financial metrics and performance tailored to the user's query",
    agent=stock_researcher,
    dependencies=[],
    context=[]
)

# task to perform fundamental and technical analysis
perform_analysis = Task(
    description='''
    Conduct a thorough analysis of the stock, tailored to the user's query and expertise level.
    1. Use the get_stock_info, get_fundamental_analysis and get_technical_analysis tools as needed, based on the query's focus. E.g. If the query is about the fundamentals of a stock, then technical info need not be present.
    2. Focus on metrics and trends most relevant to the user's specific question and identified timeframe.
    3. Provide clear explanations of complex financial concepts if the query suggests a novice user.
    4. Relate the analysis directly to the key concerns identified in the query interpretation.
    5. Consider both historical performance and future projections in your analysis..
    
    User query: {query}.
    ''',
    expected_output="A detailed analysis of the stock's financial and/or technical performance, directly addressing the user's query and concerns.",
    agent=financial_analyst,
    dependencies=[collect_stock_info],
    context=[collect_stock_info]
)

# create the crew
crew = Crew(
    agents=[stock_researcher, financial_analyst],
    tasks=[ collect_stock_info, perform_analysis],
    process=Process.sequential
)

st.header("Stock Research Assistant")
st.write("This app helps you to analyze stocks using the Yahoo Finance API and CrewAI.")

question = st.chat_input("Ask me anything about stocks!")
if question:
    with st.spinner("Analyzing..."):
        # run the crew
        response = crew.kickoff({"query": question})
    
    # display the response
    st.markdown(response)