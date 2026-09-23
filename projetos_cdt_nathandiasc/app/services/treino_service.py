from datetime import date

from app.database.connection import obter_conexao
from app.models.treino import Treino

from app.services.aluno_service import buscar_aluno_por_id
from app.services.exercicio_service import buscar_exercicio_por_id


def cadastrar_treino(treino: Treino) -> Treino:
    aluno = buscar_aluno_por_id(treino.aluno_id)

    if aluno is None:
        raise ValueError("Aluno não encontrado.")

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            INSERT INTO treinos (
                aluno_id,
                nome,
                objetivo,
                data_criacao,
                ativo
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                treino.aluno_id,
                treino.nome,
                treino.objetivo,
                treino.data_criacao.isoformat(),
                int(treino.ativo),
            ),
        )

        conexao.commit()

        treino.id = cursor.lastrowid

        return treino

    finally:
        conexao.close()


def buscar_treino_por_id(
    treino_id: int,
) -> Treino | None:
    conexao = obter_conexao()

    try:
        linha = conexao.execute(
            """
            SELECT
                id,
                aluno_id,
                nome,
                objetivo,
                data_criacao,
                ativo
            FROM treinos
            WHERE id = ?
            """,
            (treino_id,),
        ).fetchone()

        if linha is None:
            return None

        return _linha_para_treino(linha)

    finally:
        conexao.close()


def listar_treinos_por_aluno(
    aluno_id: int,
) -> list[Treino]:
    conexao = obter_conexao()

    try:
        linhas = conexao.execute(
            """
            SELECT
                id,
                aluno_id,
                nome,
                objetivo,
                data_criacao,
                ativo
            FROM treinos
            WHERE aluno_id = ?
            ORDER BY data_criacao DESC, id DESC
            """,
            (aluno_id,),
        ).fetchall()

        return [
            _linha_para_treino(linha)
            for linha in linhas
        ]

    finally:
        conexao.close()


def adicionar_exercicio_ao_treino(
    treino_id: int,
    exercicio_id: int,
    series: int,
    repeticoes: str,
    carga: float | None = None,
    descanso_segundos: int | None = None,
    ordem: int | None = None,
):
    treino = buscar_treino_por_id(treino_id)

    if treino is None:
        raise ValueError("Treino não encontrado.")

    exercicio = buscar_exercicio_por_id(
        exercicio_id
    )

    if exercicio is None:
        raise ValueError("Exercício não encontrado.")

    if series <= 0:
        raise ValueError(
            "O número de séries deve ser maior que zero."
        )

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            INSERT INTO treino_exercicios (
                treino_id,
                exercicio_id,
                series,
                repeticoes,
                carga,
                descanso_segundos,
                ordem
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                treino_id,
                exercicio_id,
                series,
                repeticoes,
                carga,
                descanso_segundos,
                ordem,
            ),
        )

        conexao.commit()

        return cursor.lastrowid

    finally:
        conexao.close()


def listar_exercicios_do_treino(
    treino_id: int,
) -> list[dict]:
    conexao = obter_conexao()

    try:
        linhas = conexao.execute(
            """
            SELECT
                treino_exercicios.id,
                treino_exercicios.exercicio_id,
                exercicios.nome,
                exercicios.grupo_muscular,
                treino_exercicios.series,
                treino_exercicios.repeticoes,
                treino_exercicios.carga,
                treino_exercicios.descanso_segundos,
                treino_exercicios.ordem
            FROM treino_exercicios

            INNER JOIN exercicios
                ON exercicios.id =
                   treino_exercicios.exercicio_id

            WHERE treino_exercicios.treino_id = ?

            ORDER BY
                treino_exercicios.ordem,
                treino_exercicios.id
            """,
            (treino_id,),
        ).fetchall()

        return [
            {
                "id": linha["id"],
                "exercicio_id": linha["exercicio_id"],
                "nome": linha["nome"],
                "grupo_muscular": linha["grupo_muscular"],
                "series": linha["series"],
                "repeticoes": linha["repeticoes"],
                "carga": linha["carga"],
                "descanso_segundos": linha[
                    "descanso_segundos"
                ],
                "ordem": linha["ordem"],
            }
            for linha in linhas
        ]

    finally:
        conexao.close()


def _linha_para_treino(linha) -> Treino:
    return Treino(
        id=linha["id"],
        aluno_id=linha["aluno_id"],
        nome=linha["nome"],
        objetivo=linha["objetivo"],
        data_criacao=date.fromisoformat(
            linha["data_criacao"]
        ),
        ativo=bool(linha["ativo"]),
    )