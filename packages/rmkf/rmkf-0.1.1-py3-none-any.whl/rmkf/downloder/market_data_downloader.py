import pandas as pd
import yfinance as yf
import FinanceDataReader as fdr
import pandas_datareader.data as web
from tqdm import tqdm
import time

class MarketDataDownloader:
    def __init__(self, start_date="2000-01-01", end_date="2024-07-28", src='yfinance'):
        self.start_date = start_date
        self.end_date = end_date
        self.src = src
    
    def download_prices(self, ticker_list):
        prices_list = []
        
        if not isinstance(ticker_list, list):
            try: 
                ticker_list = list(ticker_list)
            except:
                raise ValueError
            
        for ticker in tqdm(ticker_list):
            if self.src == 'yfinance':
                stock = yf.Ticker(ticker)
                price_info = stock.history(start=self.start_date, end=self.end_date)
            elif self.src == 'fdr':
                price_info = fdr.DataReader(ticker, start=self.start_date, end=self.end_date)
            elif self.src == 'fred':
                price_info = web.DataReader(ticker, "fred", start=self.start_date, end=self.end_date)
            
            time.sleep(1)

            price_info['ticker'] = ticker
            prices_list.append(price_info)
        
        prices_df = pd.concat(prices_list)
        return prices_df
    
    def remake_df(self, prices_df):
        # 날짜 형식으로 인덱스 변환 시도
        if pd.api.types.is_datetime64_any_dtype(prices_df.index):
            prices_df.index = prices_df.index.strftime('%Y-%m-%d')
        
        # 불필요한 컬럼 제거
        columns_to_drop = ['adj close', 'capital gains', 'stock splits']
        for column in columns_to_drop:
            if column in prices_df.columns:
                prices_df = prices_df.drop([column], axis=1)
        
        # 인덱스 재설정 및 컬럼명 정리
        prices_df = prices_df.reset_index()
        prices_df.columns = prices_df.columns.str.lower()
        prices_df.columns = prices_df.columns.str.replace("dividends", "dividend")
        
        # 인덱스 설정 및 중복 제거
        if 'ticker' in prices_df.columns and 'date' in prices_df.columns:
            prices_df = prices_df.set_index(['ticker', 'date'])
            prices_df = prices_df[~prices_df.index.duplicated(keep='first')]
        
        return prices_df

    def df_intersection(self, df1, df2):
        common_index = df1.index.intersection(df2.index)
        df1 = df1.loc[common_index]
        df2 = df2.loc[common_index]
        return df1, df2
