import requests
import os
import sqlite3
from datetime import date, datetime, timedelta
import pandas as pd

class Fetcher:
   def fetcher(self):
        
        def fetch_stock_data(symbol):
            API_KEY = "J8YYYHG8BODFJQKX"
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"

            response = requests.get(url)
            data = response.json()
            
            stock_data = []
            five_years_ago = date.today() - timedelta(days=5*365)
            
            try:
                for date_str, attributes in data['Time Series (Daily)'].items():
                    record_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    
                    if record_date < five_years_ago:
                        continue
                    
                    record = {
                        'date': date_str,
                        'ticker': symbol,
                        'open_price': float(attributes['1. open']),
                        'close_price': float(attributes['4. close']),
                        'volume': int(attributes['5. volume']),
                    }
                    stock_data.append(record)
                
                stock_data.sort(key=lambda x: x['date'])
                
            except KeyError:
                print(f"Could not find 'Time Series (Daily)' in API response for {symbol}")
            
            return stock_data

        def create_table():

            conn = sqlite3.connect('stock_data.db')
            cursor = conn.cursor()
            
            cursor.execute('DROP TABLE IF EXISTS stock_data')

            cursor.execute('''CREATE TABLE stock_data
                            (date TEXT, ticker TEXT, open_price REAL, close_price REAL, volume INTEGER,
                            daily_return REAL, moving_avg REAL, rsi REAL, macd REAL, upper_band REAL, lower_band REAL)''')
            
            conn.commit()
            conn.close()

        def insert_stock_data(stock_data):
            conn = sqlite3.connect('stock_data.db')
            cursor = conn.cursor()

            # Insert new data
            for record in stock_data:
                cursor.execute(
                    "INSERT INTO stock_data (date, ticker, open_price, close_price, volume) VALUES (?, ?, ?, ?, ?)",
                    (record['date'], record['ticker'], record['open_price'], record['close_price'], record['volume'])
                )
                
            conn.commit()
            conn.close()

        def calculate_metrics(symbol):
            conn = sqlite3.connect('stock_data.db')
            df = pd.read_sql_query(f"SELECT date, close_price FROM stock_data WHERE ticker = '{symbol}' ORDER BY date ASC", conn)
            
            df['daily_return'] = df['close_price'].pct_change(1)
            df['moving_avg'] = df['close_price'].rolling(window=5).mean()
            
            delta = df['close_price'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            exp12 = df['close_price'].ewm(span=12, adjust=False).mean()
            exp26 = df['close_price'].ewm(span=26, adjust=False).mean()
            df['macd'] = exp12 - exp26
            
            df['upper_band'] = df['close_price'].rolling(window=20).mean() + 2 * df['close_price'].rolling(window=20).std()
            df['lower_band'] = df['close_price'].rolling(window=20).mean() - 2 * df['close_price'].rolling(window=20).std()
            
            for index, row in df.iterrows():
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE stock_data SET daily_return = ?, moving_avg = ?, rsi = ?, macd = ?, upper_band = ?, lower_band = ? WHERE date = ? AND ticker = ?",
                    (row['daily_return'], row['moving_avg'], row['rsi'], row['macd'], row['upper_band'], row['lower_band'], row['date'], symbol)
                )
                
            conn.commit()
            conn.close()


        create_table()
        
        symbols = ['AAPL', 'GOOGL', 'MSFT']
        
        for symbol in symbols:
            stock_data = fetch_stock_data(symbol)
            insert_stock_data(stock_data)
            calculate_metrics(symbol)