import pandas as pd
import yfinance as yf
import FinanceDataReader as fdr
import pandas_datareader.data as web
from tqdm import tqdm
import time
from datetime import datetime

class MarketDataDownloader:
    def __init__(self, start_date:str= None, end_date:str=None) -> None:
        
        if start_date is None:
            self.start_date = "2000-01-01"
        else:
            self.start_date = start_date
        
        if end_date is None:
            self.end_date = datetime.today().strftime('%Y-%m-%d')
        else:
            self.end_date = end_date
        
    
    def download_prices(self, symbols:list, src:str='yfinance')-> pd.DataFrame:
        prices_list = []
        
        if not isinstance(symbols, list):
            try: 
                symbols = list(symbols)
            except:
                raise ValueError
            
        for ticker in tqdm(symbols):
            if src == 'yfinance':
                stock = yf.Ticker(ticker)
                price_info = stock.history(start=self.start_date, end=self.end_date)
            elif src == 'fdr':
                price_info = fdr.DataReader(ticker, start=self.start_date, end=self.end_date)
            elif src == 'fred':
                price_info = web.DataReader(ticker, "fred", start=self.start_date, end=self.end_date)
            
            time.sleep(1)

            price_info['ticker'] = ticker
            prices_list.append(price_info)
        
        prices_df = pd.concat(prices_list)
        return prices_df
    
    def remake_df(self, prices_df:pd.DataFrame) -> pd.DataFrame:
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

    def df_intersection(self, df1, df2) -> tuple[pd.DataFrame,pd.DataFrame]:
        common_index = df1.index.intersection(df2.index)
        df1 = df1.loc[common_index]
        df2 = df2.loc[common_index]
        return df1, df2
