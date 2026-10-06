from app.database.connection import obter_conexao


def criar_tabelas():
    conexao = obter_conexao()

    try:
        conexao.executescript(
            """
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                data_nascimento TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                telefone TEXT NOT NULL,
                data_cadastro TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ativo'
            );

            CREATE TABLE IF NOT EXISTS planos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                valor REAL NOT NULL,
                descricao TEXT,
                ativo INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS assinaturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER NOT NULL,
                plano_id INTEGER NOT NULL,
                data_inicio TEXT NOT NULL,
                data_fim TEXT,
                status TEXT NOT NULL DEFAULT 'ativa',

                FOREIGN KEY (aluno_id)
                    REFERENCES alunos(id),

                FOREIGN KEY (plano_id)
                    REFERENCES planos(id)
            );

            CREATE TABLE IF NOT EXISTS pagamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assinatura_id INTEGER NOT NULL,
                valor REAL NOT NULL,
                data_vencimento TEXT NOT NULL,
                data_pagamento TEXT,
                status TEXT NOT NULL DEFAULT 'pendente',
                forma_pagamento TEXT,

                FOREIGN KEY (assinatura_id)
                    REFERENCES assinaturas(id)
            );

            CREATE TABLE IF NOT EXISTS acessos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER NOT NULL,
                data_hora TEXT NOT NULL,
                status TEXT NOT NULL,
                motivo TEXT,

                FOREIGN KEY (aluno_id)
                    REFERENCES alunos(id)
            );

            CREATE TABLE IF NOT EXISTS treinos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                objetivo TEXT NOT NULL,
                data_criacao TEXT NOT NULL,
                ativo INTEGER NOT NULL DEFAULT 1,

                FOREIGN KEY (aluno_id)
                    REFERENCES alunos(id)
            );

            CREATE TABLE IF NOT EXISTS exercicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                grupo_muscular TEXT NOT NULL,
                descricao TEXT
            );

            CREATE TABLE IF NOT EXISTS treino_exercicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                treino_id INTEGER NOT NULL,
                exercicio_id INTEGER NOT NULL,
                series INTEGER NOT NULL,
                repeticoes TEXT NOT NULL,
                carga REAL,
                descanso_segundos INTEGER,
                ordem INTEGER,

                FOREIGN KEY (treino_id)
                    REFERENCES treinos(id),

                FOREIGN KEY (exercicio_id)
                    REFERENCES exercicios(id)
            );

            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL,
                perfil TEXT NOT NULL DEFAULT 'administrador'
            );

            CREATE UNIQUE INDEX IF NOT EXISTS
                idx_planos_nome_normalizado
            ON planos (
                LOWER(TRIM(nome))
            );
            """
        )

        conexao.commit()

    finally:
        conexao.close()