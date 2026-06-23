import sqlite3


def conectar():
    return sqlite3.connect("cafeteria.db")


def criar_tabelas():

    conn = conectar()
    cursor = conn.cursor()

    # ---------------- USUÁRIOS ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        senha TEXT
    )
    """)

    # ---------------- PRODUTOS ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        preco REAL,
        categoria TEXT,
        imagem TEXT,
        estoque INTEGER DEFAULT 0
    )
    """)

    # ---------------- PEDIDOS ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        endereco TEXT,
        observacao TEXT,
        produto TEXT,
        preco REAL,
        status TEXT DEFAULT 'Recebido'
    )
    """)

    # ---------------- ADMIN PADRÃO ----------------
    cursor.execute("""
    SELECT * FROM usuarios
    WHERE usuario = 'admin'
    """)

    if not cursor.fetchone():

        cursor.execute("""
        INSERT INTO usuarios (usuario, senha)
        VALUES (?, ?)
        """, ("admin", "123"))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    criar_tabelas()
    print("Banco criado com sucesso!")