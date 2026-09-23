from dataclasses import dataclass
from datetime import date


@dataclass
class Pagamento:
    assinatura_id: int
    valor: float
    data_vencimento: date
    data_pagamento: date | None = None
    status: str = "pendente"
    forma_pagamento: str | None = None
    id: int | None = None