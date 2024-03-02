import yfinance as yf

def baixar_dados():
    '''
    Funçao para baixar os dados do Petrobras dos ultimos 7 dias
    com o timeframe de 1 minuto. O YahooFinance permite baixar apenas
    7 dias quando o timeframe é de 1 minuto
    '''
    data = yf.download(tickers=['EURUSD=X'], period='1mo', interval="5m")
    data.to_csv('EURUSD_5_min.csv')

    # Exibir os primeiros registros dos dados
    print(data.head())

baixar_dados()