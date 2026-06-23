import sqlite3
import json
from datetime import datetime


conn = sqlite3.connect("concessionaria.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS carros(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modelo TEXT NOT NULL,
    marca TEXT NOT NULL,
    ano INTEGER NOT NULL,
    preco REAL NOT NULL,
    status TEXT DEFAULT 'disponível'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vendas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_carro INTEGER NOT NULL,
    data_venda TEXT NOT NULL,
    valor REAL NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_carro) REFERENCES carros(id)
)
""")


carros_exemplo = [
    ("Civic", "Honda", 2022, 120000, "disponível"),
    ("Corolla", "Toyota", 2023, 130000, "disponível"),
    ("Onix", "Chevrolet", 2021, 75000, "vendido")
]
cursor.executemany("INSERT INTO carros (modelo, marca, ano, preco, status) VALUES (?, ?, ?, ?, ?)", carros_exemplo)

clientes_exemplo = [
    ("João Silva", "11999999999", "joao@email.com"),
    ("Maria Souza", "11888888888", "maria@email.com")
]
cursor.executemany("INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)", clientes_exemplo)


cursor.execute("INSERT INTO vendas (id_cliente, id_carro, data_venda, valor) VALUES (?, ?, ?, ?)",
               (1, 1, datetime.now().strftime("%Y-%m-%d"), 118000))

conn.commit()


cursor.execute("SELECT * FROM carros WHERE status='disponível'")
carros = cursor.fetchall()

cursor.execute("SELECT * FROM clientes")
clientes = cursor.fetchall()

cursor.execute("SELECT * FROM vendas")
vendas = cursor.fetchall()

conn.close()

dados = {
    "carros": [
        {"id": c[0], "modelo": c[1], "marca": c[2], "ano": c[3], "preco": c[4], "status": c[5]}
        for c in carros
    ],
    "clientes": [
        {"id": cl[0], "nome": cl[1], "telefone": cl[2], "email": cl[3]}
        for cl in clientes
    ],
    "vendas": [
        {"id": v[0], "cliente_id": v[1], "carro_id": v[2], "data_venda": v[3], "valor": v[4]}
        for v in vendas
    ]
}

with open("dados_concessionaria.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, indent=4, ensure_ascii=False)

print("Dados exportados para dados_concessionaria.json")