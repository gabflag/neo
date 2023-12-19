import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.environ.get('CAMINHO_DIRETORIOS_DE_ESTRATEGIAS'))
from estrategias import rsi
import time
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def realiza_trades(df_group_trades_raw, df):
    '''
    Recebe o valor inicial do investimento, o dataframe com o conjunto de 
    operações realizadas, e o dataframe com os dados para formular o dados utilizados como
    base de preços do ativo que foi utilizado nas negociações

    Tempo de execução as informações visuais: 0.3834671974182129
    '''

    resultados_df = pd.DataFrame(columns=[
        'Valor final investido',
        'Resultado percentual final',
        'Maior resultado operacao fechada',
        'Menor resultado percentual de operação fechada',
        'Quantidade de operações positivas',
        'Percentual de operações positivas',
        'Quantidade de operações negativas',
        'Percentual de operações negativas',
        'Media resultados comprados',
        'Media resultados venda',
        'Número abertura de compra',
        'Número abertura de venda',
        'Número fechamento de compra',
        'Número fechamento de venda',
        'Total de operações abertas',
        'Total de operações finalizadas',
        'Maior rebaixamento ma conta durante operacoes',
        'Maior valor alcançado na conta durante operacoes'
    ])


    # Criando e Plotando no gráfico
    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], vertical_spacing=0.02, shared_xaxes=True)
    
    # O gráfico
    fig.add_trace(go.Candlestick(x=df['Datetime'],
                                open=df['Open'],
                                high=df['High'],
                                low=df['Low'],
                                close=df['Close']), row=1, col=1)

    # Operações no gráfico
    df_buy = df_group_trades_raw[df_group_trades_raw['kind'] == 'Buy']
    df_sell = df_group_trades_raw[df_group_trades_raw['kind'] == 'Sell']
    df_close_buy = df_group_trades_raw[df_group_trades_raw['kind'] == 'Close Buy']
    df_close_sell = df_group_trades_raw[df_group_trades_raw['kind'] == 'Close Sell']
    
    # Obter o número de linhas para df_close_buy
    num_linhas_buy = df_buy.shape[0]
    num_linhas_sell = df_sell.shape[0]
    num_linhas_close_buy = df_close_buy.shape[0]
    num_linhas_close_sell = df_close_sell.shape[0]

    # Total de operações
    total_operacoes = num_linhas_close_buy + num_linhas_close_sell
    

    valor_final = df_group_trades_raw["valor_investimento"].iloc[-1]
    if pd.isna(valor_final):
        valor_final = df_group_trades_raw["durante_operacao"].iloc[-1]

    # Contagem de operações positivas e negativas
    quantidade_operacoes_positivas = (df_group_trades_raw["diferenca_percentual"] > 0).sum()
    quantidade_operacoes_negativas = (df_group_trades_raw["diferenca_percentual"] < 0).sum()

    percentual_positivas = (quantidade_operacoes_positivas / total_operacoes) * 100
    percentual_negativas = (quantidade_operacoes_negativas / total_operacoes) * 100

    resultados = {
        'Valor final investido': valor_final,
        'Resultado percentual final': df_group_trades_raw["diferenca_percentual"].sum(),
        'Maior resultado operacao fechada': df_group_trades_raw["diferenca_percentual"].max(),
        'Menor resultado percentual de operação fechada': df_group_trades_raw["diferenca_percentual"].min(),
        'Quantidade de operações positivas': quantidade_operacoes_positivas,
        'Percentual de operações positivas': percentual_positivas,
        'Quantidade de operações negativas': quantidade_operacoes_negativas,
        'Percentual de operações negativas': percentual_negativas,
        'Media resultados comprados': df_group_trades_raw[df_group_trades_raw["kind"] == "Close Buy"]["diferenca_percentual"].mean(),
        'Media resultados venda': df_group_trades_raw[df_group_trades_raw["kind"] == "Close Sell"]["diferenca_percentual"].mean(),
        'Número abertura de compra': num_linhas_buy,
        'Número abertura de venda': num_linhas_sell,
        'Número fechamento de compra': num_linhas_close_buy,
        'Número fechamento de venda': num_linhas_close_sell,
        'Total de operações abertas': num_linhas_buy + num_linhas_sell,
        'Total de operações finalizadas': total_operacoes,
        'Maior rebaixamento ma conta durante operacoes': df_group_trades_raw["durante_operacao"].min(),
        'Maior valor alcançado na conta durante operacoes': df_group_trades_raw["durante_operacao"].max()
    }

    # Adição do dicionário como uma nova linha no DataFrame
    resultados_df = resultados_df._append(resultados, ignore_index=True)

    return resultados_df


