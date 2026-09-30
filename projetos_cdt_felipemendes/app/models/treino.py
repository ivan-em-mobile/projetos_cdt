from dataclasses import dataclass
from datetime import date


@dataclass
class Treino:
    aluno_id: int
    nome: str
    objetivo: str
    data_criacao: date
    ativo: bool = True
    id: int | None = None