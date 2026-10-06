from dataclasses import dataclass
from datetime import datetime


@dataclass
class Acesso:
    aluno_id: int
    data_hora: datetime
    status: str
    motivo: str | None = None
    id: int | None = None