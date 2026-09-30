import hashlib

from app.database.connection import obter_conexao
from app.models.usuario import Usuario


USUARIO_ROOT = "root master"
SENHA_ROOT = "root"


def gerar_hash_senha(senha: str) -> str:
    return hashlib.sha256(
        senha.encode("utf-8")
    ).hexdigest()


def buscar_usuario_por_nome(
    nome_usuario: str,
) -> Usuario | None:
    conexao = obter_conexao()

    try:
        linha = conexao.execute(
            """
            SELECT
                id,
                usuario,
                senha_hash,
                perfil
            FROM usuarios
            WHERE usuario = ?
            """,
            (nome_usuario,),
        ).fetchone()

        if linha is None:
            return None

        return Usuario(
            id=linha["id"],
            usuario=linha["usuario"],
            senha_hash=linha["senha_hash"],
            perfil=linha["perfil"],
        )

    finally:
        conexao.close()


def criar_usuario_root():
    usuario_existente = buscar_usuario_por_nome(
        USUARIO_ROOT
    )

    if usuario_existente is not None:
        return usuario_existente

    usuario = Usuario(
        usuario=USUARIO_ROOT,
        senha_hash=gerar_hash_senha(
            SENHA_ROOT
        ),
        perfil="administrador",
    )

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            INSERT INTO usuarios (
                usuario,
                senha_hash,
                perfil
            )
            VALUES (?, ?, ?)
            """,
            (
                usuario.usuario,
                usuario.senha_hash,
                usuario.perfil,
            ),
        )

        conexao.commit()

        usuario.id = cursor.lastrowid

        return usuario

    finally:
        conexao.close()


def autenticar_usuario(
    nome_usuario: str,
    senha: str,
) -> Usuario | None:
    usuario = buscar_usuario_por_nome(
        nome_usuario
    )

    if usuario is None:
        return None

    senha_hash = gerar_hash_senha(
        senha
    )

    if senha_hash != usuario.senha_hash:
        return None

    return usuario