import os
import sys
import json
import sqlite3
import threading
import datetime
import requests
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Dependências Opcionais / Externas
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas as pdf_canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# ==========================================
# GESTÃO DE BANCO DE DADOS E LOGS JSON
# ==========================================
DB_FILE = "monitor_data.db"
LOG_FILE = "activity_log.json"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metas_financeiras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            valor_alvo REAL NOT NULL,
            valor_atual REAL DEFAULT 0.0,
            data_limite TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            moeda_origem TEXT,
            moeda_destino TEXT,
            valor_origem REAL,
            valor_convertido REAL,
            taxa REAL,
            data_conversao TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            alvo TEXT,
            preco_alvo REAL,
            ativo INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

def log_event_json(tipo_evento, detalhe):
    evento = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": tipo_evento,
        "detalhes": detalhe
    }
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            logs = []
    logs.append(evento)
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erro ao salvar JSON log: {e}")


# ==========================================
# API DE MOEDAS TEMPO REAL
# ==========================================
def obter_cotacoes():
    """Busca cotações em tempo real via AwesomeAPI."""
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,GBP-BRL,JPY-BRL,CAD-BRL,BTC-BRL"
    try:
        res = requests.get(url, timeout=8)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None


# ==========================================
# INTERFACE GRÁFICA PRINCIPAL (TKINTER)
# ==========================================
class MonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Integrado de Monitoramento Financeiro & Metas")
        self.geometry("1000x780")
        self.minsize(900, 650)
        self.configure(bg="#181825")

        self.dados_cotacoes_atuais = None

        self.setup_styles()
        self.create_widgets()
        self.bind_shortcuts()
        
        self.atualizar_cotacoes_thread()

    def setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        
        self.bg_dark = "#181825"
        self.card_bg = "#1e1e2e"
        self.accent = "#89b4fa"
        self.fg_text = "#cdd6f4"

        self.style.configure(".", background=self.bg_dark, foreground=self.fg_text, font=("Segoe UI", 10))
        self.style.configure("TNotebook", background=self.bg_dark, borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#313244", foreground=self.fg_text, padding=[12, 8], font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", self.accent)], foreground=[("selected", "#11111b")])

        self.style.configure("Treeview", background=self.card_bg, foreground=self.fg_text, fieldbackground=self.card_bg, rowheight=28)
        self.style.configure("Treeview.Heading", background="#313244", foreground=self.accent, font=("Segoe UI", 10, "bold"))
        self.style.map("Treeview", background=[("selected", "#45475a")])

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_cotacoes = ttk.Frame(self.notebook)
        self.tab_metas = ttk.Frame(self.notebook)
        self.tab_alertas = ttk.Frame(self.notebook)
        self.tab_graficos = ttk.Frame(self.notebook)
        self.tab_relatorios = ttk.Frame(self.notebook)
        self.tab_acessibilidade = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_cotacoes, text="💱 Conversor & Moedas")
        self.notebook.add(self.tab_metas, text="🎯 Metas & Orçamento")
        self.notebook.add(self.tab_alertas, text="🔔 Alertas")
        self.notebook.add(self.tab_graficos, text="📊 Gráficos")
        self.notebook.add(self.tab_relatorios, text="📄 Relatórios")
        self.notebook.add(self.tab_acessibilidade, text="♿ Guia & Acessibilidade")

        self.build_tab_cotacoes()
        self.build_tab_metas()
        self.build_tab_alertas()
        self.build_tab_graficos()
        self.build_tab_relatorios()
        self.build_tab_acessibilidade()

        self.status_bar = tk.Label(self, text="Sistema pronto.", bg="#11111b", fg="#a6e3a1", anchor="w", padx=10, font=("Segoe UI", 9))
        self.status_bar.pack(side="bottom", fill="x")

    def bind_shortcuts(self):
        self.bind("<F1>", lambda e: self.notebook.select(5))
        self.bind("<Alt-1>", lambda e: self.notebook.select(0))
        self.bind("<Alt-2>", lambda e: self.notebook.select(1))
        self.bind("<Alt-3>", lambda e: self.notebook.select(2))
        self.bind("<Alt-4>", lambda e: self.notebook.select(3))
        self.bind("<Alt-5>", lambda e: self.notebook.select(4))
        self.bind("<Alt-6>", lambda e: self.notebook.select(5))

    # ABA 1: CONVERSOR & COTAÇÕES
    def build_tab_cotacoes(self):
        frame = tk.Frame(self.tab_cotacoes, bg=self.bg_dark, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Painel de Cotações em Tempo Real", font=("Segoe UI", 14, "bold"), fg=self.accent, bg=self.bg_dark).pack(anchor="w", pady=(0, 15))

        self.lbl_cotacoes_cards = tk.Label(frame, text="Carregando dados...", font=("Consolas", 11), bg=self.card_bg, fg="#a6e3a1", justify="left", padx=15, pady=15, relief="solid", bd=1)
        self.lbl_cotacoes_cards.pack(fill="x", pady=(0, 20))

        btn_atualizar = tk.Button(frame, text="🔄 Atualizar Cotações Agora", command=self.atualizar_cotacoes_thread, bg=self.accent, fg="#11111b", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", padx=10, pady=5)
        btn_atualizar.pack(anchor="w", pady=(0, 25))

        conv_frame = tk.LabelFrame(frame, text=" Conversor Integrado ", font=("Segoe UI", 11, "bold"), bg=self.card_bg, fg=self.accent, padx=15, pady=15)
        conv_frame.pack(fill="x")

        row = tk.Frame(conv_frame, bg=self.card_bg)
        row.pack(fill="x", pady=5)

        tk.Label(row, text="Valor:", bg=self.card_bg, fg=self.fg_text).pack(side="left", padx=(0, 5))
        self.ent_val_conv = tk.Entry(row, width=12, font=("Segoe UI", 10))
        self.ent_val_conv.insert(0, "100.00")
        self.ent_val_conv.pack(side="left", padx=(0, 15))

        tk.Label(row, text="De:", bg=self.card_bg, fg=self.fg_text).pack(side="left", padx=(0, 5))
        self.cb_moeda_de = ttk.Combobox(row, values=["USD", "EUR", "GBP", "JPY", "CAD", "BTC", "BRL"], width=8, state="readonly")
        self.cb_moeda_de.set("USD")
        self.cb_moeda_de.pack(side="left", padx=(0, 15))

        tk.Label(row, text="Para:", bg=self.card_bg, fg=self.fg_text).pack(side="left", padx=(0, 5))
        self.cb_moeda_para = ttk.Combobox(row, values=["BRL", "USD", "EUR", "GBP", "JPY", "CAD", "BTC"], width=8, state="readonly")
        self.cb_moeda_para.set("BRL")
        self.cb_moeda_para.pack(side="left", padx=(0, 15))

        btn_calcular = tk.Button(row, text="Converter", command=self.executar_conversao, bg="#a6e3a1", fg="#11111b", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", padx=10)
        btn_calcular.pack(side="left")

        self.lbl_resultado_conv = tk.Label(conv_frame, text="Resultado: -", font=("Segoe UI", 12, "bold"), bg=self.card_bg, fg="#f9e2af")
        self.lbl_resultado_conv.pack(anchor="w", pady=(15, 0))

    def atualizar_cotacoes_thread(self):
        self.status_bar.config(text="Atualizando cotações...")
        threading.Thread(target=self._worker_cotacoes, daemon=True).start()

    def _worker_cotacoes(self):
        dados = obter_cotacoes()
        if dados:
            try:
                texto = (
                    f"💵 Dólar (USD): R$ {float(dados['USDBRL']['bid']):.2f}   |   "
                    f"💶 Euro (EUR): R$ {float(dados['EURBRL']['bid']):.2f}\n"
                    f"💷 Libra (GBP): R$ {float(dados['GBPBRL']['bid']):.2f}   |   "
                    f"💴 Iene (JPY): R$ {float(dados['JPYBRL']['bid']):.4f}\n"
                    f"🇨🇦 CAD: R$ {float(dados['CADBRL']['bid']):.2f}         |   "
                    f"₿ Bitcoin (BTC): R$ {float(dados['BTCBRL']['bid']):,.2f}"
                )
                self.dados_cotacoes_atuais = dados
            except KeyError:
                texto = "Erro ao formatar os dados de cotações recebidos."
                self.dados_cotacoes_atuais = None
        else:
            texto = "Não foi possível conectar com o servidor de cotações."
            self.dados_cotacoes_atuais = None

        self.after(0, lambda: self._update_cotacoes_ui(texto))

    def _update_cotacoes_ui(self, texto):
        self.lbl_cotacoes_cards.config(text=texto)
        self.status_bar.config(text="Cotações atualizadas.")

    def executar_conversao(self):
        try:
            val = float(self.ent_val_conv.get().replace(",", "."))
            de = self.cb_moeda_de.get()
            para = self.cb_moeda_para.get()

            if de == para:
                res = val
                taxa = 1.0
            else:
                def get_rate(m):
                    if m == "BRL": return 1.0
                    key = f"{m}BRL"
                    if self.dados_cotacoes_atuais and key in self.dados_cotacoes_atuais:
                        return float(self.dados_cotacoes_atuais[key]['bid'])
                    return None

                taxa_de = get_rate(de)
                taxa_para = get_rate(para)

                if taxa_de is None or taxa_para is None:
                    messagebox.showwarning("Aviso", "Por favor, atualize as cotações primeiro.")
                    return

                valor_brl = val * taxa_de
                res = valor_brl / taxa_para
                taxa = taxa_de / taxa_para

            self.lbl_resultado_conv.config(text=f"Resultado: {val:.2f} {de} = {res:.2f} {para} (Taxa: {taxa:.4f})")

            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO conversoes (moeda_origem, moeda_destino, valor_origem, valor_convertido, taxa, data_conversao) VALUES (?, ?, ?, ?, ?, ?)",
                      (de, para, val, res, taxa, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            conn.close()
            log_event_json("CONVERSAO", {"de": de, "para": para, "valor": val, "resultado": res})
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor numérico válido.")

    # ABA 2: METAS & ORÇAMENTO PESSOAL
    def build_tab_metas(self):
        frame = tk.Frame(self.tab_metas, bg=self.bg_dark, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Gestão de Metas Financeiras e Orçamento", font=("Segoe UI", 14, "bold"), fg=self.accent, bg=self.bg_dark).pack(anchor="w", pady=(0, 10))

        form_frame = tk.LabelFrame(frame, text=" Nova Meta / Orçamento ", font=("Segoe UI", 10, "bold"), bg=self.card_bg, fg=self.accent, padx=15, pady=10)
        form_frame.pack(fill="x", pady=(0, 15))

        f_row1 = tk.Frame(form_frame, bg=self.card_bg)
        f_row1.pack(fill="x", pady=4)

        tk.Label(f_row1, text="Nome da Meta:", bg=self.card_bg, fg=self.fg_text).pack(side="left", padx=(0, 5))
        self.ent_meta_nome = tk.Entry(f_row1, width=20)
        self.ent_meta_nome.pack(side="left", padx=(0, 15))

        tk.Label(f_row1, text="Categoria:", bg=self.card_bg, fg=self.fg_text).pack(side="left", padx=(0, 5))
        self.cb_meta_cat = ttk.Combobox(f_row1, values=["Reserva de Emergência", "Investimentos", "Viagem", "Tecnologia", "Educação", "Outros"], width=18, state="readonly")
        self.cb_meta_cat.set("Reserva de Emergência")
        self.cb_meta_cat.pack(side="left", padx=(0, 15))

        f_row2 = tk.Frame(form_frame, bg=self.card_bg)
        f_row2.pack(fill="x", pady=4)

        tk.Label(f_row2, text="Valor Alvo (R$):", bg=self.card_bg, fg=self.fg_text).pack(side="left", padx=(0, 5))
        self.ent_meta_alvo = tk.Entry(f_row2, width=12)
        self.ent_meta_alvo.pack(side="left", padx=(0, 15))

        tk.Label(f_row2, text="Valor Atual (R$):", bg=self.card_bg, fg=self.fg_text).pack(side="left", padx=(0, 5))
        self.ent_meta_atual = tk.Entry(f_row2, width=12)
        self.ent_meta_atual.insert(0, "0.00")
        self.ent_meta_atual.pack(side="left", padx=(0, 15))

        tk.Label(f_row2, text="Data Limite:", bg=self.card_bg, fg=self.fg_text).pack(side="left", padx=(0, 5))
        self.ent_meta_data = tk.Entry(f_row2, width=12)
        self.ent_meta_data.insert(0, datetime.datetime.now().strftime("%Y-12-31"))
        self.ent_meta_data.pack(side="left", padx=(0, 15))

        btn_salvar_meta = tk.Button(f_row2, text="➕ Adicionar Meta", command=self.salvar_meta, bg=self.accent, fg="#11111b", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", padx=10)
        btn_salvar_meta.pack(side="left")

        # Tabela de Metas
        columns = ("id", "nome", "categoria", "alvo", "atual", "progresso", "limite")
        self.tree_metas = ttk.Treeview(frame, columns=columns, show="headings")
        self.tree_metas.heading("id", text="ID")
        self.tree_metas.heading("nome", text="Meta / Objetivo")
        self.tree_metas.heading("categoria", text="Categoria")
        self.tree_metas.heading("alvo", text="Alvo (R$)")
        self.tree_metas.heading("atual", text="Atual (R$)")
        self.tree_metas.heading("progresso", text="% Concluído")
        self.tree_metas.heading("limite", text="Data Limite")

        self.tree_metas.column("id", width=40, anchor="center")
        self.tree_metas.column("nome", width=200)
        self.tree_metas.column("categoria", width=140)
        self.tree_metas.column("alvo", width=110, anchor="e")
        self.tree_metas.column("atual", width=110, anchor="e")
        self.tree_metas.column("progresso", width=100, anchor="center")
        self.tree_metas.column("limite", width=100, anchor="center")

        self.tree_metas.pack(fill="both", expand=True, pady=(0, 10))

        action_bar = tk.Frame(frame, bg=self.bg_dark)
        action_bar.pack(fill="x")

        tk.Button(action_bar, text="💵 Aportar / Atualizar Saldo Selecionado", command=self.atualizar_saldo_meta, bg="#a6e3a1", fg="#11111b", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", padx=10).pack(side="left", padx=(0, 10))
        tk.Button(action_bar, text="❌ Excluir Meta", command=self.excluir_meta, bg="#f38ba8", fg="#11111b", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", padx=10).pack(side="left")

        self.carregar_metas_db()

    def salvar_meta(self):
        nome = self.ent_meta_nome.get().strip()
        cat = self.cb_meta_cat.get()
        data_lim = self.ent_meta_data.get().strip()
        try:
            val_alvo = float(self.ent_meta_alvo.get().replace(",", "."))
            val_atual = float(self.ent_meta_atual.get().replace(",", "."))
            if not nome or val_alvo <= 0:
                raise ValueError()

            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO metas_financeiras (nome, categoria, valor_alvo, valor_atual, data_limite) VALUES (?, ?, ?, ?, ?)",
                      (nome, cat, val_alvo, val_atual, data_lim))
            conn.commit()
            conn.close()

            log_event_json("NOVA_META", {"nome": nome, "alvo": val_alvo, "atual": val_atual})
            messagebox.showinfo("Sucesso", "Meta cadastrada com sucesso!")
            
            self.ent_meta_nome.delete(0, tk.END)
            self.ent_meta_alvo.delete(0, tk.END)
            self.ent_meta_atual.delete(0, tk.END)
            self.ent_meta_atual.insert(0, "0.00")

            self.carregar_metas_db()
            self.atualizar_graficos()
        except ValueError:
            messagebox.showerror("Erro", "Preencha o nome e valores numéricos válidos.")

    def carregar_metas_db(self):
        for item in self.tree_metas.get_children():
            self.tree_metas.delete(item)

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT id, nome, categoria, valor_alvo, valor_atual, data_limite FROM metas_financeiras")
        rows = c.fetchall()
        conn.close()

        for r in rows:
            m_id, nome, cat, alvo, atual, limite = r
            pct = (atual / alvo * 100) if alvo > 0 else 0
            self.tree_metas.insert("", "end", values=(m_id, nome, cat, f"R$ {alvo:,.2f}", f"R$ {atual:,.2f}", f"{pct:.1f}%", limite))

    def atualizar_saldo_meta(self):
        selected = self.tree_metas.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma meta na tabela para atualizar o saldo.")
            return

        item = self.tree_metas.item(selected[0])
        meta_id = item["values"][0]
        nome_meta = item["values"][1]

        def popup_salvar():
            try:
                novo_val = float(ent_novo.get().replace(",", "."))
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("UPDATE metas_financeiras SET valor_atual = ? WHERE id = ?", (novo_val, meta_id))
                conn.commit()
                conn.close()
                log_event_json("ATUALIZACAO_META", {"id": meta_id, "novo_saldo": novo_val})
                top.destroy()
                self.carregar_metas_db()
                self.atualizar_graficos()
            except ValueError:
                messagebox.showerror("Erro", "Insira um valor válido.")

        top = tk.Toplevel(self)
        top.title("Atualizar Saldo")
        top.geometry("300x150")
        top.configure(bg=self.card_bg)

        tk.Label(top, text=f"Novo saldo para '{nome_meta}':", bg=self.card_bg, fg=self.fg_text).pack(pady=10)
        ent_novo = tk.Entry(top, font=("Segoe UI", 10))
        ent_novo.pack(pady=5)
        tk.Button(top, text="Salvar", command=popup_salvar, bg=self.accent, fg="#11111b", font=("Segoe UI", 9, "bold")).pack(pady=10)

    def excluir_meta(self):
        selected = self.tree_metas.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma meta para excluir.")
            return

        meta_id = self.tree_metas.item(selected[0])["values"][0]
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("DELETE FROM metas_financeiras WHERE id = ?", (meta_id,))
        conn.commit()
        conn.close()

        self.carregar_metas_db()
        self.atualizar_graficos()

    # ABA 3: ALERTAS DE PREÇO / COTAÇÃO
    def build_tab_alertas(self):
        frame = tk.Frame(self.tab_alertas, bg=self.bg_dark, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Gerenciador de Alertas de Preços / Cotações", font=("Segoe UI", 14, "bold"), fg=self.accent, bg=self.bg_dark).pack(anchor="w", pady=(0, 15))

        form = tk.Frame(frame, bg=self.card_bg, padx=15, pady=15)
        form.pack(fill="x", pady=(0, 15))

        tk.Label(form, text="Tipo:", bg=self.card_bg, fg=self.fg_text).pack(side="left", padx=(0, 5))
        self.cb_alerta_tipo = ttk.Combobox(form, values=["Moeda", "Meta Progresso"], width=15, state="readonly")
        self.cb_alerta_tipo.set("Moeda")
        self.cb_alerta_tipo.pack(side="left", padx=(0, 15))

        tk.Label(form, text="Alvo (ex: USD):", bg=self.card_bg, fg=self.fg_text).pack(side="left", padx=(0, 5))
        self.ent_alerta_alvo = tk.Entry(form, width=15)
        self.ent_alerta_alvo.pack(side="left", padx=(0, 15))

        tk.Label(form, text="Preço Máximo Teto (R$):", bg=self.card_bg, fg=self.fg_text).pack(side="left", padx=(0, 5))
        self.ent_alerta_preco = tk.Entry(form, width=12)
        self.ent_alerta_preco.pack(side="left", padx=(0, 15))

        btn_add = tk.Button(form, text="➕ Salvar Alerta", command=self.adicionar_alerta, bg=self.accent, fg="#11111b", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2")
        btn_add.pack(side="left")

        self.tree_alertas = ttk.Treeview(frame, columns=("id", "tipo", "alvo", "preco"), show="headings")
        self.tree_alertas.heading("id", text="ID")
        self.tree_alertas.heading("tipo", text="Tipo")
        self.tree_alertas.heading("alvo", text="Alvo")
        self.tree_alertas.heading("preco", text="Preço Alvo Teto")
        self.tree_alertas.column("id", width=50)
        self.tree_alertas.pack(fill="both", expand=True)

        self.carregar_alertas_db()

    def adicionar_alerta(self):
        tipo = self.cb_alerta_tipo.get()
        alvo = self.ent_alerta_alvo.get().strip()
        try:
            preco = float(self.ent_alerta_preco.get().replace(",", "."))
            if not alvo: raise ValueError()
            
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO alertas (tipo, alvo, preco_alvo) VALUES (?, ?, ?)", (tipo, alvo, preco))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Alerta cadastrado com sucesso!")
            self.carregar_alertas_db()
        except ValueError:
            messagebox.showerror("Erro", "Preencha o alvo e o preço limite corretamente.")

    def carregar_alertas_db(self):
        for item in self.tree_alertas.get_children():
            self.tree_alertas.delete(item)
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT id, tipo, alvo, preco_alvo FROM alertas WHERE ativo = 1")
        for row in c.fetchall():
            self.tree_alertas.insert("", "end", values=(row[0], row[1], row[2], f"R$ {row[3]:,.2f}"))
        conn.close()

    # ABA 4: GRÁFICOS (MATPLOTLIB)
    def build_tab_graficos(self):
        frame = tk.Frame(self.tab_graficos, bg=self.bg_dark, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Progresso das Metas Financeiras", font=("Segoe UI", 14, "bold"), fg=self.accent, bg=self.bg_dark).pack(anchor="w", pady=(0, 10))

        if not MATPLOTLIB_AVAILABLE:
            tk.Label(frame, text="Biblioteca Matplotlib não instalada.\nInstale com: pip install matplotlib", fg="#f38ba8", bg=self.bg_dark).pack(expand=True)
            return

        self.fig = Figure(figsize=(8, 4), dpi=100, facecolor="#181825")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#1e1e2e")
        self.ax.tick_params(colors="#cdd6f4")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.atualizar_graficos()

    def atualizar_graficos(self):
        if not MATPLOTLIB_AVAILABLE or not hasattr(self, 'ax'):
            return
        
        self.ax.clear()
        self.ax.set_facecolor("#1e1e2e")
        self.ax.tick_params(colors="#cdd6f4")

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT nome, valor_alvo, valor_atual FROM metas_financeiras LIMIT 6")
        rows = c.fetchall()
        conn.close()

        if rows:
            nomes = [r[0][:12] for r in rows]
            alvos = [r[1] for r in rows]
            atuais = [r[2] for r in rows]

            x = range(len(nomes))
            width = 0.35

            self.ax.bar([i - width/2 for i in x], alvos, width, label="Alvo (R$)", color="#45475a")
            self.ax.bar([i + width/2 for i in x], atuais, width, label="Atual (R$)", color="#89b4fa")

            self.ax.set_xticks(list(x))
            self.ax.set_xticklabels(nomes)
            self.ax.legend(facecolor="#1e1e2e", labelcolor="#cdd6f4")
            self.ax.set_ylabel("Valor (R$)", color="#cdd6f4")
            self.ax.set_title("Comparativo: Valor Alvo vs Saldo Atual", color="#cdd6f4")
        else:
            self.ax.text(0.5, 0.5, "Cadastre metas para visualizar o gráfico comparativo.", color="#cdd6f4", ha="center")

        self.canvas.draw()

    # ABA 5: RELATÓRIOS (CSV & PDF)
    def build_tab_relatorios(self):
        frame = tk.Frame(self.tab_relatorios, bg=self.bg_dark, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Central de Exportação de Relatórios", font=("Segoe UI", 14, "bold"), fg=self.accent, bg=self.bg_dark).pack(anchor="w", pady=(0, 15))

        box = tk.Frame(frame, bg=self.card_bg, padx=20, pady=20)
        box.pack(fill="x")

        tk.Button(box, text="📥 Exportar Metas Financeiras (CSV)", command=self.exportar_csv, bg=self.accent, fg="#11111b", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", padx=10, pady=8).pack(anchor="w", pady=5)
        tk.Button(box, text="📄 Gerar Relatório Executivo de Metas (PDF)", command=self.exportar_pdf, bg="#a6e3a1", fg="#11111b", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", padx=10, pady=8).pack(anchor="w", pady=5)

    def exportar_csv(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not filepath: return

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM metas_financeiras")
        rows = c.fetchall()
        conn.close()

        import csv
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Nome Meta", "Categoria", "Valor Alvo", "Valor Atual", "Data Limite"])
            writer.writerows(rows)

        messagebox.showinfo("Sucesso", f"Relatório CSV salvo em:\n{filepath}")

    def exportar_pdf(self):
        if not REPORTLAB_AVAILABLE:
            messagebox.showwarning("Aviso", "Biblioteca ReportLab não instalada.\nInstale com: pip install reportlab")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not filepath: return

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT nome, categoria, valor_alvo, valor_atual, data_limite FROM metas_financeiras")
        rows = c.fetchall()
        conn.close()

        c_pdf = pdf_canvas.Canvas(filepath, pagesize=letter)
        c_pdf.setFont("Helvetica-Bold", 16)
        c_pdf.drawString(50, 750, "Relatório Executivo de Metas Financeiras")
        c_pdf.setFont("Helvetica", 10)
        c_pdf.drawString(50, 730, f"Gerado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        y = 690
        c_pdf.drawString(50, y, "Objetivo")
        c_pdf.drawString(200, y, "Categoria")
        c_pdf.drawString(320, y, "Alvo (R$)")
        c_pdf.drawString(420, y, "Atual (R$)")
        c_pdf.drawString(500, y, "%")
        c_pdf.line(50, y-5, 550, y-5)
        
        y -= 25
        for row in rows:
            if y < 50:
                c_pdf.showPage()
                y = 750
            nome, cat, alvo, atual, lim = row
            pct = (atual / alvo * 100) if alvo > 0 else 0
            c_pdf.drawString(50, y, str(nome)[:20])
            c_pdf.drawString(200, y, str(cat)[:15])
            c_pdf.drawString(320, y, f"R$ {alvo:,.2f}")
            c_pdf.drawString(420, y, f"R$ {atual:,.2f}")
            c_pdf.drawString(500, y, f"{pct:.0f}%")
            y -= 20

        c_pdf.save()
        messagebox.showinfo("Sucesso", f"Relatório PDF gerado em:\n{filepath}")

    # ABA 6: GUIA & ACESSIBILIDADE
    def build_tab_acessibilidade(self):
        frame = tk.Frame(self.tab_acessibilidade, bg=self.bg_dark, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Guia de Uso & Acessibilidade", font=("Segoe UI", 14, "bold"), fg=self.accent, bg=self.bg_dark).pack(anchor="w", pady=(0, 10))

        btn_voz = tk.Button(frame, text="🔊 Ouvir Explicação (Voz)", command=self.falar_guias, bg="#f9e2af", fg="#11111b", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2")
        btn_voz.pack(anchor="w", pady=(0, 15))

        self.txt_guia = tk.Text(frame, bg=self.card_bg, fg=self.fg_text, font=("Segoe UI", 10), wrap="word", padx=10, pady=10)
        self.txt_guia.pack(fill="both", expand=True)

        texto_explicativo = (
            "SOBRE O SISTEMA:\n"
            "Este software é um gerenciador financeiro projetado para auxiliar no acompanhamento de cotações de moedas e na gestão de metas de orçamento pessoal.\n\n"
            "COMO ELE TE AJUDA NO DIA A DIA:\n"
            "1. Cotações e Conversões: Permite visualizar instantaneamente taxas de moedas estrangeiras (Dólar, Euro, Bitcoin) em tempo real e fazer conversões diretas.\n"
            "2. Gestão de Metas & Orçamento: Permite cadastrar e acompanhar metas financeiras (ex: Reserva de Emergência, Viagens, Compras), monitorando o valor acumulado e a porcentagem concluída.\n"
            "3. Gráficos & Alertas: Exibe comparativos visuais do progresso das suas metas e permite salvar alertas de preço teto.\n"
            "4. Exportação de Dados: Gera relatórios completos em formatos CSV e PDF organizados para impressão ou backup.\n\n"
            "TECLAS DE ATALHO DE NAVEGAÇÃO:\n"
            "• F1: Abre esta tela de Ajuda e Acessibilidade.\n"
            "• Alt + 1: Vai para a aba Conversor & Moedas.\n"
            "• Alt + 2: Vai para a aba Metas & Orçamento.\n"
            "• Alt + 3: Vai para a aba Alertas.\n"
            "• Alt + 4: Vai para a aba Gráficos.\n"
            "• Alt + 5: Vai para a aba Relatórios."
        )
        self.txt_guia.insert("1.0", texto_explicativo)
        self.txt_guia.config(state="disabled")

    def falar_guias(self):
        if not PYTTSX3_AVAILABLE:
            messagebox.showwarning("Aviso", "Sintetizador de voz pyttsx3 não disponível.\nInstale com: pip install pyttsx3")
            return
        
        def _speak():
            try:
                engine = pyttsx3.init()
                engine.say("Bem-vindo ao sistema de cotações e metas financeiras. Pressione Alt de 1 a 6 para navegar entre as abas ou F1 para retornar a esta ajuda.")
                engine.runAndWait()
            except Exception as e:
                print(f"Erro no leitor de voz: {e}")

        threading.Thread(target=_speak, daemon=True).start()


# ==========================================
# EXECUÇÃO DA APLICAÇÃO
# ==========================================
if __name__ == "__main__":
    init_db()
    app = MonitorApp()
    app.mainloop()