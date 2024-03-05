import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

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

    df['dif_percentual_close'] = calcular_diferenca_percentual(df['Open'].shift(1), df['Open'])
    return df


def adicionar_dados(df):
    pd.options.mode.chained_assignment = None  # default='warn'
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Date'].dt.year >= 2023]

    decomposicao = seasonal_decompose(df["Close"], model="additive", period=30, extrapolate_trend=30)

    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Day_of_week'] = df['Date'].dt.day_of_week
    df = diferencas_percentuais(df)
    
    return df


def main():
    df = pd.read_csv("/home/gabriel/Desktop/Codes/neo/banco_de_dados/candles/acoes/SP500_total_1_D.csv")

    #decomposicao = seasonal_decompose(df["Close"], model="additive", period=30, extrapolate_trend=30)
    df = adicionar_dados(df)
    print(df.head())

    ###############################
    # Mostrando o Dataframe
    ##############################
    # plt.plot(df['Date'],df['Close'])
    # plt.xlabel('Date')
    # plt.ylabel('Close Price')
    # plt.title('Analise')
    # plt.show()


    ##############################
    # Mostrandos os dados do seasonal_decompose
    ############################## 

    # ax, fig = plt.subplots(figsize=(15,8))
    # plt.plot(decomposicao.observed)
    # plt.plot(decomposicao.trend)
    # plt.show()

    #############################
    # Mostrandos todos os dados do 
    # seasonal_decompose
    #############################

    # decomposicao.observed.index = df['Date']
    # decomposicao.trend.index = df['Date']
    # decomposicao.seasonal.index = df['Date']
    # decomposicao.resid.index = df['Date']


    # fig, (ax1,ax2,ax3,ax4) = plt.subplots(4,1, figsize=(15,8))
    # ax1.plot(decomposicao.observed)
    # ax1.set_title('Observed')

    # ax2.plot(decomposicao.trend)
    # ax2.set_title('Trend')
    # ax3.plot(decomposicao.seasonal)
    # ax3.set_title('Seasonal')
    # ax4.plot(decomposicao.resid)
    # ax4.set_title('Residual')

    # # Ajustando o layout para evitar sobreposição
    # plt.tight_layout()
    # plt.show()

main()