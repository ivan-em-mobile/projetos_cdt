import os
import re
import json
import sqlite3
import time
import threading
from datetime import datetime
import pandas as pd

import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# ==========================================
# 1. BANCO DE DADOS (SQLite)
# ==========================================
DB_NAME = "historico.db"

def init_db():
    """Cria a estrutura inicial de tabelas no banco de dados SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tabela para guardar os termos pesquisados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS buscas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            termo TEXT NOT NULL,
            data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela para guardar os produtos vinculados a cada busca
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            busca_id INTEGER,
            titulo TEXT,
            preco REAL,
            link TEXT,
            FOREIGN KEY (busca_id) REFERENCES buscas (id)
        )
    """)

    # Tabela de utilizadores administradores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    
    # Inserção do utilizador padrão caso a tabela esteja vazia
    cursor.execute("SELECT COUNT(*) FROM admin")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO admin (usuario, senha) VALUES (?, ?)",
            ("root master", "root")
        )

    conn.commit()
    conn.close()

def verificar_login_admin(usuario: str, senha: str) -> bool:
    """Valida o utilizador e senha na tabela admin."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM admin WHERE usuario = ? AND senha = ?",
        (usuario, senha)
    )
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado > 0

def salvar_no_banco(termo: str, lista_produtos: list):
    """Grava a busca e a lista de produtos retornados no banco SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    data_formatada = datetime.now().strftime("%d/%m/%Y %H:%M")
    cursor.execute("INSERT INTO buscas (termo, data_hora) VALUES (?, ?)", (termo, data_formatada))
    busca_id = cursor.lastrowid

    for item in lista_produtos:
        cursor.execute(
            "INSERT INTO produtos (busca_id, titulo, preco, link) VALUES (?, ?, ?, ?)",
            (busca_id, item["titulo"], item["preco"], item["link"])
        )

    conn.commit()
    conn.close()

def obter_historico_completo():
    """Consulta todos os produtos pesquisados no banco de dados."""
    conn = sqlite3.connect(DB_NAME)
    query = """
        SELECT b.data_hora, b.termo, p.titulo, p.preco, p.link
        FROM produtos p
        JOIN buscas b ON p.busca_id = b.id
        ORDER BY p.id DESC
    """
    cursor = conn.cursor()
    cursor.execute(query)
    registros = cursor.fetchall()
    conn.close()
    return registros

