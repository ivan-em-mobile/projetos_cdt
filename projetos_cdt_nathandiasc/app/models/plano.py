from dataclasses import dataclass


@dataclass
class Plano:
    nome: str
    valor: float
    descricao: str
    ativo: bool = True
    id: int | None = None