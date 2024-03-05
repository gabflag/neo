# https://quantbrasil.com.br/descobrindo-as-tendencias-do-ibovespa-utilizando-o-expoente-de-hurst/

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


"""
    Existem duas formas principais de se calcular o Expoente de Hurst:
        - Rescaled Range (R/S)
        - Detrended Fluctuation Analysis (DFA).
    
    Abaixo irá ser calculado utilizado o método DFA, uma vez que ele não 
    pressupõe que a série temporal seja estacionária.
       
    Se H=0.5H = 0.5H=0.5, então a série é dita aleatória.
    Se H>0.5H > 0.5H>0.5, então a série é dita persistente (em tendência).
    Se H<0.5H < 0.5H<0.5, então a série é dita anti-persistente (em reversão).

    
    hurst: Esta função calcula o Expoente de Hurst de uma série temporal dada. Ele calcula a variação (sigma) de 
    diferenças entre preços em diferentes lags (diferenças de tempo) e, em seguida, ajusta 
    uma linha linear aos valores no espaço log-log.

    series: É a série temporal para a qual você deseja calcular o Expoente de Hurst. 
    No seu código, você está usando a coluna "Close" do DataFrame df.

    H: O valor do Expoente de Hurst calculado usando o método de Hurst.

    c: O coeficiente da linha ajustada no espaço log-log.

    lags e sigmas: São os lags (diferenças de tempo) e os sigmas (desvios padrão) correspondentes, usados para calcular o Expoente de Hurst.

    A função np.polyfit calcula a regressão linear dos logs de lags e sigmas e retorna 
    a tupla (H, c) onde H é o Expoente de Hurst e c é o coeficiente linear da reta.
"""

def hurst(price, min_lag, max_lag):
  lags = np.arange(min_lag, max_lag + 1)
  sigmas = [np.std(np.subtract(price[tau:], price[:-tau])) for tau in lags]
  H, c = np.polyfit(np.log10(lags), np.log10(sigmas), 1)
  return H, c, lags, sigmas


def identificar_tamanho_janela(series):
    max_lags = np.arange(10, 1000 + 1)
    all_hursts = [hurst(series, 2, max_lag)[0] for max_lag in max_lags]

    plt.figure(figsize=(12,6))
    plt.plot(max_lags, all_hursts, marker='o')
    plt.axhline(y=0.52, color='pink', linestyle='--')
    plt.axhline(y=0.50, color='r', linestyle='--')
    plt.axhline(y=0.48, color='pink', linestyle='--')
    plt.xlabel('Max Lags')
    plt.ylabel('Hurst Values')
    plt.title('Hurst Values vs Max Lags')
    plt.show()
    

def main():
    caminho_arquivo = "/home/gabriel/Desktop/Codes/neo/banco_de_dados/candles/commodities/GOLD_200-08-30_2024-03-05_1_D.csv"
    df = pd.read_csv(caminho_arquivo, index_col="Date") 

    df.index = pd.to_datetime(df.index)
    df_2023 = df[df.index.year >= 2024]

    series = df_2023["Close"].values
    # identificar_tamanho_janela(series)
    H, c, lags, sigmas = hurst(series, 2, 30)
    print(f"Hurst GOLD:\t{H:.4f}")


    fig, ax = plt.subplots(2, 1, figsize=(8, 10))
    df_2023["Close"].plot(ax=ax[0], rot=45, xlabel="")
    ax[0].set_title("GOLD")

    ax[1].plot(np.log10(lags), H * np.log10(lags) + c, color="red")
    ax[1].scatter(np.log10(lags), np.log10(sigmas))
    ax[1].set_title(f"GOLD (H = {H:.4f})")
    ax[1].set_xlabel(r"log($\tau$)")
    ax[1].set_ylabel(r"log($\sigma_\tau$)")

    plt.subplots_adjust(hspace=0.4)

    plt.show()

main()