import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import seaborn as sns
import matplotlib.pyplot as plt


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

    df['rentabilidade'] = calcular_diferenca_percentual(df['Open'].shift(1), df['Open'])
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


dfs_path = [
    '/home/gabriel/Desktop/Codes/neo/banco_de_dados/candles/acoes/DowJones_total_1_D.csv',
    '/home/gabriel/Desktop/Codes/neo/banco_de_dados/candles/acoes/MiniDowJones_Mar24_total_1_D.csv',
    '/home/gabriel/Desktop/Codes/neo/banco_de_dados/candles/acoes/MiniS&P500_Mar24_total_1_D.csv',
    '/home/gabriel/Desktop/Codes/neo/banco_de_dados/candles/acoes/NASDAQ_total_1_D.csv',
    '/home/gabriel/Desktop/Codes/neo/banco_de_dados/candles/acoes/SP500_total_1_D.csv'
]

list_name = [
    'DowJones',
    'MiniDowJones',
    'MiniSP500',
    'NASDAQ',
    'SP500',
]

df_correlacao = pd.DataFrame()
for i in range(0, len(list_name)):
    df = pd.read_csv(str(dfs_path[i]))
    df = adicionar_dados(df)
    df = df.reset_index(drop=True)
    df_correlacao[list_name[i]] = df['rentabilidade']

## Para calcular a correlação é utilizado o método de Pearson, no pandas tem a função corr
print(df_correlacao.head())
print("\n")
print(df_correlacao.corr())


ax, fig = plt.subplots(figsize=(20,5))
ax = sns.heatmap(df_correlacao.corr(), annot=True)
plt.show()