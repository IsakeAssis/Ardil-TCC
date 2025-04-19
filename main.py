# Antes de rodar qualquer coisa da aplicação:
# 1. Ative o ambiente virtual: .\venv\Scripts\activate
# 2. Execute o servidor com: python -m uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection
from models import ContaBancaria, Transacao
import psycopg2.extras

app = FastAPI()

# Habilitar CORS para permitir requisições do front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, substitua por ["http://seusite.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""Listar contas bancárias"""
@app.get("/contas")
def listar_contas():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM contas_bancarias")
    contas = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(c) for c in contas]

@app.post("/contas")
def criar_conta(conta: ContaBancaria):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO contas_bancarias (saldo, tipo_chave_pix, chave_pix, nome_titular, data_nascimento,
            numero_agencia, numero_conta, numero_banco, instituicao_bancaria, cpf)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        conta.saldo, conta.tipo_chave_pix, conta.chave_pix, conta.nome_titular, conta.data_nascimento,
        conta.numero_agencia, conta.numero_conta, conta.numero_banco, conta.instituicao_bancaria, conta.cpf
    ))
    conn.commit()
    cur.close()
    conn.close()
    return {"mensagem": "Conta criada com sucesso"}

@app.get("/transacoes/{id_conta}")
def ver_transacoes(id_conta: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM historico_transacoes WHERE id_conta = %s", (id_conta,))
    transacoes = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(t) for t in transacoes]

@app.post("/transacoes")
def registrar_transacao(transacao: Transacao):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO historico_transacoes (id_conta, tipo_operacao, valor, data_operacao, descricao, 
            tipo_transacao, status_transacao, id_conta_origem, id_conta_destino)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        transacao.id_conta, transacao.tipo_operacao, transacao.valor, transacao.data_operacao, transacao.descricao,
        transacao.tipo_transacao, transacao.status_transacao, transacao.id_conta_origem, transacao.id_conta_destino
    ))
    conn.commit()
    cur.close()
    conn.close()
    return {"mensagem": "Transação registrada"}
