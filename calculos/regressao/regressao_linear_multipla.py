import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

'''###############################
    https://www4.eco.unicamp.br/docentes/gori/images/arquivos/EconometriaI/Econometria_RegressaoMultipla.pdf

    Implementação do Calculos de
    Regressão linear multipla

    Aqui não retorna uma reta mas sim um hiperplano

    
    ######
    A equação é: ŷ = b0 + b1 * x1 + b2 * x2 + ..... bn xn

    ŷ = preco previsto
    b0 e b1 e b2 = coeficientes
    x1 = var_01
    x2 = var_02


    ######
                         _         _        _                _ 
    Para calcular o b0 = y - b1 * x1 - b2 * x2 + ..... bn * xn
    _
    y = Media de valores de y                       
    _
    x = Media de valores de x

    ######
    Para calcular o b1:
    B1 e B2 é igual ao Somatório do produto de (xI menos media de X) vezes (yI menos a media de de Y) dividido pelo
    somatório de (xI - media de X) ao quadrado

                    _          _
            { (xI - x) * (yI - y)
     bX =         -------------
                     _
            {  (xI - x)²

    b0 é o ponto de encontro da reta onde se toca no eixo Y
    b1 é a inclinação da reta (positivo = reta crecente / negativo = reta decrecente) - taxa de variacao

    
    Além da regressão linear, existe outros modelos : quadratica, exponencial, logaritima
###############################'''



def minimos_quadrados(df, df_eixo_x, df_eixo_y, eixo, mean_x, mean_y):
    df[f'xI{eixo} - X{eixo}'] = df_eixo_x - mean_x 
    df['yI - Y'] = df_eixo_y - mean_y
    df[f'xI{eixo} - X{eixo} * yI - Y'] = df[f'xI{eixo} - X{eixo}'] * df['yI - Y']
    sum_x_y = df[f'xI{eixo} - X{eixo} * yI - Y'].sum()
    df[f'xI{eixo} - X{eixo} squared'] = df[f'xI{eixo} - X{eixo}'] ** 2
    sum_x_squared = df[f'xI{eixo} - X{eixo} squared'].sum()

    bx = sum_x_y / sum_x_squared
    return bx, df

dados = {
    'eixo_y':[100000,200000,120000,200000],
    'eixo_x1':[2,4,3,5],
    'eixo_x2':[200,450,320,470],
}

df = pd.DataFrame(dados)

df_eixo_y = df['eixo_y']
df_eixo_x1 = df['eixo_x1']
df_eixo_x2 = df['eixo_x2']

mean_y = df_eixo_y.mean()
mean_x1 = df_eixo_x1.mean()
mean_x2 = df_eixo_x2.mean()


b1, df = minimos_quadrados(df, df_eixo_x1, df_eixo_y, str(1), mean_x1, mean_y)
b2, df = minimos_quadrados(df, df_eixo_x2, df_eixo_y, str(2), mean_x2, mean_y)

b0 = mean_y - (b1 * mean_x1) - (b1 * mean_x2)

#########
# Agora efetivamente se obtem o valor estimado
# para a pesquisa conforme o 'treinamento' 
# b0 e b1 são os produtos do treinamento
valor_x1_avaliado = 4
valor_x2_avaliado = 450
y_estimado =  b0 + (b1 * valor_x1_avaliado) + (b2 * valor_x2_avaliado) 


print('\n')
print(f'Coenficiente linear: {b0}')
print(f'Coeficiente angular x1: {b1}')
print(f'Coeficiente angular x2: {b1}')
print(f"Valor estimado de x1 = {valor_x1_avaliado} e x2 = {valor_x2_avaliado} no eixo y é {y_estimado}")

print('\n')

print(df)

# Coeficiente de Determinação
y_predicted = b0 + b1 * df['eixo_x1'] + b2 * df['eixo_x2']  # Valores previstos pelo modelo de regressão
residuals = df['eixo_y'] - y_predicted                      # Calcular os resíduos
sse = np.sum(residuals ** 2)                                # Calcular SSE (Sum of Squared Errors)
sst = np.sum((df['eixo_y'] - mean_y) ** 2)                  # Calcular SST (Total Sum of Squares)
r_squared = 1 - (sse / sst)                                 # Calcular R²




fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(df['eixo_x1'], df['eixo_y'], df['eixo_x2'])
ax.set_xlabel('eixo_y - n° Quatos')
ax.set_ylabel('eixo_x1 - valor')
ax.set_zlabel('eixo_x2 - m²')

plt.show()
