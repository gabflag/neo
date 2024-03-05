import sys
sys.path.append('/home/gabriel/Desktop/Codes/neo')

import pandas as pd
from calculos.regressao import regressao_linear_simples as rs


df = pd.read_csv("/home/gabriel/Desktop/Codes/neo/banco_de_dados/candles/acoes/SP500_total_1_D.csv")
eixo_x='Close'
eixo_y='Volume'
valor_x_avaliado=5000

rs.main(df, eixo_x, eixo_y, valor_x_avaliado, imprimir=True, save_image=True)

