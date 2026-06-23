import tkinter as tk
from tkinter import messagebox
import json
import os

# --- LÓGICA DE DADOS ---
NOME_ARQUIVO = "tarefas_gui.json"

def carregar_dados():
    if os.path.exists(NOME_ARQUIVO):
        try:
            with open(NOME_ARQUIVO, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def salvar_dados(tarefas):
    with open(NOME_ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)

# --- INTERFACE GRÁFICA ---
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tarefas Pro")
        self.root.geometry("400x500")
        self.root.configure(bg="#F0F0F0")

        self.tarefas = carregar_dados()

        # Título
        self.label_titulo = tk.Label(root, text="Minhas Tarefas", font=("Arial", 18, "bold"), bg="#F0F0F0", fg="#333")
        self.label_titulo.pack(pady=10)

        # Entrada de Texto
        self.entrada = tk.Entry(root, font=("Arial", 12), width=30)
        self.entrada.pack(pady=5, padx=10)
        self.entrada.bind('<Return>', lambda event: self.adicionar()) # Adiciona ao apertar Enter

        # Botão Adicionar
        self.btn_add = tk.Button(root, text="ADICIONAR TAREFA", bg="#2ECC71", fg="white", font=("Arial", 10, "bold"), command=self.adicionar)
        self.btn_add.pack(pady=5)

        # Lista de Tarefas (Listbox)
        self.lista_frame = tk.Frame(root)
        self.lista_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.lista_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self.lista_frame, font=("Arial", 12), width=40, height=10, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.listbox.yview)

        # Frame para botões de ação
        self.btn_frame = tk.Frame(root, bg="#F0F0F0")
        self.btn_frame.pack(pady=10)

        self.btn_concluir = tk.Button(self.btn_frame, text="CONCLUIR", bg="#3498DB", fg="white", width=12, command=self.concluir)
        self.btn_concluir.grid(row=0, column=0, padx=5)

        self.btn_remover = tk.Button(self.btn_frame, text="REMOVER", bg="#E74C3C", fg="white", width=12, command=self.remover)
        self.btn_remover.grid(row=0, column=1, padx=5)

        self.atualizar_lista_visual()

    def adicionar(self):
        desc = self.entrada.get().strip()
        if desc:
            self.tarefas.append({"descricao": desc, "concluida": False})
            self.entrada.delete(0, tk.END)
            self.salvar_e_atualizar()
        else:
            messagebox.showwarning("Aviso", "A tarefa não pode estar vazia!")

    def concluir(self):
        try:
            index = self.listbox.curselection()[0]
            self.tarefas[index]["concluida"] = not self.tarefas[index]["concluida"]
            self.salvar_e_atualizar()
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione uma tarefa na lista!")

    def remover(self):
        try:
            index = self.listbox.curselection()[0]
            confirmar = messagebox.askyesno("Confirmar", "Deseja remover esta tarefa?")
            if confirmar:
                del self.tarefas[index]
                self.salvar_e_atualizar()
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para remover!")

    def salvar_e_atualizar(self):
        salvar_dados(self.tarefas)
        self.atualizar_lista_visual()

    def atualizar_lista_visual(self):
        self.listbox.delete(0, tk.END)
        for t in self.tarefas:
            prefixo = "✅ " if t["concluida"] else "⏳ "
            self.listbox.insert(tk.END, f"{prefixo} {t['descricao']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()