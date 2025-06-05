from ftplib import FTP
import pandas as pd
from io import StringIO
import yfinance as yf
import time

def get_nasdaq_tickers():
    ftp = FTP('ftp.nasdaqtrader.com')
    ftp.login()
    ftp.cwd('symboldirectory')
    
    def read_file(file):
        buffer = StringIO()
        ftp.retrlines(f"RETR {file}", lambda line: buffer.write(line + '\n'))
        buffer.seek(0)
        df = pd.read_csv(buffer, sep='|')
        df = df[df['ETF'] == 'N']
        df = df[df['Test Issue']=='N']
    
        if 'Symbol' in df.columns:
            symbol_col = 'Symbol'
            df = df[df['Financial Status'] == 'N']
        elif 'ACT Symbol' in df.columns:
            symbol_col = 'ACT Symbol'
            df = df[df['Exchange']=='N']
        else:
            raise ValueError(f"No known symbol column found in {file}")
        return df[symbol_col].tolist()
    

       
    tickers = read_file('nasdaqlisted.txt') + read_file('otherlisted.txt')
    
    print(f"Total tickers before filtering: {len(tickers)}")
    tickers = [t for t in tickers if isinstance(t, str) and t.isalpha()]
    print(f"Total tickers after filtering: {len(tickers)}")
    print(tickers[:10])
    ftp.quit()

    return list(set([t for t in tickers if isinstance(t, str)]))   



### Pull financials from yahoo finance

def get_financial_ratios(ticker):
    print(f"Analyzing: {ticker}")
    try:
        stock = yf.Ticker(ticker)
        income = stock.financials.T
        balance = stock.balance_sheet.T
        if income.empty or balance.empty:
            return None

        latest_income = income.iloc[0]
        latest_balance = balance.iloc[0]
        revenue = latest_income.get('Total Revenue', 0)
        net_income = latest_income.get('Net Income', 0)
        total_assets = latest_balance.get('Total Assets', 0)
        total_liabilities = latest_balance.get('Total Liab', 0)
        pe_ratio_raw = stock.info.get('trailingPE')
        pe_ratio = float(pe_ratio_raw)
        total_equity = total_assets - total_liabilities

        return {
            "Ticker": ticker,
            "Revenue": revenue,
            "NetIncome": net_income,
            "NetMargin": net_income / revenue if revenue else 0,
            "DebtToEquity": total_liabilities / total_equity if total_equity else 0,
            "pe_ratio": pe_ratio
            
        }
    except:
        return None


#define criteria for undervaluation

def is_undervalued(r):
    return (
    r 
    and r['pe_ratio'] is not None
    and r['pe_ratio'] < 15 
    and r['NetIncome'] > 0
    and r['NetMargin'] > 0
    and r['Revenue']  > 0
    )

    
def scan_tickers(tickers, limit=100):
    results = []
    for t in tickers[:limit]: 
        r = get_financial_ratios(t) 
        if is_undervalued(r):
            results.append(r)
        time.sleep(.2)
    return pd.DataFrame(results)

