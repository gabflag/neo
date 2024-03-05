import pandas as pd
from matplotlib import pyplot
import numpy as np
import uuid



def imprimindo(df_eixo_x, df_eixo_y, b0, b1, valor_x_avaliado, y_estimado, save_image):
    pyplot.scatter(df_eixo_x, df_eixo_y)
    pyplot.plot(valor_x_avaliado, y_estimado, marker='o', markersize=12, color='green') 
    pyplot.plot(df_eixo_x, b0 + b1 * df_eixo_x, color='red') # faço uma reta com base no valor perfeito para o eixo x
    pyplot.xlabel('Eixo X')
    pyplot.ylabel('Eixo Y')
    pyplot.title('Regressão Linear Simples')

    if save_image:
        filename = 'imagens/testes/' + str(uuid.uuid4()) + '.png'
        pyplot.savefig(filename)

    pyplot.show()



def minimos_quadrados(df, df_eixo_x, df_eixo_y, eixo, mean_x, mean_y):
    df[f'xI{eixo} - X{eixo}'] = df_eixo_x - mean_x 
    df['yI - Y'] = df_eixo_y - mean_y
    df[f'xI{eixo} - X{eixo} * yI - Y'] = df[f'xI{eixo} - X{eixo}'] * df['yI - Y']
    sum_x_y = df[f'xI{eixo} - X{eixo} * yI - Y'].sum()
    df[f'xI{eixo} - X{eixo} squared'] = df[f'xI{eixo} - X{eixo}'] ** 2
    sum_x_squared = df[f'xI{eixo} - X{eixo} squared'].sum()

    bx = sum_x_y / sum_x_squared
    return bx, df


def main(df, eixo_x, eixo_y, valor_x_avaliado, imprimir=False, save_image=False):
    df_eixo_x = df[eixo_x]
    df_eixo_y = df[eixo_y]

    mean_x = df_eixo_x.mean()
    mean_y = df_eixo_y.mean()

    b1, df = minimos_quadrados(df, df_eixo_x, df_eixo_y, str(1), mean_x, mean_y)
    b0 = mean_y - b1 * mean_x

    y_estimado =  b0 + b1 * valor_x_avaliado

    #########
    # Coeficiente de Determinação
    y_predicted = b0 + b1 * df_eixo_x       # Valores previstos pelo modelo de regressão
    residuals = df_eixo_y - y_predicted     # Calcular os resíduos
    sse = np.sum(residuals ** 2)            # Calcular SSE (Sum of Squared Errors)
    sst = np.sum((df_eixo_y - mean_y) ** 2) # Calcular SST (Total Sum of Squares)
    r_squared = 1 - (sse / sst)             # Calcular R²


    print('\n')
    print(f'Coenficiente linear: {b0}')
    print(f'Coeficiente angular: {b1}')
    print(f"Valor estimado de x = {valor_x_avaliado} no eixo y é {y_estimado}")
    print("Coeficiente de Determinação (R²):", r_squared)

    if imprimir:
        imprimindo(df_eixo_x, df_eixo_y, b0, b1, valor_x_avaliado, y_estimado, save_image)



'''
# Descomente o código para visualizar

df = pd.read_csv("/home/gabriel/Desktop/Codes/neo/banco_de_dados/candles/acoes/SP500_total_1_D.csv")
eixo_x='Close'
eixo_y='Volume'
valor_x_avaliado=5000

main(df, eixo_x, eixo_y, valor_x_avaliado, imprimir=True)
'''
