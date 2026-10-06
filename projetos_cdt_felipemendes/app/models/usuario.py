from dataclasses import dataclass


@dataclass
class Usuario:
    usuario: str
    senha_hash: str
    perfil: str = "administrador"
    id: int | None = None