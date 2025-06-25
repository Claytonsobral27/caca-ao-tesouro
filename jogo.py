# jogo.py

import numpy as np
from config import TAMANHO_MAPA

def criar_mapa():
    return np.random.randint(1, 10, size=(TAMANHO_MAPA, TAMANHO_MAPA))

def gerar_posicao_tesouro():
    while True:
        linha, coluna = np.random.randint(0, TAMANHO_MAPA, size=2)
        if (linha, coluna) != (0, 0):
            return (linha, coluna)
