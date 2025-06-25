# main.py

import tkinter as tk
from tkinter import simpledialog
import numpy as np
from jogo import criar_mapa, gerar_posicao_tesouro
from config import TAMANHO_MAPA, SIMBOLO_JOGADOR
from db import criar_tabela, salvar_pontuacao, listar_pontuacoes

# Dados do jogo
mapa = criar_mapa()
posicao_jogador = [0, 0]
tesouro = gerar_posicao_tesouro()
pontuacao = 0

# Cria janela
janela = tk.Tk()
janela.title("Caça ao Tesouro")

# Grade do mapa (labels visuais)
botoes = []

def atualizar_mapa():
    for i in range(TAMANHO_MAPA):
        for j in range(TAMANHO_MAPA):
            texto = ""
            if [i, j] == posicao_jogador:
                texto = SIMBOLO_JOGADOR
            else:
                texto = "🟦"
            botoes[i][j]["text"] = texto
    pontuacao_label.config(text=f"Pontuação: {pontuacao}")

def mover(direcao):
    global pontuacao
    linha, coluna = posicao_jogador

    movimentos = {
        "cima": (-1, 0),
        "baixo": (1, 0),
        "esquerda": (0, -1),
        "direita": (0, 1)
    }

    dx, dy = movimentos[direcao]
    nova_linha, nova_coluna = linha + dx, coluna + dy

    if 0 <= nova_linha < TAMANHO_MAPA and 0 <= nova_coluna < TAMANHO_MAPA:
        posicao_jogador[0], posicao_jogador[1] = nova_linha, nova_coluna
        pontuacao += 1
        atualizar_mapa()

        if (nova_linha, nova_coluna) == tesouro:
            botoes[nova_linha][nova_coluna]["text"] = "🪙"
            
            # Pergunta nome e salva pontuação
            nome = simpledialog.askstring("Parabéns!", "Você encontrou o tesouro!\nQual seu nome?")
            if nome:
                salvar_pontuacao(nome, pontuacao)
                msg = f"🎉 {nome}, pontuação salva!"
            else:
                msg = "Pontuação não salva (sem nome)."
            
            resultado = tk.Label(janela, text=msg, font=("Arial", 14), fg="green")
            resultado.grid(row=TAMANHO_MAPA+2, column=0, columnspan=5)

            # Desativa botões de movimento
            for btn in botoes_movimento:
                btn.config(state="disabled")

def mostrar_ranking():
    top = tk.Toplevel(janela)
    top.title("Ranking")
    tk.Label(top, text="🏆 Melhores Pontuações", font=("Arial", 14)).pack(pady=5)

    ranking = listar_pontuacoes()
    if ranking:
        for nome, pont, data in ranking:
            tk.Label(top, text=f"{nome} - {pont} pontos ({data[:10]})").pack()
    else:
        tk.Label(top, text="Nenhuma pontuação registrada ainda.").pack()

# Criar grid do mapa
for i in range(TAMANHO_MAPA):
    linha_botoes = []
    for j in range(TAMANHO_MAPA):
        btn = tk.Label(janela, text="🟦", width=4, height=2, font=("Arial", 14), borderwidth=2, relief="ridge")
        btn.grid(row=i, column=j)
        linha_botoes.append(btn)
    botoes.append(linha_botoes)

# Label da pontuação
pontuacao_label = tk.Label(janela, text="Pontuação: 0", font=("Arial", 12))
pontuacao_label.grid(row=TAMANHO_MAPA, column=0, columnspan=5)

# Botões de movimento
frame_controles = tk.Frame(janela)
frame_controles.grid(row=TAMANHO_MAPA + 1, column=0, columnspan=5, pady=5)

botoes_movimento = [
    tk.Button(frame_controles, text="↑", command=lambda: mover("cima")),
    tk.Button(frame_controles, text="←", command=lambda: mover("esquerda")),
    tk.Button(frame_controles, text="→", command=lambda: mover("direita")),
    tk.Button(frame_controles, text="↓", command=lambda: mover("baixo")),
]

botoes_movimento[0].grid(row=0, column=1)
botoes_movimento[1].grid(row=1, column=0)
botoes_movimento[2].grid(row=1, column=2)
botoes_movimento[3].grid(row=2, column=1)

# Botão de ranking
btn_ranking = tk.Button(janela, text="Ver Ranking", command=mostrar_ranking)
btn_ranking.grid(row=TAMANHO_MAPA+3, column=0, columnspan=5, pady=5)

# Inicia mapa
criar_tabela()
atualizar_mapa()
janela.mainloop()
