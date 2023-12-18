
import pandas as pd


def get_rsi(df, periods):

    close_return = df['Close'] / df['Close'].shift(1) - 1
    
    up = close_return.clip(lower=0)
    down = -1 * close_return.clip(upper=0)
    
    move_avarage_up = up.rolling(window=periods).mean()
    move_avarage_down = down.rolling(window=periods).mean()

    rs = move_avarage_up / move_avarage_down
    rsi = 100 - (100 / (1 + rs))
    return rsi


def verifica_variacao_compra(valor_anterior, valor_atual, percentual_compra):
    '''
    Função que verifica se um número atual é maior do que a variação
    percentual de um número anterior.

    Recebe o número anterior, o valor atual e o percentual
    '''
    if valor_atual >= (valor_anterior * percentual_compra):
        return True
    else:
        return False
    

def verifica_variacao_venda(valor_anterior, valor_atual, percentual):
    '''
    Função que verifica se um número atual é menor do que a variação
    percentual de um número anterior.

    Recebe o número anterior, o valor atual e o percentual
    '''
    if valor_atual <= (valor_anterior * percentual):
        return True
    else:
        return False


def operando_com_rsi(banco_de_dados, valor_inicial, bet_size, periodos_rsi, rsi_base, rsi_teto, percentual_compra, percentual_venda):

    '''
    Operações simuladas com o RSI

    Estratégia Base:
        Quando passar o ponto superior do RSI irá ser dando uma ordem de venda.
        Quando passar o ponto inferiior do RSI irá ser dando uma ordem de compra.
        A regras de saida em nivel percentual de lucro do valor de entrada e venda são definidas nas variaveis 'percentual_compra' 'percentual_venda'
        bet_size é a forma padrão para simular o contrato, volume, quantidade de ativos adiquiridos
    
    '''

    df = pd.read_csv(banco_de_dados)
    df['rsi'] = get_rsi(df, periodos_rsi)

    list_trades = []
    comprado = vendido = operando = False
    valor_ao_abrir_posicao = 0
    
    for idx, row in df.iterrows():
   
        atingiu_objetivo_compra = verifica_variacao_compra(valor_ao_abrir_posicao, row['Close'], percentual_compra)    
        atingiu_objetivo_venda = verifica_variacao_venda(valor_ao_abrir_posicao, row['Close'], percentual_venda)    
      
        ##########################
        ######### Fechar operações

        # Fechar operacao vendido
        if (row['rsi'] <= rsi_base and operando and vendido) or (atingiu_objetivo_venda and operando and vendido):
            resultado = valor_ao_abrir_posicao - row['Close']
            valor_inicial += resultado
            valor_ao_abrir_posicao = 0
            vendido = operando = False
            list_trades += [{'price': row['Close'], 'time': row['Datetime'], 'kind':'Close Sell', 'quantity':bet_size, 'resultado':resultado}]


        # Fechar operacao comprado
        elif (row['rsi'] >= rsi_teto and operando and comprado) or (atingiu_objetivo_compra and operando and comprado):
            resultado = row['Close'] - valor_ao_abrir_posicao
            valor_inicial += resultado
            valor_ao_abrir_posicao = 0
            comprado = operando = False
            list_trades += [{'price': row['Close'], 'time': row['Datetime'], 'kind':'Close Buy', 'quantity':bet_size, 'resultado':resultado}]
    
        ##########################
        ######### Abrir operações

        # Comprar
        if row['rsi'] <= rsi_base and operando == False:
            list_trades += [{'price': row['Close'], 'time': row['Datetime'], 'kind':'buy', 'quantity':bet_size, 'resultado': pd.NA}]
            valor_ao_abrir_posicao = row['Close']
            comprado = operando = True
        
        # Vender
        elif row['rsi'] >= rsi_teto and operando == False:
            list_trades += [{'price': row['Close'], 'time': row['Datetime'], 'kind':'sell', 'quantity':bet_size, 'resultado': pd.NA}]
            valor_ao_abrir_posicao = row['Close']
            vendido = operando = True


    # Criando df de operações
    df_group_trades_raw = pd.DataFrame(list_trades)
    df_group_trades_raw.set_index('time', inplace=True)

    return df_group_trades_raw, df

