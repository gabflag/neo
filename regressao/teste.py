import numpy as np
import statsmodels.api as sm
    

# criando variáveis que serão usadas daqui para frente
# variável preditora = INDICADORES
X = np.array([1,2,3,4,5])

# variável alvo = CRESCIMENTO/DIMINUICAO PAR
y = np.array([3,7,5,11,14])

# é necessário adicionar uma constante a matriz X
X_sm = sm.add_constant(X)

# OLS vem de Ordinary Least Squares e o método fit irá treinar o modelo
results = sm.OLS(y, X_sm).fit()

# mostrando as estatísticas do modelo
print(results.summary())

# mostrando as previsões para o mesmo conjunto passado
print(results.predict(X_sm))


