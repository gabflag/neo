import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.environ.get('CAMINHO_DIRETORIOS_DE_ESTRATEGIAS'))
from estrategias import rsi

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def mostrar_resultado():
    '''
    Mostrar a tabela similar a que temos no metatrader.
    Recebe um dataframe com as operações realizadas
    e retorna os resultados visualmente explicativas
    '''
    pass


def mostrar_grafico_operacao_rsi(valor_inicial, df_group_trades_raw, df):
    '''
    Recebe o valor inicial do investimento, o dataframe com o conjunto de 
    operações realizadas, e o dataframe com os dados para formular o dados utilizados como
    base de preços do ativo que foi utilizado nas negociações
    '''

    print(f'Valor final: {valor_inicial}')
    print(f'Resultado final: {df_group_trades_raw["resultado"].sum()}')
    print(f'Maior resultado: {df_group_trades_raw["resultado"].max()}')
    print(f'Menor resultado: {df_group_trades_raw["resultado"].min()}')
    
    print(f'Media resultados comprados: {df_group_trades_raw[df_group_trades_raw["kind"] == "Close Buy"]["resultado"].mean() }')
    print(f'Media resultados venda: {df_group_trades_raw[df_group_trades_raw["kind"] == "Close Sell"]["resultado"].mean() }')

    # Criando e Plotando no gráfico
    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], vertical_spacing=0.02, shared_xaxes=True)
    
    # O gráfico
    fig.add_trace(go.Candlestick(x=df['Datetime'],
                                open=df['Open'],
                                high=df['High'],
                                low=df['Low'],
                                close=df['Close']), row=1, col=1)

    # Operações no gráfico
    df_buy = df_group_trades_raw[df_group_trades_raw['kind'] == 'buy']
    df_sell = df_group_trades_raw[df_group_trades_raw['kind'] == 'sell']

    df_close_buy = df_group_trades_raw[df_group_trades_raw['kind'] == 'Close Buy']
    df_close_sell = df_group_trades_raw[df_group_trades_raw['kind'] == 'Close Sell']
    
    fig.add_trace(go.Scatter(x=df_buy.index,
                             y=df_buy['price'],
                             marker_color='#11dd11',
                             marker_size=15,
                             mode='markers',
                             marker_symbol='triangle-up',
                             name='Compra Aberta'), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df_sell.index,
                            y=df_sell['price'],
                            marker_color='#993399',
                            marker_size=15,
                            mode='markers',
                            marker_symbol='triangle-down',
                            name='Venda Aberta'), row=1, col=1)


    fig.add_trace(go.Scatter(x=df_close_buy.index,
                            y=df_close_buy['price'],
                            marker_color='#ffff00',
                            marker_size=5,
                            mode='markers',
                            marker_symbol='circle',
                            name='Compra Fechada'), row=1, col=1)
    

    fig.add_trace(go.Scatter(x=df_close_sell.index,
                        y=df_close_sell['price'],
                        marker_color='#0000ff',
                        marker_size=5,
                        mode='markers',
                        marker_symbol='circle',
                        name='Venda Fechada'), row=1, col=1)

    
    # # Adicionando Grafico RSI do RSI
    # fig.add_trace(go.Scatter(x=df['Datetime'],
    #                         y=df['rsi'],
    #                         name=f'RSI'), row=2, col=1)
    
    # Criando um dicionário de limitação de hora e dias que devem ser excluidos, como é bitcoin
    #fig.update_xaxes(rangebreaks=[dict(bounds=[17,10], pattern='hour'), dict(bounds=['sat','mon'])])
    
    # Remove uma tela que tem de baixo
    fig.update_layout(height=800, xaxis_rangeslider_visible=False)
    fig.show()


def main():
    banco_de_dados = os.environ.get('BTC_USD_23_11_03_23_12_03_1MES_CANDLE')
    
    df = pd.read_csv(banco_de_dados)
    valor_inicial = 100000
    bet_size = 100
    periodos_rsi = 14
    rsi_base = 20
    rsi_teto = 85
    percentual_compra = 1.005
    percentual_venda = 0.997

    # Resultado Operacaoes e Grafico
    df_group_trades_raw = rsi.operando_com_rsi(banco_de_dados, valor_inicial, bet_size, periodos_rsi, rsi_base, rsi_teto, percentual_compra, percentual_venda)
    
    mostrar_grafico_operacao_rsi(valor_inicial, df_group_trades_raw, df)


main()

