# https://www.cboe.com/us/equities/market_statistics/listed_symbols/
# https://finance.yahoo.com/calendar/

import yfinance as yf

def baixar_dados():
    '''
    Funçao para baixar os dados do Petrobras dos ultimos 7 dias
    com o timeframe de 1 minuto. O YahooFinance permite baixar apenas
    7 dias quando o timeframe é de 1 minuto
    '''
    data = yf.download(tickers=['YM=F'], period='Max', interval="1D")
    data.to_csv('10_Year_T_NoteFutures_total_1_D.csv')

    # Exibir os primeiros registros dos dados
    print(data.head())

baixar_dados()

