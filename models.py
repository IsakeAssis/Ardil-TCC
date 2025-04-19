from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContaBancaria(BaseModel):
    id_conta: Optional[int]
    saldo: float
    tipo_chave_pix: str
    chave_pix: str
    nome_titular: str
    data_nascimento: str
    numero_agencia: str
    numero_conta: str
    numero_banco: str
    instituicao_bancaria: str
    cpf: str


class Transacao(BaseModel):
    id_conta: int
    tipo_operacao: str
    valor: float
    data_operacao: datetime
    descricao: str
    tipo_transacao: str
    status_transacao: str
    id_conta_origem: Optional[int]
    id_conta_destino: Optional[int]    