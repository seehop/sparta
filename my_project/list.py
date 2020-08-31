import pandas as pd

stock_list=pd.read_csv('data.csv')
stock_code=stock_list[['종목코드','기업명']]