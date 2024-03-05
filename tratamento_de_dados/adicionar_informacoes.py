import pandas as pd


def calcular_diferenca_percentual(valor_antigo, valor_novo):
    '''
    Calcula a diferença percentual entre os valores
    '''

    diferenca = valor_novo - valor_antigo
    diferenca_percentual = (diferenca / abs(valor_antigo)) * 100
    return diferenca_percentual

def diferencas_percentuais(df):
    '''
    Adiciona ao dataframe as diferencas percentuais.
    Recebe um dataframe e retorna um dataframe
    '''

    df['dif_percentual_open'] = calcular_diferenca_percentual(df['Open'].shift(1), df['Open'])
    df['dif_percentual_high'] = calcular_diferenca_percentual(df['High'].shift(1), df['High'])
    df['dif_percentual_low'] = calcular_diferenca_percentual(df['Low'].shift(1), df['Low'])
    df['dif_percentual_close'] = calcular_diferenca_percentual(df['Close'].shift(1), df['Close'])

    df['dif_percentual_open_close'] = calcular_diferenca_percentual(df['Open'].shift(1), df['Close'])
    df['dif_percentual_higth_low'] = calcular_diferenca_percentual(df['High'].shift(1), df['Low'])

    df['dif_percentual_media'] = calcular_diferenca_percentual(df['media_valores'].shift(1), df['media_valores'])

    return df


def calcule_rsi(df, periods):
    '''
    Funcao que redecebe um dataframe e calcula o rsi

    Para calcular o rsi é necessário setar a quantidade de periodos 
    que irá ser utilizada para fazer o calculo.
    '''

    close_return = df['Close'] / df['Close'].shift(1) - 1

    up = close_return.clip(lower=0)
    down = -1 * close_return.clip(upper=0)
    
    move_avarage_up = up.rolling(window=periods).mean()
    move_avarage_down = down.rolling(window=periods).mean()

    rs = move_avarage_up / move_avarage_down
    rsi = 100 - (100 / (1 + rs))

    return rsi

def rsi(df, periodos):
    '''
    Adiciona ao dataframe os valores de rsi
    Recebe um dataframe e retorna um dataframe
    '''
    range_periods_rsi = range(2,periodos)
    for rsi in range_periods_rsi:
        rsi_collum_name = 'rsi_' +  str(rsi)
        df[rsi_collum_name] = calcule_rsi(df, rsi)
    
    return df


def calcula_media_movel_simples(df, ma):
    '''
    Calcula a média móvel simples (SMA) no DataFrame.
    '''

    sma_column_open = 'sma_open_' + str(ma)
    sma_column_close = 'sma_close_' + str(ma)
    sma_column_high = 'sma_high_' + str(ma)
    sma_column_low = 'sma_low_' + str(ma)
    sma_column_media = 'media_valores_' + str(ma)

    df[sma_column_open] = df['Open'].rolling(window=ma).mean()
    df[sma_column_close] = df['High'].rolling(window=ma).mean()
    df[sma_column_high] = df['Low'].rolling(window=ma).mean()
    df[sma_column_low] = df['Close'].rolling(window=ma).mean()
    df[sma_column_media] = df['Close'].rolling(window=ma).mean()

    return df

def sma(df,periodos):
    range_periods_sma = range(2,periodos)
    for sma in range_periods_sma:
        df = calcula_media_movel_simples(df, sma)
    return df


def calcula_media_movel_exponencial(df, ma):
    '''
    Calcula a média móvel exponencial (EMA) no DataFrame.
    ewm() (exponential weighted moving average)
    '''

    ema_column_open = 'ema_open_' + str(ma)
    ema_column_close = 'ema_close_' + str(ma)
    ema_column_high = 'ema_high_' + str(ma)
    ema_column_low = 'ema_low_' + str(ma)
    ema_column_media = 'media_valores_' + str(ma)

    df[ema_column_open] = df['Open'].ewm(span=ma, adjust=False).mean()
    df[ema_column_close] = df['High'].ewm(span=ma, adjust=False).mean()
    df[ema_column_high] = df['Low'].ewm(span=ma, adjust=False).mean()
    df[ema_column_low] = df['Close'].ewm(span=ma, adjust=False).mean()
    df[ema_column_media] = df['Close'].ewm(span=ma, adjust=False).mean()

    return df

def ema(df, periodos):
    range_periods_ema = range(2, periodos)
    for ema in range_periods_ema:
        df = calcula_media_movel_exponencial(df, ema)
    return df


def main():
    caminho_df = 'banco_de_dados/candles/pares_de_moedas/EURUSD_2024-02-02-2024-02-29_1mes_candle.csv'
    df = pd.read_csv(caminho_df)

    df['media_valores'] = df[['Open', 'High', 'Low', 'Close']].mean(axis=1)

    periodos = 10

    df = diferencas_percentuais(df)
    df = rsi(df, periodos)

    df = sma(df, periodos)
    df = ema(df, periodos)

    df.to_csv('/home/gabriel/Desktop/Codes/neo/tratamento_de_dados/tratados.csv')

main()

