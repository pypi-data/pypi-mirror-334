# fin_insight.py
import yfinance as yf
import requests  # For News API (will be used later)
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # (will be used later)
import json # (will be used later)
import pandas as pd # Import pandas for DataFrame handling from yfinance
import argparse
import sys
import os

# --- API Keys and Configuration (If Needed for NewsAPI, etc.) ---


def get_stock_data(ticker):
    """
    Fetches stock data from yfinance for a given ticker.
    Added basic ticker symbol validation.

    Args:
        ticker (str): Stock ticker symbol to fetch data for.

    Returns:
        dict or None: Stock data dictionary or None if invalid ticker.
    """
    try:
        ticker_object = yf.Ticker(ticker)

        # **Basic Ticker Validation - Check if ticker_object.info is empty or contains error**
        if not ticker_object.info or ticker_object.info.get('symbol') is None or ticker_object.info.get('symbol') == '': # Check if info is empty or symbol is missing/empty
            print(f"Error fetching stock data for {ticker}: Invalid ticker symbol. Please check the ticker symbol.")
            return None # Return None to signal invalid ticker

        # **GET LATEST PRICE (using history as before - robust)**
        latest_day_data = ticker_object.history(period="1d")
        if not latest_day_data.empty:
            latest_price = latest_day_data['Close'].iloc[-1]
        else:
            latest_price = None

        # **GET FINANCIAL HIGHLIGHTS USING ticker_object.info**
        info_data = ticker_object.info
        financial_highlights = {
            'revenue_growth': info_data.get('revenueGrowth'),
            'earnings_growth': info_data.get('earningsGrowth'),
            'forward_pe': info_data.get('forwardPE'),
            'debt_to_equity': info_data.get('debtToEquity')
        }
        if financial_highlights['debt_to_equity'] is None:
            financial_highlights['debt_to_equity'] = info_data.get('debtToAssets')


        return {
            'latest_price': latest_price,
            'financial_highlights': financial_highlights
        }

    except Exception as e:
        print(f"Error fetching stock data for {ticker}: An unexpected error occurred while fetching data from yfinance. Details: {e} (Exception type: {type(e).__name__})") # More detailed general error for yfinance
        return None

