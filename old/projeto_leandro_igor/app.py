from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import json
import webbrowser

app = Flask(__name__)

# ==========================================
# BANCO DE DADOS
# ==========================================

def conectar():
    return sqlite3.connect("central_tenis.db")

conexao = conectar()
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    usuario TEXT UNIQUE,
    senha TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    produto TEXT,
    preco REAL
)
""")

conexao.commit()
conexao.close()

# ==========================================
# ESTOQUE
# ==========================================

estoque = [
    {"marca": "Nike", "modelo": "Air Max 90", "preco": 799.90},
    {"marca": "Nike", "modelo": "Jordan 1", "preco": 999.90},
    {"marca": "Puma", "modelo": "Ultraboost", "preco": 699.90},
    {"marca": "Puma", "modelo": "RS-X", "preco": 450.00},
    {"marca": "Vans", "modelo": "Old Skool", "preco": 399.90},
    {"marca": "New Balance", "modelo": "9060", "preco": 950.00},
    {"marca": "Asics", "modelo": "Gel Kayano", "preco": 850.00},
    {"marca": "Converse", "modelo": "Chuck Taylor", "preco": 320.00},
    {"marca": "Jordan", "modelo": "Jordan 4 Retro", "preco": 1799.90},
]

# ==========================================
# HOME
# ==========================================

@app.route("/")
def inicio():
    return render_template("index.html", estoque=estoque)

# ==========================================
# CADASTRAR USUÁRIO
# ==========================================

@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    nome = request.form["nome"]
    email = request.form["email"]
    usuario = request.form["usuario"]
    senha = request.form["senha"]

    if nome == "" or email == "" or usuario == "" or senha == "":
        return "Preencha todos os campos!"

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute("""
        INSERT INTO usuarios (nome, email, usuario, senha)
        VALUES (?, ?, ?, ?)
        """, (nome, email, usuario, senha))

        conexao.commit()

    except:
        conexao.close()
        return "Usuário já existe!"

    conexao.close()

    return redirect("/")

# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["POST"])
def login():

    usuario = request.form["usuario"]
    senha = request.form["senha"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT * FROM usuarios
    WHERE usuario = ? AND senha = ?
    """, (usuario, senha))

    resultado = cursor.fetchone()

    conexao.close()

    if resultado:
        return f"Login realizado! Bem-vindo {resultado[1]}"
    else:
        return "Usuário ou senha incorretos!"

# ==========================================
# EXPORTAR JSON
# ==========================================

@app.route("/exportar")
def exportar():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    cursor.execute("SELECT * FROM pedidos")
    pedidos = cursor.fetchall()

    lista_usuarios = []

    for u in usuarios:
        lista_usuarios.append({
            "id": u[0],
            "nome": u[1],
            "email": u[2],
            "usuario": u[3],
            "senha": u[4]
        })

    lista_pedidos = []

    for p in pedidos:
        lista_pedidos.append({
            "id": p[0],
            "usuario": p[1],
            "produto": p[2],
            "preco": p[3]
        })