import sqlite3


def conectar():
    return sqlite3.connect("cafeteria.db")


# =========================
# PRODUTOS
# =========================

def get_produtos(categoria=None):
    conn = conectar()
    cursor = conn.cursor()

    if categoria:
        cursor.execute(
            "SELECT * FROM produtos WHERE categoria=?",
            (categoria,)
        )
    else:
        cursor.execute("SELECT * FROM produtos")

    dados = cursor.fetchall()

    conn.close()

    return dados


def atualizar_estoque(nome, quantidade):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE produtos SET estoque = ? WHERE nome = ?",
        (quantidade, nome)
    )

    conn.commit()
    conn.close()


# =========================
# PEDIDOS
# =========================

def salvar_pedido(cliente, endereco, observacao, produto, preco):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pedidos
        (cliente, endereco, observacao, produto, preco)

        VALUES (?, ?, ?, ?, ?)
    """, (cliente, endereco, observacao, produto, preco))

    conn.commit()
    conn.close()


def get_pedidos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pedidos")

    dados = cursor.fetchall()

    conn.close()

    return dados


def excluir_pedido(id_pedido):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM pedidos WHERE id = ?",
        (id_pedido,)
    )

    conn.commit()
    conn.close()


# =========================
# LOGIN
# =========================

def verificar_login(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=? AND senha=?",
        (usuario, senha)
    )

    user = cursor.fetchone()

    conn.close()

    return user


# =========================
# FATURAMENTO
# =========================

def calcular_faturamento():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(preco) FROM pedidos"
    )

    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        return 0

    return total


# =========================
# ESTOQUE AUTOMÁTICO
# =========================

def adicionar_coluna_estoque():
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "ALTER TABLE produtos ADD COLUMN estoque INTEGER DEFAULT 0"
        )

        conn.commit()

    except:
        pass

    conn.close()

def verificar_estoque(nome):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT estoque FROM produtos WHERE nome = ?",
        (nome,)
    )

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado[0]

    return 0


def atualizar_status(id_pedido, status):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE pedidos
    SET status = ?
    WHERE id = ?
    """, (status, id_pedido))

    conn.commit()
    conn.close()


def diminuir_estoque(nome):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE produtos
        SET estoque = estoque - 1
        WHERE nome = ? AND estoque > 0
        """,
        (nome,)
    )

    conn.commit()
    conn.close()

adicionar_coluna_estoque()