from datetime import datetime, timedelta
import calendar
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import pandas as pd
import seaborn as sns
import yfinance as yf
sns.set()


def one_month_from_today():
    today = datetime.today()
    _, last_day_of_month = calendar.monthrange(today.year, today.month)
    one_month_ago = today - timedelta(days=today.day + last_day_of_month - 1)

    return one_month_ago


def one_year_from_today():
    today = datetime.today()
    one_year_ago = today - timedelta(days=365)

    return one_year_ago


def two_years_from_today():
    today = datetime.today()
    two_years_ago = today - timedelta(days=365 * 2)

    return two_years_ago


def five_years_from_today():
    today = datetime.today()
    five_years_ago = today - timedelta(days=365 * 5)

    return five_years_ago


today = datetime.today().strftime('%Y-%m-%d')


def get_stock_data(symbol, start, end):

    try:
        stock_data = yf.download(symbol, start, end)

        if stock_data.empty:
            raise ValueError(
                f"No data available for {symbol} in the specified date range.")
        stock_data = stock_data.reset_index()

        return stock_data
    except Exception as e:
        print(f"An error occured: {str(e)}")

        return None


def analyse_stock_data(symbol, start, end):
    try:
        stock_data = get_stock_data(symbol, start, end)
        stock_ticker = yf.Ticker(symbol)
        stock_ticker = stock_ticker.info['longBusinessSummary']

        stock_data = stock_data[['Date', 'Adj Close']].copy()
        stock_data['returns'] = stock_data['Adj Close'].pct_change(1)

        x_data = stock_data['Date'].tolist()
        y_data = stock_data['Adj Close'].tolist()
        average_return = stock_data['returns'].mean()

        stock_data_json = stock_data.to_json(
            orient='records', date_format='iso')

        return stock_ticker, x_data, y_data, average_return
    except Exception as e:
        error_message = f"Error during analysis: {str(e)}"
        print(error_message)
        return None


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph


def get_plot(x, y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))
    plt.title('Price of the Stock vs Time')
    plt.plot(x, y)
    plt.xticks(rotation=45)
    plt.xlabel('Dates')
    plt.ylabel('Price')
    plt.tight_layout()

    graph = get_graph()
    return graph
