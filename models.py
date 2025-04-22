from pydantic import BaseModel
from typing import Optional
from datetime import date

class ContaBancaria(BaseModel):
    saldo: float
    tipo_chave_pix: str
    chave_pix: str
    nome_titular: str
    data_nascimento: date
    numero_agencia: str
    numero_conta: str
    numero_banco: str
    instituicao_bancaria: str
    cpf: str


class Transacao(BaseModel):
    id_conta: int
    tipo_operacao: str
    valor: float
    data_operacao: date
    descricao: str
    tipo_transacao: str
    status_transacao: str
    id_conta_origem: Optional[int]
    id_conta_destino: Optional[int]   


class TransacaoCreate(BaseModel):
    id_conta_origem: int
    id_conta_destino: int
    valor: float
    descricao: str
    tipo_operacao: Optional[str] = "transferencia"
    tipo_transacao: Optional[str] = "PIX"     

""" A classe TransacaoCreate não precisa estar no banco de dados.
Ela é somente um modelo Pydantic usado para receber os dados da requisição HTTP (ex: POST /transacoes) na sua API FastAPI. """    