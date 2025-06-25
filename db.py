# bd.py

import sqlite3

# Conecta ao banco (ou cria se não existir)
def conectar():
    return sqlite3.connect("pontuacoes.db")

# Cria a tabela se ainda não existir
def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pontuacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            pontuacao INTEGER,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Salva a pontuação do jogador
def salvar_pontuacao(nome, pontuacao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pontuacoes (nome, pontuacao) VALUES (?, ?)", (nome, pontuacao))
    conn.commit()
    conn.close()

# Lista as últimas pontuações (por padrão, 5 melhores)
def listar_pontuacoes(limit=5):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, pontuacao, data FROM pontuacoes ORDER BY pontuacao ASC LIMIT ?", (limit,))
    dados = cursor.fetchall()
    conn.close()
    return dados
