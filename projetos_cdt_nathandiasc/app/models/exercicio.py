from dataclasses import dataclass


@dataclass
class Exercicio:
    nome: str
    grupo_muscular: str
    descricao: str | None = None
    id: int | None = None