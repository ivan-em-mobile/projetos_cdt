from dataclasses import dataclass
from datetime import date


@dataclass
class Aluno:
    nome: str
    cpf: str
    data_nascimento: date
    email: str
    telefone: str
    data_cadastro: date
    status: str = "ativo"
    id: int | None = None