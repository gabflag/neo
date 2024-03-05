import pandas as pd
from matplotlib import pyplot
import numpy as np


def minimos_quadrados(df, df_eixo_x, df_eixo_y, eixo, mean_x, mean_y):
    df[f'xI{eixo} - X{eixo}'] = df_eixo_x - mean_x 
    df['yI - Y'] = df_eixo_y - mean_y
    df[f'xI{eixo} - X{eixo} * yI - Y'] = df[f'xI{eixo} - X{eixo}'] * df['yI - Y']
    sum_x_y = df[f'xI{eixo} - X{eixo} * yI - Y'].sum()
    df[f'xI{eixo} - X{eixo} squared'] = df[f'xI{eixo} - X{eixo}'] ** 2
    sum_x_squared = df[f'xI{eixo} - X{eixo} squared'].sum()

    bx = sum_x_y / sum_x_squared
    return bx, df

def calculo_r(df, coluna_indicador, media_movel):
    df_eixo_x = df[coluna_indicador]
    df_eixo_y = df[media_movel]

    mean_x = df_eixo_x.mean()
    mean_y = df_eixo_y.mean()

    b1, df = minimos_quadrados(df, df_eixo_x, df_eixo_y, str(1), mean_x, mean_y)
    b0 = mean_y - b1 * mean_x

    #########
    # Coeficiente de Determinação
    y_predicted = b0 + b1 * df[coluna_indicador]    # Valores previstos pelo modelo de regressão
    residuals = df_eixo_y - y_predicted     # Calcular os resíduos
    sse = np.sum(residuals ** 2)            # Calcular SSE (Sum of Squared Errors)
    sst = np.sum((df_eixo_y - mean_y) ** 2) # Calcular SST (Total Sum of Squares)
    r_squared = 1 - (sse / sst)             # Calcular R²

    return r_squared

def main():

    caminho_df = '/home/gabriel/Desktop/Codes/neo/tratamento_de_dados/tratados.csv'
    df = pd.read_csv(caminho_df)

    dados = {}
    linha_01 = []
    range_periods = range(2,500)
    for rsi in range_periods:
        rsi_name = 'rsi_'+  str(rsi)
        for media_movel in range_periods:
            sma_name = 'sma_open_' +  str(media_movel)
            resultado_r =  calculo_r(df, rsi_name, sma_name)
            dados = {'rsi' : rsi_name,
                    'media_movel' : sma_name,
                    'resultado_r': resultado_r
                    }
            linha_01.append(dados)

        for media_movel in range_periods:
            sma_name = 'sma_close_' +  str(media_movel)
            resultado_r =  calculo_r(df, rsi_name, sma_name)
            dados = {'rsi' : rsi_name,
                    'media_movel' : sma_name,
                    'resultado_r': resultado_r
                    }
            linha_01.append(dados)


        
        for media_movel in range_periods:
            sma_name = 'sma_high_' +  str(media_movel)
            resultado_r =  calculo_r(df, rsi_name, sma_name)
            dados = {'rsi' : rsi_name,
                    'media_movel' : sma_name,
                    'resultado_r': resultado_r
                    }
            linha_01.append(dados)

        for media_movel in range_periods:
            sma_name = 'sma_low_' +  str(media_movel)
            resultado_r =  calculo_r(df, rsi_name, sma_name)
            dados = {'rsi' : rsi_name,
                    'media_movel' : sma_name,
                    'resultado_r': resultado_r
                    }
            linha_01.append(dados)
            
        for media_movel in range_periods: 
            sma_name = 'media_valores_' +  str(media_movel)
            resultado_r =  calculo_r(df, rsi_name, sma_name)
            dados = {'rsi' : rsi_name,
                    'media_movel' : sma_name,
                    'resultado_r': resultado_r
                    }
            linha_01.append(dados)

    resultados = pd.DataFrame(linha_01)
    resultados.to_csv('resultados_teste.csv')

main()
