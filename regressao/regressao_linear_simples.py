import pandas as pd
from matplotlib import pyplot
import numpy as np

'''###############################

    Implementação do Calculos de
    Regressão linear simples

    A ideia da regressão linear é encontrar uma reta
    que melhor se aproxima dos pontos cardias

    Essa reta fornece uma estimativa dos valores
    pesquisados.
    
    
    ######
    A equação da reta é: ŷ = b0 + b1 * xI
                        
    ######
                             _        _ 
    Para calcular o b0 = y - b1 * x
    _
    y = Media de valores de y                       
    _
    x = Media de valores de x

    ######
    Para calcular o b1:
    B1 é igual ao Somatório do produto de (xI menos media de X) vezes (yI menos a media de de Y) dividido pelo
    somatório de (xI - media de X) ao quadrado

                     _          _
            { (xI - x) * (yI - y)
     b1 =         -------------
                     _
            {  (xI - x)²

    b0 é o ponto de encontro da reta onde se toca no eixo Y
    b1 é a inclinação da reta (positivo = reta crecente / negativo = reta decrecente) - taxa de variacao

    
    Além da regressão linear, existe outros modelos : quadratica, exponencial, logaritima
###############################'''


dados = {
    'eixo_x':[1,2,3,4,5],
    'eixo_y':[3,7,5,11,14]
}

df = pd.DataFrame(dados)
df_eixo_x = df['eixo_x']
df_eixo_y = df['eixo_y']

mean_x = df_eixo_x.mean()
mean_y = df_eixo_y.mean()

df['xI - X'] = df_eixo_x- mean_x
df['yI - Y'] = df_eixo_y - mean_y
df['xI - X * yI - Y'] = df['xI - X'] * df['yI - Y']
sum_x_y = df['xI - X * yI - Y'].sum()

df['xI - X squared'] = df['xI - X'] ** 2
sum_x_squared = df['xI - X squared'].sum()

b1 = sum_x_y / sum_x_squared
b0 = mean_y - b1 * mean_x

#########
# Agora efetivamente se obtem o valor estimado
# para a pesquisa conforme o 'treinamento' 
# b0 e b1 são os produtos do treinamento
valor_x_avaliado = 4
y_estimado =  b0 + b1 * valor_x_avaliado


#########
# Coeficiente de Determinação
y_predicted = b0 + b1 * df['eixo_x']    # Valores previstos pelo modelo de regressão
residuals = df_eixo_y - y_predicted     # Calcular os resíduos
sse = np.sum(residuals ** 2)            # Calcular SSE (Sum of Squared Errors)
sst = np.sum((df_eixo_y - mean_y) ** 2) # Calcular SST (Total Sum of Squares)
r_squared = 1 - (sse / sst)             # Calcular R²


print('\n')
print(f'Coenficiente linear: {b0}')
print(f'Coeficiente angular: {b1}')
print(f"Valor estimado de x = {valor_x_avaliado} no eixo y é {y_estimado}")
print("Coeficiente de Determinação (R²):", r_squared)
print("Coeficiente de Correlação de Pearson")


print('\n')

print(df)




'''###############################
    Coeficiente de Correlação de Pearson 
    
    Quando é uma amostra
    A formula é lida: o coeficiente de correlacao de person entre as variaveis x e y é igual
    covariancia entre x e y dividido pelo desvio padrão de x vezes o desvio padrão de y

        Rxy =    Sxy
                 ---
                Sx * Sy    

    Para uma populalação:
    

###############################'''




pyplot.scatter(df_eixo_x, df_eixo_y)
pyplot.plot(valor_x_avaliado, y_estimado, marker='o', markersize=12, color='green') 
pyplot.plot(df_eixo_x, b0 + b1 * df_eixo_x, color='red') # faço uma reta com base no valor perfeito para o eixo x
pyplot.xlabel('Eixo X')
pyplot.ylabel('Eixo Y')
pyplot.title('Regressão Linear Simples')
pyplot.show()
