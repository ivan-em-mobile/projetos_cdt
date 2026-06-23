import sqlite3
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk


def conectar():
    return sqlite3.connect("concessionaria.db")


def cadastrar_carro():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO carros (modelo, marca, ano, preco, status) VALUES (?, ?, ?, ?, ?)",
                   (entry_modelo.get(), entry_marca.get(), int(entry_ano.get()), float(entry_preco.get()), entry_status.get()))
    conn.commit()
    conn.close()
    atualizar_listagens()
    messagebox.showinfo("Sucesso", "Carro cadastrado!")

def cadastrar_cliente():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)",
                   (entry_nome.get(), entry_telefone.get(), entry_email.get()))
    conn.commit()
    conn.close()
    atualizar_listagens()
    messagebox.showinfo("Sucesso", "Cliente cadastrado!")

def registrar_venda():
    conn = conectar()
    cursor = conn.cursor()
    data = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO vendas (id_cliente, id_carro, data_venda, valor) VALUES (?, ?, ?, ?)",
                   (int(entry_cliente_id.get()), int(entry_carro_id.get()), data, float(entry_valor.get())))
    conn.commit()
    conn.close()
    atualizar_listagens()
    messagebox.showinfo("Sucesso", "Venda registrada!")

def exportar_json():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM carros")
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

    messagebox.showinfo("Exportação", "Dados exportados para dados_concessionaria.json")


def atualizar_listagens():
    for item in tree_carros.get_children():
        tree_carros.delete(item)
    for item in tree_clientes.get_children():
        tree_clientes.delete(item)
    for item in tree_vendas.get_children():
        tree_vendas.delete(item)

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM carros")
    for c in cursor.fetchall():
        tree_carros.insert("", "end", values=c)

    cursor.execute("SELECT * FROM clientes")
    for cl in cursor.fetchall():
        tree_clientes.insert("", "end", values=cl)

    cursor.execute("SELECT * FROM vendas")
    for v in cursor.fetchall():
        tree_vendas.insert("", "end", values=v)

    conn.close()


root = tk.Tk()
root.title("Concessionária")
root.configure(bg="#004d6e") 


style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview", background="#00b1cd", foreground="black", rowheight=25, fieldbackground="#0081ab")
style.map("Treeview", background=[("selected", "#0081ab")])

tk.Label(root, text="Modelo", bg="#004d6e").grid(row=0, column=0)
entry_modelo = tk.Entry(root); entry_modelo.grid(row=0, column=1)

tk.Label(root, text="Marca", bg="#004d6e").grid(row=1, column=0)
entry_marca = tk.Entry(root); entry_marca.grid(row=1, column=1)

tk.Label(root, text="Ano", bg="#004d6e").grid(row=2, column=0)
entry_ano = tk.Entry(root); entry_ano.grid(row=2, column=1)

tk.Label(root, text="Preço", bg="#004d6e").grid(row=3, column=0)
entry_preco = tk.Entry(root); entry_preco.grid(row=3, column=1)

tk.Label(root, text="Status", bg="#004d6e").grid(row=4, column=0)
entry_status = tk.Entry(root); entry_status.grid(row=4, column=1)

tk.Button(root, text="Cadastrar Carro", bg="#0192f3", fg="white", command=cadastrar_carro).grid(row=5, column=0, columnspan=2)


tk.Label(root, text="Nome", bg="#004d6e").grid(row=6, column=0)
entry_nome = tk.Entry(root); entry_nome.grid(row=6, column=1)

tk.Label(root, text="Telefone", bg="#004d6e").grid(row=7, column=0)
entry_telefone = tk.Entry(root); entry_telefone.grid(row=7, column=1)

tk.Label(root, text="Email", bg="#004d6e").grid(row=8, column=0)
entry_email = tk.Entry(root); entry_email.grid(row=8, column=1)

tk.Button(root, text="Cadastrar Cliente", bg="#2196F3", fg="white", command=cadastrar_cliente).grid(row=9, column=0, columnspan=2)


tk.Label(root, text="ID Cliente", bg="#004d6e").grid(row=10, column=0)
entry_cliente_id = tk.Entry(root); entry_cliente_id.grid(row=10, column=1)

tk.Label(root, text="ID Carro", bg="#004d6e").grid(row=11, column=0)
entry_carro_id = tk.Entry(root); entry_carro_id.grid(row=11, column=1)

tk.Label(root, text="Valor", bg="#004d6e").grid(row=12, column=0)
entry_valor = tk.Entry(root); entry_valor.grid(row=12, column=1)

tk.Button(root, text="Registrar Venda", bg="#004d6e", fg="white", command=registrar_venda).grid(row=13, column=0, columnspan=2)


tk.Button(root, text="Exportar JSON", bg="#0084FF", fg="white", command=exportar_json).grid(row=14, column=0, columnspan=2)


tree_carros = ttk.Treeview(root, columns=("ID", "Modelo", "Marca", "Ano", "Preço", "Status"), show="headings")
for col in ("ID", "Modelo", "Marca", "Ano", "Preço", "Status"):
    tree_carros.heading(col, text=col)
tree_carros.grid(row=15, column=0, columnspan=2)

tree_clientes = ttk.Treeview(root, columns=("ID", "Nome", "Telefone", "Email"), show="headings")
for col in ("ID", "Nome", "Telefone", "Email"):
    tree_clientes.heading(col, text=col)
tree_clientes.grid(row=16, column=0, columnspan=2)

tree_vendas = ttk.Treeview(root, columns=("ID", "Cliente_ID", "Carro_ID", "Data_Venda", "Valor"), show="headings")
for col in ("ID", "Cliente_ID", "Carro_ID", "Data_Venda", "Valor"):
    tree_vendas.heading(col, text=col)
tree_vendas.grid(row=17, column=0, columnspan=2)


atualizar_listagens()

root.mainloop()
