# Antes de rodar qualquer coisa da aplicação:
# 1. Ative o ambiente virtual: .\venv\Scripts\activate
# 2. Execute o servidor com: python -m uvicorn main:app --reload

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from database import get_connection
from models import ContaBancaria, Transacao, TransacaoCreate
import psycopg2
import psycopg2.extras

app = FastAPI()

# Habilitar CORS para permitir requisições do front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, troque pelo domínio do seu site
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Rota GET /contas
@app.get("/contas")
def listar_contas():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM contas_bancarias")
    contas = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(c) for c in contas]

# 🔹 Rota POST /contas
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

# 🔹 Rota GET /transacoes/{id_conta}
@app.get("/transacoes/{id_conta}")
def ver_transacoes(id_conta: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM historico_transacoes WHERE id_conta = %s", (id_conta,))
    transacoes = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(t) for t in transacoes]

# 🔹 Rota POST /transacoes
@app.post("/transacoes")
async def realizar_transacao(transacao: TransacaoCreate, request: Request):
    body = await request.body()
    print("Body bruto:", body)
def realizar_transacao(transacao: TransacaoCreate):
    print("O front ta chamando a função de transações ?")#Revendo os testes Piranha 
    print("Recebido:", transacao)
    conn = get_connection()
    try:
        cur = conn.cursor()

        # Verificar conta origem
        cur.execute("SELECT saldo FROM contas_bancarias WHERE id_conta = %s", (transacao.id_conta_origem,))
        origem = cur.fetchone()
        if not origem:
            raise HTTPException(status_code=404, detail="Conta de origem não encontrada")
        if origem[0] < transacao.valor:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")

        # Verificar conta destino
        cur.execute("SELECT saldo FROM contas_bancarias WHERE id_conta = %s", (transacao.id_conta_destino,))
        destino = cur.fetchone()
        if not destino:
            raise HTTPException(status_code=404, detail="Conta de destino não encontrada")

        # Atualizar saldos
        cur.execute("UPDATE contas_bancarias SET saldo = saldo - %s WHERE id_conta = %s",
                    (transacao.valor, transacao.id_conta_origem))
        cur.execute("UPDATE contas_bancarias SET saldo = saldo + %s WHERE id_conta = %s",
                    (transacao.valor, transacao.id_conta_destino))

        # Inserir histórico
        cur.execute("""
            INSERT INTO historico_transacoes
            (id_conta, tipo_operacao, valor, data_operacao, descricao, tipo_transacao, status_transacao, id_conta_origem, id_conta_destino)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            transacao.id_conta_origem,
            transacao.tipo_operacao,
            transacao.valor,
            datetime.now(),
            transacao.descricao,
            transacao.tipo_transacao,
            'concluida',
            transacao.id_conta_origem,
            transacao.id_conta_destino
        ))

        conn.commit()
        cur.close()
        return {"mensagem": "Transação realizada com sucesso."}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