def mostrar_grafico_operacao_rsi(df_group_trades_raw, df):
    '''
    Recebe o valor inicial do investimento, o dataframe com o conjunto de 
    operações realizadas, e o dataframe com os dados para formular o dados utilizados como
    base de preços do ativo que foi utilizado nas negociações

    Com as informações visuais: 0.5616054534912109
    Sem as informações visuais: 
    '''
    resultados_df = pd.DataFrame(columns=[
        'Valor final investido',
        'Resultado percentual final',
        'Maior resultado operacao fechada',
        'Menor resultado percentual de operação fechada',
        'Quantidade de operações positivas',
        'Percentual de operações positivas',
        'Quantidade de operações negativas',
        'Percentual de operações negativas',
        'Media resultados comprados',
        'Media resultados venda',
        'Número abertura de compra',
        'Número abertura de venda',
        'Número fechamento de compra',
        'Número fechamento de venda',
        'Total de operações abertas',
        'Total de operações finalizadas',
        'Maior rebaixamento ma conta durante operacoes',
        'Maior valor alcançado na conta durante operacoes'
    ])


    # Criando e Plotando no gráfico
    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], vertical_spacing=0.02, shared_xaxes=True)
    
    # O gráfico
    fig.add_trace(go.Candlestick(x=df['Datetime'],
                                open=df['Open'],
                                high=df['High'],
                                low=df['Low'],
                                close=df['Close']), row=1, col=1)

    # Operações no gráfico
    df_buy = df_group_trades_raw[df_group_trades_raw['kind'] == 'Buy']
    df_sell = df_group_trades_raw[df_group_trades_raw['kind'] == 'Sell']
    df_close_buy = df_group_trades_raw[df_group_trades_raw['kind'] == 'Close Buy']
    df_close_sell = df_group_trades_raw[df_group_trades_raw['kind'] == 'Close Sell']
    
    # Obter o número de linhas para df_close_buy
    num_linhas_buy = df_buy.shape[0]
    num_linhas_sell = df_sell.shape[0]
    num_linhas_close_buy = df_close_buy.shape[0]
    num_linhas_close_sell = df_close_sell.shape[0]

    # Total de operações
    total_operacoes = num_linhas_close_buy + num_linhas_close_sell
    

    valor_final = df_group_trades_raw["valor_investimento"].iloc[-1]
    if pd.isna(valor_final):
        valor_final = df_group_trades_raw["durante_operacao"].iloc[-1]

    # Contagem de operações positivas e negativas
    quantidade_operacoes_positivas = (df_group_trades_raw["diferenca_percentual"] > 0).sum()
    quantidade_operacoes_negativas = (df_group_trades_raw["diferenca_percentual"] < 0).sum()

    percentual_positivas = (quantidade_operacoes_positivas / total_operacoes) * 100
    percentual_negativas = (quantidade_operacoes_negativas / total_operacoes) * 100

    resultados = {
        'Valor final investido': valor_final,
        'Resultado percentual final': df_group_trades_raw["diferenca_percentual"].sum(),
        'Maior resultado operacao fechada': df_group_trades_raw["diferenca_percentual"].max(),
        'Menor resultado percentual de operação fechada': df_group_trades_raw["diferenca_percentual"].min(),
        'Quantidade de operações positivas': quantidade_operacoes_positivas,
        'Percentual de operações positivas': percentual_positivas,
        'Quantidade de operações negativas': quantidade_operacoes_negativas,
        'Percentual de operações negativas': percentual_negativas,
        'Media resultados comprados': df_group_trades_raw[df_group_trades_raw["kind"] == "Close Buy"]["diferenca_percentual"].mean(),
        'Media resultados venda': df_group_trades_raw[df_group_trades_raw["kind"] == "Close Sell"]["diferenca_percentual"].mean(),
        'Número abertura de compra': num_linhas_buy,
        'Número abertura de venda': num_linhas_sell,
        'Número fechamento de compra': num_linhas_close_buy,
        'Número fechamento de venda': num_linhas_close_sell,
        'Total de operações abertas': num_linhas_buy + num_linhas_sell,
        'Total de operações finalizadas': total_operacoes,
        'Maior rebaixamento ma conta durante operacoes': df_group_trades_raw["durante_operacao"].min(),
        'Maior valor alcançado na conta durante operacoes': df_group_trades_raw["durante_operacao"].max()
    }

    # Adição do dicionário como uma nova linha no DataFrame
    resultados_df = resultados_df._append(resultados, ignore_index=True)

    print('\n# # # # # # ')
    print(f'Valor final investido 1000 reais: {valor_final}')
    print(f'Resultado percentual final: {df_group_trades_raw["diferenca_percentual"].sum()}')
    
    print('\n# # # # # # ')
    print(f'Maior resultado operacao fechada: {df_group_trades_raw["diferenca_percentual"].max()}')
    print(f'Menor resultado percentual de operação fechada: {df_group_trades_raw["diferenca_percentual"].min()}')

    print(f'Quantidade de operações positivas: {quantidade_operacoes_positivas} aproximadamente {percentual_positivas:.2f}%')
    print(f'Quantidade de operações negativas: {quantidade_operacoes_negativas} aproximadamente {percentual_negativas:.2f}%')

    print('\n# # # # # # ')
    print(f'Media resultados comprados: {df_group_trades_raw[df_group_trades_raw["kind"] == "Close Buy"]["diferenca_percentual"].mean() }')
    print(f'Media resultados venda: {df_group_trades_raw[df_group_trades_raw["kind"] == "Close Sell"]["diferenca_percentual"].mean() }')

    print('\n# # # # # # ')
    print(f"Número abertura de compra: {num_linhas_buy}")
    print(f"Número abertura de venda: {num_linhas_sell}")
    print(f"Número fechamento de compra: {num_linhas_close_buy}")
    print(f"Número fechamento de venda: {num_linhas_close_sell}")
    print(f'Total de operações abertas: {num_linhas_buy + num_linhas_sell}')
    print(f'Total de operações finalizadas: {total_operacoes}')

    print('\n# # # # # # ')
    print(f'Maior rebaixamento ma conta durante operacoes: {df_group_trades_raw["durante_operacao"].min()}')
    print(f'Maior valor alcançado na conta durante operacoes: {df_group_trades_raw["durante_operacao"].max()}')

    print('\n\n')


    fig.add_trace(go.Scatter(x=df_buy.index,
                             y=df_buy['preco_de_abertura'],
                             marker_color='#11dd11',
                             marker_size=15,
                             mode='markers',
                             marker_symbol='triangle-up',
                             name='Compra Aberta'), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df_sell.index,
                            y=df_sell['preco_de_abertura'],
                            marker_color='#993399',
                            marker_size=15,
                            mode='markers',
                            marker_symbol='triangle-down',
                            name='Venda Aberta'), row=1, col=1)


    fig.add_trace(go.Scatter(x=df_close_buy.index,
                            y=df_close_buy['preco_de_fechamento'],
                            marker_color='#ffff00',
                            marker_size=5,
                            mode='markers',
                            marker_symbol='circle',
                            name='Compra Fechada'), row=1, col=1)
    

    fig.add_trace(go.Scatter(x=df_close_sell.index,
                        y=df_close_sell['preco_de_fechamento'],
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
    valor_inicial = 1000
    bet_size = 1
    periodos_rsi = 14
    rsi_base = 20
    rsi_teto = 85
    percentual_compra = 1.005
    percentual_venda = 0.997

    resultados = []

    for periodos_rsi in range(14, 16):
        for rsi_base in range(15, 20):
            for rsi_teto in range(80,85):
                df_group_trades_raw = rsi.operando_com_rsi(banco_de_dados, valor_inicial, bet_size, periodos_rsi, rsi_base, rsi_teto, percentual_compra, percentual_venda)
                df_resultado = realiza_trades(df_group_trades_raw, df)


                resultados.append({
                    'periodos_rsi': periodos_rsi,
                    'rsi_base': rsi_base,
                    'rsi_teto': rsi_teto,
                    'resultado_df': df_resultado.iloc[0]      
            })

    resultados_df = pd.DataFrame(resultados)
    resultados_df.to_csv('resultados_completos.csv', index=False)


def calcular_tempo_total(segundos_por_execucao, numero_de_execucoes):
    tempo_total_segundos = segundos_por_execucao * numero_de_execucoes
    minutos, segundos = divmod(tempo_total_segundos, 60)
    horas, minutos = divmod(minutos, 60)

    print(f"\n\nTempo total estimado para testar todos os parametros: {horas} horas, {minutos} minutos e {segundos} segundos.\n\n")


'''
    # PARA ESTIMAR O TEMPO DE EXCECUCAO
    start_time = time.time()

    df_group_trades_raw = rsi.operando_com_rsi(banco_de_dados, valor_inicial, bet_size, periodos_rsi, rsi_base, rsi_teto, percentual_compra, percentual_venda)
    df_resultado = realiza_trades(df_group_trades_raw, df)
    
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"A função levou {elapsed_time} segundos para ser executada.")

'''
main()
#calcular_tempo_total(5, 50)