def get_financial_news(ticker):
    """
    Fetches financial news related to the ticker from NewsAPI.org.
    Enhanced error messages for better debugging.

    Args:
        ticker (str): Stock ticker symbol to fetch news for.

    Returns:
        list: List of news article dictionaries.
    """
    api_key = os.environ.get('NEWS_API_KEY') # Get API key from environment variable
    if not api_key: # Check if API key is set in environment variables
        raise EnvironmentError("NewsAPI API key is missing. Please set the NEWS_API_KEY environment variable.") # Raise EnvironmentError if missing

    url = f"https://newsapi.org/v2/everything"
    params = {
        "q": f"{ticker} finance OR {ticker} stock OR {ticker} market",
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 5,
        "apiKey": api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()

        articles = []
        if data.get('status') == 'ok' and data.get('articles'):
            for article_data in data['articles']:
                articles.append({
                    "title": article_data.get('title'),
                    "description": article_data.get('description') or article_data.get('content')
                })
        return articles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from NewsAPI for {ticker}: Network error. Please check your internet connection. Details: {e}") # More specific network error message
    except json.JSONDecodeError as e:
        print(f"Error fetching news from NewsAPI for {ticker}: Error decoding JSON response from NewsAPI. There might be an issue with the NewsAPI response format. Details: {e}") # More specific JSON decoding error
    except Exception as e: # General error
        print(f"Error fetching news from NewsAPI for {ticker}: An unexpected error occurred. Details: {e} (Exception type: {type(e).__name__})") # More detailed general error

    return [] # Return empty list if any error occurred


def analyze_sentiment(news_articles, ticker): 
    """
    Analyzes sentiment of news articles using VADER.
    ... (rest of docstring) ...

    Args:
        news_articles (list): List of news article dictionaries.
        ticker (str): Stock ticker symbol.

    Returns:
        str: Sentiment summary string.
    """
    # ... (rest of analyze_sentiment function code) ...
    # ... (Now 'ticker' variable will be accessible inside the function) ...

    analyzer = SentimentIntensityAnalyzer()
    overall_sentiment_score = 0
    article_count = 0
    positive_keywords = [] # Lists to track keywords (example - can be expanded)
    negative_keywords = []

    if not news_articles:
        return "Neutral sentiment - No news articles found."

    for article in news_articles:
        title = article.get('title', "")
        description = article.get('description', "")
        text_to_analyze = title + " " + description

        if text_to_analyze:
            vs = analyzer.polarity_scores(text_to_analyze)
            overall_sentiment_score += vs['compound']
            article_count += 1

            # **Keyword/Theme Extraction (Basic Example - can be improved)**
            words = text_to_analyze.lower().split() # Simple tokenization
            for word in words:
                if vs['compound'] > 0.3 and word not in ["stock", "stocks", "company", "financial", "market", ticker.lower()]: # Example positive threshold & common words to ignore
                    if word not in positive_keywords:
                        positive_keywords.append(word)
                elif vs['compound'] < -0.3 and word not in ["stock", "stocks", "company", "financial", "market", ticker.lower()]: # Example negative threshold & common words to ignore
                    if word not in negative_keywords:
                        negative_keywords.append(word)


    if article_count > 0:
        average_sentiment_score = overall_sentiment_score / article_count
        if average_sentiment_score >= 0.2:
            sentiment_label = "Positive"
            summary_detail = ". Positive news themes include: " + ", ".join(positive_keywords[:3]) if positive_keywords else "." # Include top 3 positive keywords in summary
        elif average_sentiment_score <= -0.2:
            sentiment_label = "Negative"
            summary_detail = ". Negative news themes include: " + ", ".join(negative_keywords[:3]) if negative_keywords else "." # Include top 3 negative keywords
        else:
            sentiment_label = "Neutral"
            summary_detail = "." # No detail for neutral sentiment

        return f"Overall {sentiment_label} sentiment in news articles{summary_detail}"
    else:
        return "Neutral sentiment - No articles analyzed."

def generate_rating(sentiment_summary, financial_data):
    """
    Generates a Buy/Sell/Hold rating based on sentiment summary and financial data.
    Refined rating logic with adjusted weights and thresholds (Version 2 - refined).

    Args:
        sentiment_summary (str): Sentiment summary string.
        financial_data (dict): Financial data dictionary.

    Returns:
        str: Rating string (Buy, Sell, or Hold).
    """
    rating = "Hold" # Default rating is Hold

    # --- Sentiment Score ---
    sentiment_label = "Neutral" # Default sentiment label
    if "Positive" in sentiment_summary:
        sentiment_label = "Positive"
        sentiment_weight = 0.3 # Sentiment weight remains 0.3
    elif "Negative" in sentiment_summary:
        sentiment_label = "Negative"
        sentiment_weight = -0.25 # Reduced negative sentiment weight (was -0.3)
    else:
        sentiment_weight = 0 # Neutral sentiment

    # --- Financial Data ---
    financial_score = 0
    if financial_data:
        revenue_growth = financial_data.get('revenue_growth')
        earnings_growth = financial_data.get('earnings_growth')
        forward_pe = financial_data.get('forward_pe')
        debt_to_equity = financial_data.get('debt_to_equity')

        # --- Revenue Growth ---
        if isinstance(revenue_growth, (int, float)):
            if revenue_growth > 0.12: # Increased threshold to 12% (was 10%)
                financial_score += 0.4 # Weight remains 0.4
            elif revenue_growth < 0: # < 0% revenue growth
                financial_score -= 0.1 # Weight remains -0.1

        # --- Earnings Growth ---
        if isinstance(earnings_growth, (int, float)):
            if earnings_growth > 0.12: # Increased threshold to 12% (was 10%)
                financial_score += 0.5 # Weight remains 0.5
            elif earnings_growth < 0: # < 0% earnings growth
                financial_score -= 0.2 # Weight remains -0.2
        elif earnings_growth is None: # Penalty for missing earnings data
            financial_score -= 0.1 # New penalty for missing earnings

        # --- Forward P/E Ratio ---
        if isinstance(forward_pe, (int, float)):
            if forward_pe > 0 and forward_pe < 18:
                financial_score += 0.3 # Weight remains 0.3
            elif forward_pe > 28: # Threshold remains 28
                financial_score -= 0.25 # Increased negative weight (was -0.2)

        # --- Debt-to-Equity Ratio (or Debt-to-Assets) ---
        if isinstance(debt_to_equity, (int, float)):
            if debt_to_equity < 1.2:
                financial_score += 0.2 # Weight remains 0.2
            elif debt_to_equity > 2.5:
                financial_score -= 0.3 # Weight remains -0.3

    # --- Combine Sentiment and Financial Scores ---
    overall_score = sentiment_weight + financial_score

    # --- Rating Decision based on Overall Score ---
    if overall_score >= 0.6: # Increased Buy threshold to 0.6 (was 0.5)
        rating = "Buy"
    elif overall_score <= -0.3: # Sell threshold remains -0.3
        rating = "Sell"
    else:
        rating = "Hold" # Remains "Hold" for scores in between

    print(f"generate_rating() - Sentiment: {sentiment_label}, Financial Score: {financial_score:.2f}, Overall Score: {overall_score:.2f}, Rating: {rating}") # Print rating breakdown for debugging
    return rating

def create_json_response(ticker, latest_price, sentiment_summary, financial_highlights, rating):
    """
    Formats the analysis results into a JSON response.
    Enhanced financial_highlights with clearer labels and percentage formatting.

    Args:
        ticker (str): Stock ticker symbol.
        latest_price (float): Latest stock price.
        sentiment_summary (str): Sentiment summary string.
        financial_highlights (dict): Financial highlights dictionary.
        rating (str): Rating string (Buy, Sell, or Hold).

    Returns:
        str: JSON-formatted string containing stock analysis results.
    """
    formatted_financial_highlights = {} # New dictionary for formatted highlights

    if financial_highlights:
        formatted_financial_highlights = {
            "revenueGrowthPercentage": f"{financial_highlights.get('revenue_growth', 'N/A') * 100:.2f}%" if isinstance(financial_highlights.get('revenue_growth'), (int, float)) else 'N/A', # Format as percentage, handle missing data
            "earningsGrowthPercentage": f"{financial_highlights.get('earnings_growth', 'N/A') * 100:.2f}%" if isinstance(financial_highlights.get('earnings_growth'), (int, float)) else 'N/A', # Format as percentage, handle missing data
            "forwardPERatio": f"{financial_highlights.get('forward_pe', 'N/A'):.2f}" if isinstance(financial_highlights.get('forward_pe'), (int, float)) else 'N/A', # Format to 2 decimal places, handle missing
            "debtToEquityRatio": f"{financial_highlights.get('debt_to_equity', 'N/A'):.2f}" if isinstance(financial_highlights.get('debt_to_equity'), (int, float)) else 'N/A' # Format to 2 decimal places, handle missing
        }


    response_data = {
        "ticker": ticker,
        "latest_price": latest_price,
        "sentiment_summary": sentiment_summary,
        "financialHighlights": formatted_financial_highlights, # Use the formatted dictionary
        "rating": rating
    }
    return json.dumps(response_data, indent=4)

def main(ticker):
    """
    Main function to orchestrate the financial analysis and generate JSON output.

    Args:
        ticker (str): Stock ticker symbol to analyze.

    Returns:
        str: JSON-formatted string containing stock analysis results.
    """
    stock_data = get_stock_data(ticker)

    if stock_data:
        news_articles = get_financial_news(ticker)
        print(f"\n--- News Articles for {ticker} ---")
        if news_articles:
            print(f"Fetched {len(news_articles)} news articles.")
        else:
            print("No news articles found or error fetching news.")

        sentiment_summary = analyze_sentiment(news_articles, ticker)
        rating = generate_rating(sentiment_summary, stock_data['financial_highlights'])

        json_output = create_json_response(
            ticker,
            stock_data['latest_price'],
            sentiment_summary=sentiment_summary,
            financial_highlights=stock_data['financial_highlights'],
            rating=rating
        )
        return json_output
    else: # stock_data is None - error case
        # **More informative JSON error based on why get_stock_data failed**
        error_message = f"Could not retrieve data for ticker: {ticker}. Please check the ticker symbol or try again later." # Default error message
        stock_data_error = get_stock_data(ticker) # Call get_stock_data again (we could technically capture the error message from the first call, but for simplicity, re-call it)

        if stock_data_error is None: # get_stock_data returned None (as we made it do for invalid ticker)
             error_message = f"Invalid ticker symbol: {ticker}. Please check the ticker symbol and ensure it is valid." # More specific error for invalid ticker

        return json.dumps({"error": error_message}, indent=4) # Use the more specific error message in JSON

def cli():
    """
    Command-line interface entry point for the fin_insight tool.
    Handles API key check and argument parsing.
    """
    # --- NewsAPI Key Check at Startup (Environment Variable) ---
    if not os.environ.get('NEWS_API_KEY'): # Check for environment variable
        print("Error: NewsAPI API key is not configured.")
        print("Please set the NEWS_API_KEY environment variable.")
        sys.exit(1)

    # --- Set up argument parser ---
    parser = argparse.ArgumentParser(description="Financial News Sentiment Analyzer for Stocks")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., AAPL, MSFT)")
    args = parser.parse_args()

    ticker_input = args.ticker
    result_json = main(ticker_input)
    print(result_json)

if __name__ == "__main__":
    cli()