def obter_df_historico():
    """Retorna um DataFrame do Pandas com o histórico formatado para exportação."""
    conn = sqlite3.connect(DB_NAME)
    query = """
        SELECT b.data_hora AS 'Data/Hora', b.termo AS 'Termo Pesquisado',
               p.titulo AS 'Produto', p.preco AS 'Preço (R$)', p.link AS 'Link'
        FROM produtos p
        JOIN buscas b ON p.busca_id = b.id
        ORDER BY p.id DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ==========================================
# 2. AUTOMAÇÃO WEB (Selenium)
# ==========================================
def executar_scraping(termo: str, limite: int = 10, callback_status=None):
    """Executa a navegação automatizada no Mercado Livre e extrai os produtos."""
    if callback_status:
        callback_status("Iniciando Chrome...")

    options = Options()
    options.add_argument("--window-size=1280,800")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)
    produtos_coletados = []

    try:
        if callback_status:
            callback_status(f"Acessando Mercado Livre para '{termo}'...")

        termo_url = termo.replace(" ", "-").lower()
        driver.get(f"https://lista.mercadolivre.com.br/{termo_url}")
        time.sleep(3)

        cards = []
        tentativas = 0
        max_tentativas = 12

        # Rolagem da página para carregar elementos dinâmicos
        while len(cards) < limite and tentativas < max_tentativas:
            driver.execute_script("window.scrollBy(0, 1200);")
            time.sleep(1.2)
            cards = driver.find_elements(
                By.CSS_SELECTOR,
                "li.ui-search-layout__item, div.poly-card, div.ui-search-result__content, .ui-search-result"
            )
            tentativas += 1

        if callback_status:
            callback_status(f"Lendo {len(cards)} itens e extraindo preços...")

        for card in cards[:limite]:
            try:
                # 1. Extração do Título
                titulo = ""
                for sel in [".poly-component__title", ".ui-search-item__title", "h2", "a.poly-component__title"]:
                    elems = card.find_elements(By.CSS_SELECTOR, sel)
                    if elems and elems[0].text.strip():
                        titulo = elems[0].text.strip()
                        break

                # 2. Extração do Link
                link_elem = card.find_elements(By.TAG_NAME, "a")
                link = link_elem[0].get_attribute("href") if link_elem else ""

                # 3. Extração do Preço
                preco_num = 0.0
                for sel in [
                    ".poly-price__current .andromeda-money-amount__fraction",
                    ".poly-component__price .andromeda-money-amount__fraction",
                    ".andromeda-money-amount__fraction",
                    ".price-tag-fraction",
                    ".poly-price__current"
                ]:
                    elems = card.find_elements(By.CSS_SELECTOR, sel)
                    if elems and elems[0].text.strip():
                        txt = elems[0].text.replace(".", "").replace("R$", "").strip()
                        match = re.search(r'\d+', txt)
                        if match:
                            preco_num = float(match.group())
                            break

                # Fallback por Regex no texto do cartão
                if preco_num == 0.0:
                    match_fallback = re.search(r'R\$\s*([\d\.]+)', card.text)
                    if match_fallback:
                        try:
                            preco_num = float(match_fallback.group(1).replace(".", ""))
                        except Exception:
                            pass

                if titulo:
                    produtos_coletados.append({
                        "titulo": titulo,
                        "preco": preco_num,
                        "link": link
                    })
            except Exception:
                continue
    finally:
        driver.quit()

    return produtos_coletados

# ==========================================
# 3. INTERFACE GRÁFICA (Tkinter / ttkbootstrap)
# ==========================================
class AppAutomação:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Automação de Preços & Banco de Dados")
        self.root.geometry("980x620")

        init_db()
        self.criar_interface()

    def criar_interface(self):
        # Cabeçalho
        frame_header = ttk.Frame(self.root, bootstyle="primary")
        frame_header.pack(fill=tk.X)

        lbl_titulo = ttk.Label(
            frame_header, text="🛍️  Monitor de Produtos — Mercado Livre",
            font=("Helvetica", 17, "bold"), bootstyle="inverse-primary",
            padding=(15, 14)
        )
        lbl_titulo.pack(side=tk.LEFT)

        btn_admin = ttk.Button(
            frame_header, text="🔐 Admin", bootstyle="dark",
            command=self.abrir_login_admin
        )
        btn_admin.pack(side=tk.RIGHT, padx=15, pady=10)

        # Painel de Pesquisa
        frame_busca_card = ttk.Frame(self.root, padding=15)
        frame_busca_card.pack(fill=tk.X, padx=15, pady=(15, 5))

        frame_busca = ttk.Frame(frame_busca_card)
        frame_busca.pack(fill=tk.X)

        ttk.Label(frame_busca, text="Produto:", font=("Arial", 11)).pack(side=tk.LEFT, padx=(0, 5))

        self.ent_busca = ttk.Entry(frame_busca, font=("Arial", 11), width=30)
        self.ent_busca.pack(side=tk.LEFT, padx=5)
        self.ent_busca.bind("<Return>", lambda e: self.iniciar_busca_thread())

        ttk.Label(frame_busca, text="Qtd. produtos:", font=("Arial", 11)).pack(side=tk.LEFT, padx=(15, 5))

        self.spin_quantidade = ttk.Spinbox(frame_busca, from_=1, to=120, width=5, font=("Arial", 11), bootstyle="primary")
        self.spin_quantidade.delete(0, tk.END)
        self.spin_quantidade.insert(0, "10")
        self.spin_quantidade.pack(side=tk.LEFT, padx=5)

        self.btn_buscar = ttk.Button(
            frame_busca, text="🔍 Nova Pesquisa", bootstyle="primary",
            command=self.iniciar_busca_thread
        )
        self.btn_buscar.pack(side=tk.LEFT, padx=(15, 0))

        # Rótulo de Status
        self.lbl_status = ttk.Label(
            frame_busca_card, text="Status: Pronto", font=("Arial", 10, "italic"),
            bootstyle="secondary"
        )
        self.lbl_status.pack(anchor="w", pady=(8, 0))

        # Tabela (Treeview)
        frame_tabela = ttk.Frame(self.root, padding=(15, 5))
        frame_tabela.pack(fill=tk.BOTH, expand=True)
        frame_tabela.grid_rowconfigure(0, weight=1)
        frame_tabela.grid_columnconfigure(0, weight=1)

        colunas = ("Data/Hora", "Termo", "Produto", "Preço (R$)", "Link")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=12, bootstyle="primary")

        self.tree.heading("Data/Hora", text="Data/Hora")
        self.tree.heading("Termo", text="Termo")
        self.tree.heading("Produto", text="Produto")
        self.tree.heading("Preço (R$)", text="Preço (R$)")
        self.tree.heading("Link", text="Link")

        self.tree.column("Data/Hora", width=110, anchor="center", stretch=False)
        self.tree.column("Termo", width=110, stretch=False)
        self.tree.column("Produto", width=320, stretch=False)
        self.tree.column("Preço (R$)", width=100, anchor="center", stretch=False)
        self.tree.column("Link", width=420, stretch=False)

        scrollbar_v = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=self.tree.yview, bootstyle="round")
        scrollbar_h = ttk.Scrollbar(frame_tabela, orient=tk.HORIZONTAL, command=self.tree.xview, bootstyle="round")
        self.tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        scrollbar_h.grid(row=1, column=0, sticky="ew")

        # Painel Inferior de Ações
        frame_acoes = ttk.Frame(self.root, padding=(15, 5, 15, 15))
        frame_acoes.pack(fill=tk.X)

        # Grupo Histórico
        frame_historico = ttk.Labelframe(frame_acoes, text="📜  Histórico", padding=10, bootstyle="info")
        frame_historico.pack(side=tk.LEFT, padx=(0, 10), fill=tk.Y)

        btn_ver_banco = ttk.Button(
            frame_historico, text="📜 Carregar Histórico do Banco",
            bootstyle="info-outline", command=self.carregar_historico_banco
        )
        btn_ver_banco.pack(side=tk.LEFT, padx=5)

        btn_ver_exportacoes = ttk.Button(
            frame_historico, text="🗂️ Ver Exportações",
            bootstyle="secondary-outline", command=self.ver_exportacoes
        )
        btn_ver_exportacoes.pack(side=tk.LEFT, padx=5)

        btn_abrir_excel = ttk.Button(
            frame_historico, text="📂 Abrir e Ler Planilha Excel",
            bootstyle="warning-outline", command=self.abrir_arquivo_excel
        )
        btn_abrir_excel.pack(side=tk.LEFT, padx=5)

        # Grupo Exportação
        frame_exportar = ttk.Labelframe(frame_acoes, text="📤  Exportar Dados", padding=10, bootstyle="success")
        frame_exportar.pack(side=tk.LEFT, fill=tk.Y)

        btn_exportar = ttk.Button(
            frame_exportar, text="📊 Exportar para Excel",
            bootstyle="success", command=self.exportar_excel
        )
        btn_exportar.pack(side=tk.LEFT, padx=5)

        btn_exportar_json = ttk.Button(
            frame_exportar, text="🧾 Exportar para JSON",
            bootstyle="dark", command=self.exportar_json
        )
        btn_exportar_json.pack(side=tk.LEFT, padx=5)

    def atualizar_status(self, mensagem: str):
        self.lbl_status.config(text=f"Status: {mensagem}")
        self.root.update_idletasks()

    def limpar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def iniciar_busca_thread(self):
        termo = self.ent_busca.get().strip()
        if not termo:
            messagebox.showwarning("Aviso", "Por favor, digite um produto para pesquisar.")
            return

        try:
            quantidade = int(self.spin_quantidade.get())
        except ValueError:
            messagebox.showwarning("Aviso", "A quantidade de produtos deve ser um número.")
            return

        if quantidade < 1 or quantidade > 120:
            messagebox.showwarning("Aviso", "A quantidade de produtos deve estar entre 1 e 120.")
            return

        self.btn_buscar.config(state=tk.DISABLED)
        threading.Thread(target=self.rodar_automacao, args=(termo, quantidade), daemon=True).start()

    def rodar_automacao(self, termo: str, quantidade: int = 10):
        try:
            resultados = executar_scraping(termo, limite=quantidade, callback_status=self.atualizar_status)

            if resultados:
                self.atualizar_status("Salvando no Banco SQLite...")
                salvar_no_banco(termo, resultados)
                self.exibir_resultados_busca(termo, resultados)
                self.atualizar_status("✅ Concluído com sucesso!")
                messagebox.showinfo("Sucesso", f"Busca concluída!\n{len(resultados)} produtos encontrados e gravados no banco.")
            else:
                self.atualizar_status("Nenhum resultado encontrado.")
                messagebox.showwarning("Aviso", "Nenhum resultado foi retornado.")
        except Exception as e:
            self.atualizar_status("Erro durante a execução.")
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        finally:
            self.btn_buscar.config(state=tk.NORMAL)

    def exibir_resultados_busca(self, termo: str, resultados: list):
        self.limpar_tabela()
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        for item in resultados:
            preco_fmt = f"R$ {item['preco']:.2f}" if item["preco"] > 0 else "N/D"
            self.tree.insert("", tk.END, values=(data_hora, termo, item["titulo"], preco_fmt, item["link"]))

    def carregar_historico_banco(self):
        self.limpar_tabela()
        registros = obter_historico_completo()

        if not registros:
            self.atualizar_status("O banco de dados está vazio.")
            messagebox.showinfo("Informação", "Nenhum histórico encontrado no banco de dados.")
            return

        for reg in registros:
            data, termo, titulo, preco, link = reg
            preco_fmt = f"R$ {preco:.2f}" if preco and preco > 0 else "N/D"
            self.tree.insert("", tk.END, values=(data, termo, titulo, preco_fmt, link))

        self.atualizar_status(f"Carregados {len(registros)} registros do banco 'historico.db'.")

    def abrir_arquivo_excel(self):
        caminho = filedialog.askopenfilename(
            title="Selecione um arquivo Excel",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
        )
        if caminho:
            self.carregar_arquivo(caminho)

    def carregar_arquivo(self, caminho: str):
        try:
            if caminho.lower().endswith(".json"):
                with open(caminho, "r", encoding="utf-8") as f:
                    registros = json.load(f)
            else:
                df = pd.read_excel(caminho)
                registros = df.to_dict(orient="records")

            self.limpar_tabela()
            for row in registros:
                data = row.get("Data/Hora", "-")
                termo = row.get("Termo Pesquisado", row.get("Termo", "-"))
                titulo = row.get("Produto", row.get("titulo", "-"))
                preco = row.get("Preço (R$)", row.get("preco", 0.0))
                link = row.get("Link", row.get("link", "-"))

                preco_fmt = f"R$ {float(preco):.2f}" if isinstance(preco, (int, float)) and preco > 0 else str(preco)
                self.tree.insert("", tk.END, values=(data, termo, titulo, preco_fmt, link))

            self.atualizar_status(f"Exibindo dados do arquivo: {os.path.basename(caminho)}")
            messagebox.showinfo("Sucesso", f"Arquivo '{os.path.basename(caminho)}' carregado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao ler arquivo", f"Não foi possível ler o arquivo:\n{str(e)}")

    def exportar_excel(self):
        df = obter_df_historico()
        if df.empty:
            messagebox.showwarning("Aviso", "O banco de dados não possui registros para exportar.")
            return

        nome_arquivo = f"historico_exportado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(nome_arquivo, index=False)
        messagebox.showinfo("Exportado!", f"Histórico exportado com sucesso!\nArquivo gerado: {nome_arquivo}")

    def exportar_json(self):
        df = obter_df_historico()
        if df.empty:
            messagebox.showwarning("Aviso", "O banco de dados não possui registros para exportar.")
            return

        nome_arquivo = f"historico_exportado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        registros = df.to_dict(orient="records")
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(registros, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Exportado!", f"Histórico exportado com sucesso!\nArquivo gerado: {nome_arquivo}")

    def ver_exportacoes(self):
        arquivos = sorted(
            [f for f in os.listdir(".") if f.startswith("historico_exportado_") and f.lower().endswith((".xlsx", ".json"))],
            reverse=True
        )

        janela = ttk.Toplevel(self.root)
        janela.title("Exportações Salvas")
        janela.geometry("480x360")

        ttk.Label(
            janela, text="Arquivos exportados nesta pasta:",
            font=("Arial", 11, "bold"), padding=(10, 10, 10, 5)
        ).pack(anchor="w")

        lista = tk.Listbox(janela, font=("Arial", 10), width=58, height=12,
                            relief="flat", borderwidth=1, highlightthickness=1)
        lista.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        if not arquivos:
            lista.insert(tk.END, "Nenhuma exportação encontrada ainda.")
        else:
            for arq in arquivos:
                lista.insert(tk.END, arq)

        def carregar_selecionado():
            selecao = lista.curselection()
            if not selecao or not arquivos:
                messagebox.showwarning("Aviso", "Selecione um arquivo da lista.")
                return
            nome_arquivo = lista.get(selecao[0])
            self.carregar_arquivo(nome_arquivo)
            janela.destroy()

        btn_carregar = ttk.Button(
            janela, text="📥 Carregar Selecionado", bootstyle="primary",
            command=carregar_selecionado
        )
        btn_carregar.pack(pady=10)

    # Painel Admin
    def abrir_login_admin(self):
        janela = ttk.Toplevel(self.root)
        janela.title("Login Admin")
        janela.geometry("320x220")
        janela.resizable(False, False)

        ttk.Label(
            janela, text="🔐 Acesso Restrito", font=("Helvetica", 13, "bold"),
            padding=(0, 15, 0, 5)
        ).pack()

        frame_form = ttk.Frame(janela, padding=15)
        frame_form.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame_form, text="Usuário:").pack(anchor="w")
        ent_usuario = ttk.Entry(frame_form, width=28)
        ent_usuario.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Senha:").pack(anchor="w")
        ent_senha = ttk.Entry(frame_form, width=28, show="*")
        ent_senha.pack(pady=(0, 10))

        lbl_erro = ttk.Label(frame_form, text="", bootstyle="danger")
        lbl_erro.pack()

        def tentar_login():
            usuario = ent_usuario.get().strip()
            senha = ent_senha.get()

            if verificar_login_admin(usuario, senha):
                janela.destroy()
                self.abrir_painel_admin()
            else:
                lbl_erro.config(text="Usuário ou senha incorretos.")

        ent_senha.bind("<Return>", lambda e: tentar_login())

        btn_entrar = ttk.Button(frame_form, text="Entrar", bootstyle="primary", command=tentar_login)
        btn_entrar.pack(pady=5)

        ent_usuario.focus_set()

    def abrir_painel_admin(self):
        janela = ttk.Toplevel(self.root)
        janela.title("Painel Admin — Histórico Completo")
        janela.geometry("850x480")

        header = ttk.Frame(janela, bootstyle="dark")
        header.pack(fill=tk.X)
        ttk.Label(
            header, text="🔐 Painel Admin — Histórico Completo do Banco",
            font=("Helvetica", 13, "bold"), bootstyle="inverse-dark", padding=10
        ).pack(side=tk.LEFT)

        frame_tabela = ttk.Frame(janela, padding=10)
        frame_tabela.pack(fill=tk.BOTH, expand=True)
        frame_tabela.grid_rowconfigure(0, weight=1)
        frame_tabela.grid_columnconfigure(0, weight=1)

        colunas = ("Data/Hora", "Termo", "Produto", "Preço (R$)", "Link")
        tree_admin = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=15, bootstyle="dark")
        for col in colunas:
            tree_admin.heading(col, text=col)
            tree_admin.column(col, width=150, stretch=False)

        scrollbar_v = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tree_admin.yview, bootstyle="round")
        scrollbar_h = ttk.Scrollbar(frame_tabela, orient=tk.HORIZONTAL, command=tree_admin.xview, bootstyle="round")
        tree_admin.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        tree_admin.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        scrollbar_h.grid(row=1, column=0, sticky="ew")

        registros = obter_historico_completo()
        for reg in registros:
            data, termo, titulo, preco, link = reg
            preco_fmt = f"R$ {preco:.2f}" if preco and preco > 0 else "N/D"
            tree_admin.insert("", tk.END, values=(data, termo, titulo, preco_fmt, link))

        lbl_total = ttk.Label(
            janela, text=f"Total de registros: {len(registros)}",
            font=("Arial", 9, "italic"), bootstyle="secondary", padding=(10, 0)
        )
        lbl_total.pack(anchor="w")

        def baixar_tudo_json():
            df = obter_df_historico()
            if df.empty:
                messagebox.showwarning("Aviso", "O banco de dados não possui registros para baixar.")
                return

            caminho = filedialog.asksaveasfilename(
                title="Salvar histórico completo como...",
                defaultextension=".json",
                initialfile=f"historico_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                filetypes=[("Arquivo JSON", "*.json")]
            )
            if not caminho:
                return

            registros_json = df.to_dict(orient="records")
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(registros_json, f, ensure_ascii=False, indent=2)

            messagebox.showinfo("Baixado!", f"Histórico completo salvo em:\n{caminho}")

        btn_baixar = ttk.Button(
            janela, text="📥 Baixar Tudo em JSON", bootstyle="success",
            command=baixar_tudo_json
        )
        btn_baixar.pack(pady=10)

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    app = AppAutomação(root)
    root.mainloop()