import re
import sqlite3
from datetime import date

from app.database.connection import obter_conexao
from app.models.aluno import Aluno


def _validar_e_formatar_cpf(
    cpf: str,
) -> tuple[str, str]:
    cpf = cpf.strip()

    padrao_sem_mascara = r"\d{11}"
    padrao_com_mascara = (
        r"\d{3}\.\d{3}\.\d{3}-\d{2}"
    )

    formato_valido = (
        re.fullmatch(
            padrao_sem_mascara,
            cpf,
        )
        or re.fullmatch(
            padrao_com_mascara,
            cpf,
        )
    )

    if not formato_valido:
        raise ValueError(
            "CPF inválido. Informe exatamente "
            "11 dígitos no formato "
            "000.000.000-00."
        )

    digitos = re.sub(
        r"\D",
        "",
        cpf,
    )

    cpf_formatado = (
        f"{digitos[:3]}."
        f"{digitos[3:6]}."
        f"{digitos[6:9]}-"
        f"{digitos[9:]}"
    )

    return (
        digitos,
        cpf_formatado,
    )


def cadastrar_aluno(
    aluno: Aluno,
) -> Aluno:
    (
        cpf_digitos,
        cpf_formatado,
    ) = _validar_e_formatar_cpf(
        aluno.cpf
    )

    conexao = obter_conexao()

    try:
        cpf_existente = conexao.execute(
            """
            SELECT id
            FROM alunos
            WHERE
                REPLACE(
                    REPLACE(
                        REPLACE(
                            cpf,
                            '.',
                            ''
                        ),
                        '-',
                        ''
                    ),
                    ' ',
                    ''
                ) = ?
            """,
            (
                cpf_digitos,
            ),
        ).fetchone()

        if cpf_existente is not None:
            raise ValueError(
                "Não foi possível cadastrar "
                "o aluno. "
                "Este CPF já está cadastrado."
            )

        aluno.cpf = cpf_formatado

        cursor = conexao.execute(
            """
            INSERT INTO alunos (
                nome,
                cpf,
                data_nascimento,
                email,
                telefone,
                data_cadastro,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                aluno.nome,
                aluno.cpf,
                aluno.data_nascimento.isoformat(),
                aluno.email,
                aluno.telefone,
                aluno.data_cadastro.isoformat(),
                aluno.status,
            ),
        )

        conexao.commit()

        aluno.id = cursor.lastrowid

        return aluno

    except sqlite3.IntegrityError as erro:
        raise ValueError(
            "Não foi possível cadastrar o aluno. "
            "Verifique se CPF ou e-mail "
            "já estão cadastrados."
        ) from erro

    finally:
        conexao.close()


def listar_alunos() -> list[Aluno]:
    conexao = obter_conexao()

    try:
        linhas = conexao.execute(
            """
            SELECT
                id,
                nome,
                cpf,
                data_nascimento,
                email,
                telefone,
                data_cadastro,
                status
            FROM alunos
            ORDER BY nome
            """
        ).fetchall()

        return [
            _linha_para_aluno(
                linha
            )
            for linha in linhas
        ]

    finally:
        conexao.close()


def buscar_aluno_por_id(
    aluno_id: int,
) -> Aluno | None:
    conexao = obter_conexao()

    try:
        linha = conexao.execute(
            """
            SELECT
                id,
                nome,
                cpf,
                data_nascimento,
                email,
                telefone,
                data_cadastro,
                status
            FROM alunos
            WHERE id = ?
            """,
            (
                aluno_id,
            ),
        ).fetchone()

        if linha is None:
            return None

        return _linha_para_aluno(
            linha
        )

    finally:
        conexao.close()


def buscar_aluno_por_cpf(
    cpf: str,
) -> Aluno | None:
    try:
        (
            cpf_digitos,
            _,
        ) = _validar_e_formatar_cpf(
            cpf
        )

    except ValueError:
        return None

    conexao = obter_conexao()

    try:
        linha = conexao.execute(
            """
            SELECT
                id,
                nome,
                cpf,
                data_nascimento,
                email,
                telefone,
                data_cadastro,
                status
            FROM alunos
            WHERE
                REPLACE(
                    REPLACE(
                        REPLACE(
                            cpf,
                            '.',
                            ''
                        ),
                        '-',
                        ''
                    ),
                    ' ',
                    ''
                ) = ?
            """,
            (
                cpf_digitos,
            ),
        ).fetchone()

        if linha is None:
            return None

        return _linha_para_aluno(
            linha
        )

    finally:
        conexao.close()


def _linha_para_aluno(
    linha,
) -> Aluno:
    cpf = linha["cpf"]

    try:
        (
            _,
            cpf_formatado,
        ) = _validar_e_formatar_cpf(
            cpf
        )

    except ValueError:
        cpf_formatado = cpf

    return Aluno(
        id=linha["id"],
        nome=linha["nome"],
        cpf=cpf_formatado,
        data_nascimento=date.fromisoformat(
            linha["data_nascimento"]
        ),
        email=linha["email"],
        telefone=linha["telefone"],
        data_cadastro=date.fromisoformat(
            linha["data_cadastro"]
        ),
        status=linha["status"],
    )