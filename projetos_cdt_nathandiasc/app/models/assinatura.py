from dataclasses import dataclass
from datetime import date


@dataclass
class Assinatura:
    aluno_id: int
    plano_id: int
    data_inicio: date
    data_fim: date | None = None
    status: str = "ativa"
    id: int | None = None