import os
import json
import random
import sqlite3
import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import messagebox, ttk

# Importação de biblioteca opcional para dados fictícios
try:
    from faker import Faker
    fake = Faker("pt_BR")
except ImportError:
    fake = None

# =====================================================
# CONFIGURAÇÃO DE APARÊNCIA E TEMA
# =====================================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

NOME_LOJA = "⚽ NAÇÃO DOS MANTOS ⚽"
INSTAGRAM_LOJA = "📸 @nacaodosmantosoficial"
BANCO = "loja_camisas.db"
ARQUIVO_JSON = "configuracao.json"
PRECO_PERSONALIZACAO = 20.00

def carregar_configuracao():
    if os.path.exists(ARQUIVO_JSON):
        try:
            with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"preco_personalizacao": PRECO_PERSONALIZACAO, "loja": NOME_LOJA}

def salvar_configuracao():
    dados = {
        "loja": NOME_LOJA,
        "preco_personalizacao": PRECO_PERSONALIZACAO
    }
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

salvar_configuracao()

# Dicionário base de dados para carga inicial do catálogo
times_dados = {
    "Athletico-PR": {"preco": 340.90, "sigla": "CAP", "cor": "#C62828", "icone": "🛡️🔴"},
    "Atletico-MG": {"preco": 159.90, "sigla": "CAM", "cor": "#212121", "icone": "🛡️⚫"},
    "Bahia": {"preco": 300.90, "sigla": "BAH", "cor": "#1565C0", "icone": "🛡️🔵"},
    "Botafogo": {"preco": 149.90, "sigla": "BOT", "cor": "#111111", "icone": "🛡️⭐"},
    "Chapecoense": {"preco": 119.90, "sigla": "CHA", "cor": "#2E7D32", "icone": "🛡️🟢"},
    "Corinthians": {"preco": 360.90, "sigla": "COR", "cor": "#424242", "icone": "🛡️🦅"},
    "Coritiba": {"preco": 420.90, "sigla": "CFC", "cor": "#388E3C", "icone": "🛡️🟢"},
    "Cruzeiro": {"preco": 432.90, "sigla": "CRU", "cor": "#1565C0", "icone": "🛡️🦊"},
    "Flamengo": {"preco": 350.90, "sigla": "FLA", "cor": "#B71C1C", "icone": "🛡️🔴"},
    "Fluminense": {"preco": 159.90, "sigla": "FLU", "cor": "#00695C", "icone": "🛡️🇭🇺"},
    "Gremio": {"preco": 300.90, "sigla": "GRE", "cor": "#0277BD", "icone": "🛡️🇪🇪"},
    "Internacional": {"preco": 500.90, "sigla": "INT", "cor": "#D32F2F", "icone": "🛡️🇦🇹"},
    "Mirassol": {"preco": 119.90, "sigla": "MIR", "cor": "#F9A825", "icone": "🛡️🟡"},
    "Palmeiras": {"preco": 179.90, "sigla": "PAL", "cor": "#1B5E20", "icone": "🛡️🐷"},
    "Red Bull Bragantino": {"preco": 139.90, "sigla": "RBB", "cor": "#D32F2F", "icone": "🛡️🐂"},
    "Remo": {"preco": 119.90, "sigla": "REM", "cor": "#283593", "icone": "🛡️⚓"},
    "Santos": {"preco": 149.90, "sigla": "SAN", "cor": "#212121", "icone": "🛡️🐳"},
    "Sao Paulo": {"preco": 169.90, "sigla": "SPFC", "cor": "#C62828", "icone": "🛡️🇾🇪"},
    "Vasco": {"preco": 159.90, "sigla": "VAS", "cor": "#212121", "icone": "🛡️◤🇲🇰◢"},
    "Vitoria": {"preco": 129.90, "sigla": "VIT", "cor": "#C62828", "icone": "🛡️🦁"}
}

# =====================================================
# INICIALIZAÇÃO E CONEXÃO COM O BANCO DE DADOS (SQLITE)
# =====================================================
conexao = sqlite3.connect(BANCO, check_same_thread=False)
cursor = conexao.cursor()

# Tabela de Produtos/Estoque
cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    estoque_pp INTEGER DEFAULT 20,
    estoque_p INTEGER DEFAULT 20,
    estoque_m INTEGER DEFAULT 20,
    estoque_g INTEGER DEFAULT 20,
    estoque_gg INTEGER DEFAULT 20,
    estoque_xg INTEGER DEFAULT 20
)
""")

# Tabela de Pedidos
cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    telefone TEXT NOT NULL,
    cpf TEXT NOT NULL,
    endereco TEXT NOT NULL,
    regiao TEXT NOT NULL,
    obs TEXT NOT NULL,
    detalhes TEXT NOT NULL,
    subtotal REAL NOT NULL,
    desconto REAL NOT NULL,
    taxa_entrega REAL NOT NULL,
    total REAL NOT NULL,
    data TEXT NOT NULL,
    previsao TEXT NOT NULL,
    rastreio TEXT NOT NULL,
    pagamento TEXT NOT NULL,
    banco TEXT NOT NULL,
    brinde TEXT NOT NULL,
    status TEXT NOT NULL
)
""")
conexao.commit()

# Carga inicial do catálogo no banco de dados
cursor.execute("SELECT COUNT(*) FROM produtos")
if cursor.fetchone()[0] == 0:
    for time, dados in times_dados.items():
        cursor.execute("""
            INSERT INTO produtos (nome, preco, estoque_pp, estoque_p, estoque_m, estoque_g, estoque_gg, estoque_xg)
            VALUES (?, ?, 20, 20, 20, 20, 20, 20)
        """, ("Camisa " + time, dados["preco"]))
    conexao.commit()

# =====================================================
# INTERFACE GRÁFICA PRINCIPAL
# =====================================================
janela = ctk.CTk()
janela.title(NOME_LOJA)
janela.geometry("1220x960")

carrinho = []
time_selecionado = None
botoes_times_dados = []
cards_times_lista = []
desconto_aplicado = 0.0
cupom_ativo = ""

# Variáveis globais para guardar a referência das janelas abertas
win_admin = None
win_historico = None

janela.grid_columnconfigure(0, weight=6)
janela.grid_columnconfigure(1, weight=5)
janela.grid_rowconfigure(0, weight=1)

frame_superior_tema = ctk.CTkFrame(janela, fg_color="transparent")
frame_superior_tema.grid(row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=(5, 0))

def alternar_modo_tema():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
        btn_tema.configure(text="🌙 Modo Escuro")
    else:
        ctk.set_appearance_mode("Dark")
        btn_tema.configure(text="☀️ Modo Claro")

btn_tema = ctk.CTkButton(frame_superior_tema, text="☀️ Modo Claro", width=130, height=26, fg_color="#FF9800", hover_color="#F57C00", text_color="#000000", font=ctk.CTkFont(weight="bold"), command=alternar_modo_tema)
btn_tema.pack(side="right")

frame_esquerdo = ctk.CTkFrame(janela, corner_radius=15, border_width=2, border_color="#FF9800")
frame_esquerdo.grid(row=0, column=0, padx=12, pady=(35, 12), sticky="nsew")

frame_topo_loja = ctk.CTkFrame(frame_esquerdo, fg_color="#1E1E2C", corner_radius=10)
frame_topo_loja.pack(fill="x", padx=15, pady=(12, 5))

lbl_gato = ctk.CTkLabel(frame_topo_loja, text="🐱⚽", font=ctk.CTkFont(size=36))
lbl_gato.pack(side="left", padx=10, pady=8)

frame_titulos = ctk.CTkFrame(frame_topo_loja, fg_color="transparent")
frame_titulos.pack(side="left", fill="both", expand=True, padx=5, pady=5)

ctk.CTkLabel(frame_titulos, text=NOME_LOJA, font=ctk.CTkFont(size=16, weight="bold"), text_color="#FFD700").pack(anchor="w", pady=(2, 0))

frame_insta = ctk.CTkFrame(frame_titulos, fg_color="transparent")
frame_insta.pack(anchor="w", pady=1)

ctk.CTkLabel(frame_insta, text="🛡️", font=ctk.CTkFont(size=13)).pack(side="left", padx=(0, 4))
ctk.CTkLabel(frame_insta, text=INSTAGRAM_LOJA, font=ctk.CTkFont(size=12, weight="bold"), text_color="#E1306C").pack(side="left")

ctk.CTkLabel(frame_titulos, text="🐾 O Gato artilheiro do Inter e dos mantos!", font=ctk.CTkFont(size=10, weight="bold"), text_color="#00E676").pack(anchor="w", pady=(0, 2))

lbl_banner_boas_vindas = ctk.CTkLabel(
    frame_esquerdo, 
    text="OLÁ SEJA BEM VINDO A LOJA NAÇÃO DOS MANTOS O QUE DESEJA?", 
    font=ctk.CTkFont(size=15, weight="bold"), 
    text_color="#FF1744",
    justify="center"
)
lbl_banner_boas_vindas.pack(fill="x", padx=15, pady=(2, 8))

frame_busca = ctk.CTkFrame(frame_esquerdo, fg_color="transparent")
frame_busca.pack(fill="x", padx=15, pady=2)

def filtrar_times(event=None):
    termo = campo_busca.get().lower()
    for card, nome_time in cards_times_lista:
        if termo in nome_time.lower():
            card.pack(fill="x", padx=5, pady=4)
        else:
            card.pack_forget()

campo_busca = ctk.CTkEntry(frame_busca, placeholder_text="🔍 Pesquisar time...", height=30)
campo_busca.pack(fill="x", padx=0, pady=2)
campo_busca.bind("<KeyRelease>", filtrar_times)

scroll_times = ctk.CTkScrollableFrame(frame_esquerdo, label_text="🔥 MANTOS DISPONÍVEIS", label_text_color="#FFD700", height=160)
scroll_times.pack(fill="both", expand=True, padx=15, pady=5)

def selecionar_time(nome_time, btn_ref):
    global time_selecionado
    time_selecionado = nome_time
    label_selecionado.configure(text=f"Time Selecionado: {nome_time}", text_color="#00E676")

    for btn, _ in botoes_times_dados:
        btn.configure(fg_color="#D500F9", hover_color="#AA00FF", text="Selecionar")
    btn_ref.configure(fg_color="#00E676", hover_color="#00C853", text="Selecionado ✓", text_color="#000000")

def construir_catalogo():
    global cards_times_lista, botoes_times_dados
    for card, _ in cards_times_lista:
        card.destroy()
    cards_times_lista.clear()
    botoes_times_dados.clear()

    cursor.execute("SELECT id, nome, preco FROM produtos")
    for prod_id, nome_prod, preco in cursor.fetchall():
        nome_time = nome_prod.replace("Camisa ", "")
        info_time = times_dados.get(nome_time, {"icone": "🛡️", "cor": "#FF9800"})
        
        card = ctk.CTkFrame(scroll_times, corner_radius=10, fg_color="#1E1E2C")
        card.pack(fill="x", padx=5, pady=4)

        lbl_escudo = ctk.CTkLabel(card, text=info_time["icone"], font=ctk.CTkFont(size=22))
        lbl_escudo.pack(side="left", padx=(10, 5), pady=4)

        barra_cor = ctk.CTkFrame(card, width=4, height=24, fg_color=info_time["cor"])
        barra_cor.pack(side="left", padx=(0, 8))

        info_txt = f"{nome_time} — R$ {preco:.2f}".replace(".", ",")
        lbl_info = ctk.CTkLabel(card, text=info_txt, font=ctk.CTkFont(size=13, weight="bold"), text_color="#FFFFFF")
        lbl_info.pack(side="left", padx=2)

        btn = ctk.CTkButton(card, text="Selecionar", width=95, height=28, fg_color="#D500F9", hover_color="#AA00FF", font=ctk.CTkFont(weight="bold"))
        btn.configure(command=lambda t=nome_time, b=btn: selecionar_time(t, b))
        btn.pack(side="right", padx=8, pady=4)
        
        botoes_times_dados.append((btn, nome_time))
        cards_times_lista.append((card, nome_time))

construir_catalogo()

label_selecionado = ctk.CTkLabel(frame_esquerdo, text="Time selecionado: Nenhum", font=ctk.CTkFont(size=14, weight="bold"), text_color="#FF3D00")
label_selecionado.pack(anchor="w", padx=15, pady=2)

frame_opcoes = ctk.CTkFrame(frame_esquerdo, corner_radius=10, fg_color="#1E1E2C", border_width=1, border_color="#FFD700")
frame_opcoes.pack(fill="x", padx=15, pady=5)

box1 = ctk.CTkFrame(frame_opcoes, fg_color="transparent")
box1.pack(fill="x", padx=10, pady=4)

ctk.CTkLabel(box1, text="Tam:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 2))
combo_tamanho = ctk.CTkComboBox(box1, values=["PP", "P", "M", "G", "GG", "XG"], width=65, button_color="#FF9800")
combo_tamanho.set("M")
combo_tamanho.pack(side="left", padx=2)

ctk.CTkLabel(box1, text="Qtd:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(6, 2))
campo_quantidade = ctk.CTkEntry(box1, width=40)
campo_quantidade.insert(0, "1")
campo_quantidade.pack(side="left", padx=2)

var_brinde_item = ctk.BooleanVar(value=True)
chk_brinde_item = ctk.CTkCheckBox(box1, text="🎁 Brinde", variable=var_brinde_item, text_color="#FFD700", font=ctk.CTkFont(size=11, weight="bold"), checkbox_width=18, checkbox_height=18)
chk_brinde_item.pack(side="left", padx=(10, 0))

def ativar_personalizacao():
    if var_personalizar.get():
        campo_nome.configure(state="normal")
        campo_numero.configure(state="normal")
    else:
        campo_nome.delete(0, 'end')
        campo_numero.delete(0, 'end')
        campo_nome.configure(state="disabled")
        campo_numero.configure(state="disabled")

var_personalizar = ctk.BooleanVar(value=False)
chk_pers = ctk.CTkCheckBox(frame_opcoes, text="Personalizar (+R$ 20,00)", variable=var_personalizar, command=ativar_personalizacao, text_color="#FFD700", font=ctk.CTkFont(weight="bold"))
chk_pers.pack(anchor="w", padx=10, pady=4)

box2 = ctk.CTkFrame(frame_opcoes, fg_color="transparent")
box2.pack(fill="x", padx=10, pady=(0, 6))

campo_nome = ctk.CTkEntry(box2, placeholder_text="Nome na camisa", state="disabled", width=140)
campo_nome.pack(side="left", padx=(0, 5))

campo_numero = ctk.CTkEntry(box2, placeholder_text="N°", state="disabled", width=60)
campo_numero.pack(side="left")

def obter_taxa_entrega():
    regiao = combo_regiao.get()
    if "Capital" in regiao: return 15.00
    elif "Metropolitana" in regiao: return 30.00
    elif "Interior" in regiao: return 35.00
    return 15.00

def calcular_totais():
    subtotal = sum(item["subtotal"] for item in carrinho)
    entrega = obter_taxa_entrega() if carrinho else 0.00
    total = max(0.0, subtotal - desconto_aplicado + entrega)
    return subtotal, desconto_aplicado, entrega, total

def atualizar_total(event=None):
    sub, desc, ent, tot = calcular_totais()
    label_subtotal.configure(text=f"Subtotal: R$ {sub:.2f}".replace(".", ","))
    label_desconto.configure(text=f"Desconto: -R$ {desc:.2f}".replace(".", ","))
    label_entrega.configure(text=f"Taxa de Entrega: R$ {ent:.2f}".replace(".", ","))
    label_total.configure(text=f"TOTAL: R$ {tot:.2f}".replace(".", ","))

def atualizar_carrinho():
    for row in lista_carrinho.get_children():
        lista_carrinho.delete(row)

    for item in carrinho:
        pers_txt = f"{item['nome']} #{item['numero']}" if item["personalizado"] else "Não"
        lista_carrinho.insert("", "end", values=(
            item["produto"],
            item["tamanho"],
            pers_txt,
            item["quantidade"],
            item["brinde"],
            f"R$ {item['subtotal']:.2f}".replace(".", ",")
        ))
    atualizar_total()

def adicionar_carrinho():
    if time_selecionado is None:
        messagebox.showwarning("Aviso", "Selecione um time primeiro.")
        return

    try:
        qtd = int(campo_quantidade.get())
        if qtd <= 0: raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Digite uma quantidade válida.")
        return

    tamanho = combo_tamanho.get()
    brinde_escolhido = "Sim (Chaveiro/Adesivo)" if var_brinde_item.get() else "Não"
    coluna_estoque = f"estoque_{tamanho.lower()}"
    
    cursor.execute(f"SELECT {coluna_estoque}, preco FROM produtos WHERE nome = ?", ("Camisa " + time_selecionado,))
    res = cursor.fetchone()
    if not res:
        messagebox.showerror("Erro", "Produto não encontrado no banco de dados.")
        return
    
    estoque_atual, preco_unit = res
    if qtd > estoque_atual:
        messagebox.showwarning("Estoque Insuficiente", f"Apenas {estoque_atual} unidades disponíveis no tamanho {tamanho}!")
        return

    personalizado = var_personalizar.get()
    nome = campo_nome.get().strip()
    numero = campo_numero.get().strip()

    if personalizado:
        if not nome or not numero:
            messagebox.showwarning("Aviso", "Preencha o nome e o número para personalização.")
            return
        if not numero.isdigit():
            messagebox.showerror("Erro", "O número deve conter apenas dígitos!")
            return
        preco_unit += PRECO_PERSONALIZACAO

    subtotal = preco_unit * qtd

    carrinho.append({
        "produto": "Camisa " + time_selecionado,
        "tamanho": tamanho,
        "personalizado": personalizado,
        "nome": nome,
        "numero": numero,
        "quantidade": qtd,
        "brinde": brinde_escolhido,
        "subtotal": subtotal
    })
    atualizar_carrinho()

ctk.CTkButton(
    frame_esquerdo, 
    text="+ ADICIONAR AO CARRINHO", 
    font=ctk.CTkFont(size=14, weight="bold"), 
    fg_color="#FF6D00", 
    hover_color="#E65100", 
    height=34, 
    command=adicionar_carrinho
).pack(fill="x", padx=15, pady=(2, 10))

# Frame Direito - Carrinho e Checkout
frame_direito = ctk.CTkFrame(janela, corner_radius=15, border_width=2, border_color="#D500F9")
frame_direito.grid(row=0, column=1, padx=12, pady=(35, 12), sticky="nsew")

ctk.CTkLabel(frame_direito, text="🛒 CARRINHO DE COMPRAS", font=ctk.CTkFont(size=15, weight="bold"), text_color="#FFD700").pack(anchor="w", padx=15, pady=(8, 2))

tree_frame = ctk.CTkFrame(frame_direito)
tree_frame.pack(fill="both", expand=True, padx=15, pady=2)

lista_carrinho = ttk.Treeview(
    tree_frame,
    columns=("produto", "tamanho", "personalizado", "quantidade", "brinde", "subtotal"),
    show="headings",
    height=4
)

cols = {"produto": "Produto", "tamanho": "Tam", "personalizado": "Pers.", "quantidade": "Qtd", "brinde": "Brinde", "subtotal": "Subtotal"}
for c, t in cols.items():
    lista_carrinho.heading(c, text=t)

lista_carrinho.column("produto", width=110)
lista_carrinho.column("tamanho", width=35)
lista_carrinho.column("personalizado", width=65)
lista_carrinho.column("quantidade", width=35)
lista_carrinho.column("brinde", width=60)
lista_carrinho.column("subtotal", width=65)

lista_carrinho.pack(fill="both", expand=True)

def remover_item():
    selecionado = lista_carrinho.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um item para remover.")
        return
    idx = lista_carrinho.index(selecionado[0])
    carrinho.pop(idx)
    atualizar_carrinho()

ctk.CTkButton(frame_direito, text="✖ Remover Item", fg_color="#FF1744", hover_color="#D50000", font=ctk.CTkFont(weight="bold"), height=24, command=remover_item).pack(anchor="e", padx=15, pady=2)

# Área de Cupom
frame_cupom = ctk.CTkFrame(frame_direito, fg_color="transparent")
frame_cupom.pack(fill="x", padx=15, pady=2)

campo_cupom = ctk.CTkEntry(frame_cupom, placeholder_text="Cupom (ex: MANTO10)", width=150, height=26)
campo_cupom.pack(side="left", padx=(0, 4))

def aplicar_cupom():
    global desconto_aplicado, cupom_ativo
    codigo = campo_cupom.get().strip().upper()
    subtotal_atual = sum(item["subtotal"] for item in carrinho)
    
    if not carrinho:
        messagebox.showwarning("Aviso", "Adicione itens ao carrinho antes de aplicar o cupom.")
        return

    if codigo == "MANTO10":
        desconto_aplicado = subtotal_atual * 0.10
        cupom_ativo = "MANTO10 (10%)"
        messagebox.showinfo("Sucesso", "Cupom MANTO10 aplicado! 10% de desconto.")
    elif codigo == "PRIMEIRA":
        desconto_aplicado = 15.00
        cupom_ativo = "PRIMEIRA (R$ 15 OFF)"
        messagebox.showinfo("Sucesso", "Cupom PRIMEIRA aplicado! R$ 15,00 de desconto.")
    else:
        desconto_aplicado = 0.0
        cupom_ativo = ""
        messagebox.showerror("Erro", "Cupom inválido!")
    atualizar_total()

ctk.CTkButton(frame_cupom, text="Aplicar Cupom", fg_color="#651FFF", hover_color="#4527A0", height=26, width=110, font=ctk.CTkFont(weight="bold"), command=aplicar_cupom).pack(side="left")

label_subtotal = ctk.CTkLabel(frame_direito, text="Subtotal: R$ 0,00", font=ctk.CTkFont(size=12))
label_subtotal.pack(anchor="e", padx=15)

label_desconto = ctk.CTkLabel(frame_direito, text="Desconto: -R$ 0,00", font=ctk.CTkFont(size=12), text_color="#00E676")
label_desconto.pack(anchor="e", padx=15)

label_entrega = ctk.CTkLabel(frame_direito, text="Taxa de Entrega: R$ 0,00", font=ctk.CTkFont(size=12))
label_entrega.pack(anchor="e", padx=15)

label_total = ctk.CTkLabel(frame_direito, text="TOTAL: R$ 0,00", font=ctk.CTkFont(size=16, weight="bold"), text_color="#00E676")
label_total.pack(anchor="e", padx=15, pady=(0, 4))

# Formulário do Cliente
frame_cliente = ctk.CTkFrame(frame_direito, corner_radius=10, fg_color="#1E1E2C")
frame_cliente.pack(fill="x", padx=15, pady=2)

campo_cliente = ctk.CTkEntry(frame_cliente, placeholder_text="Nome Completo", height=28)
campo_cliente.pack(fill="x", padx=8, pady=(4, 2))

box_contato = ctk.CTkFrame(frame_cliente, fg_color="transparent")
box_contato.pack(fill="x", padx=8, pady=2)

campo_tel = ctk.CTkEntry(box_contato, placeholder_text="WhatsApp / Telefone", height=28)
campo_tel.pack(side="left", fill="x", expand=True, padx=(0, 4))

campo_cpf = ctk.CTkEntry(box_contato, placeholder_text="CPF (Nota Fiscal)", height=28, width=130)
campo_cpf.pack(side="left")

campo_endereco = ctk.CTkEntry(frame_cliente, placeholder_text="Endereço (Rua, Número, Bairro)", height=28)
campo_endereco.pack(fill="x", padx=8, pady=2)

box_frete = ctk.CTkFrame(frame_cliente, fg_color="transparent")
box_frete.pack(fill="x", padx=8, pady=2)

ctk.CTkLabel(box_frete, text="Região Frete:", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=(0, 4))
combo_regiao = ctk.CTkComboBox(box_frete, values=["Capital (R$ 15,00)", "Região Metropolitana (R$ 30,00)", "Interior (R$ 35,00)"], command=atualizar_total, height=26)
combo_regiao.set("Capital (R$ 15,00)")
combo_regiao.pack(side="left", fill="x", expand=True)

box_pag_banco = ctk.CTkFrame(frame_cliente, fg_color="transparent")
box_pag_banco.pack(fill="x", padx=8, pady=2)

ctk.CTkLabel(box_pag_banco, text="Pgto:", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=(0, 2))
combo_pagamento = ctk.CTkComboBox(box_pag_banco, values=["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"], button_color="#651FFF", height=26, width=115)
combo_pagamento.set("Pix")
combo_pagamento.pack(side="left", padx=(0, 6))

ctk.CTkLabel(box_pag_banco, text="Banco:", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=(0, 2))
combo_banco_cliente = ctk.CTkComboBox(box_pag_banco, values=["Nubank", "Itaú", "Bradesco", "Banco do Brasil", "Santander", "Caixa", "Inter"], button_color="#2979FF", height=26)
combo_banco_cliente.set("Nubank")
combo_banco_cliente.pack(side="left", fill="x", expand=True)

campo_obs = ctk.CTkEntry(frame_cliente, placeholder_text="Observações (ex: Deixar na portaria)", height=28)
campo_obs.pack(fill="x", padx=8, pady=(2, 6))

def gerar_cliente():
    nome = fake.name() if fake else "Cliente Automático"
    tel = fake.phone_number() if fake else "(11) 99999-9999"
    cpf = fake.cpf() if fake else "123.456.789-00"
    endereco_fake = fake.address() if fake else "Rua Exemplo, 123"
    campo_cliente.delete(0, 'end')
    campo_cliente.insert(0, nome)
    campo_tel.delete(0, 'end')
    campo_tel.insert(0, tel)
    campo_cpf.delete(0, 'end')
    campo_cpf.insert(0, cpf)
    campo_endereco.delete(0, 'end')
    campo_endereco.insert(0, endereco_fake.replace("\n", ", "))
    campo_obs.delete(0, 'end')
    campo_obs.insert(0, "Entregar com cuidado")

ctk.CTkButton(frame_cliente, text="⚡ Preencher Automático (Faker)", fg_color="#651FFF", hover_color="#4527A0", font=ctk.CTkFont(weight="bold"), height=24, command=gerar_cliente).pack(fill="x", padx=8, pady=(0, 4))

def finalizar_pedido():
    if not carrinho:
        messagebox.showwarning("Aviso", "O carrinho está vazio.")
        return

    cliente = campo_cliente.get().strip()
    telefone = campo_tel.get().strip()
    cpf = campo_cpf.get().strip()
    endereco = campo_endereco.get().strip()
    regiao = combo_regiao.get()
    obs = campo_obs.get().strip() or "Nenhuma"
    pagamento = combo_pagamento.get()
    banco = combo_banco_cliente.get()
    brinde = "Sim (Chaveiro/Adesivo)"

    if not cliente or not telefone or not endereco:
        messagebox.showwarning("Aviso", "Preencha o nome, telefone e endereço.")
        return

    subtotal, desconto, entrega, total = calcular_totais()
    detalhes = []
    
    # Baixa no estoque
    for item in carrinho:
        tamanho = item["tamanho"].lower()
        col_est = f"estoque_{tamanho}"
        prod_nome = item["produto"]
        
        cursor.execute(f"UPDATE produtos SET {col_est} = {col_est} - ? WHERE nome = ?", (item["quantidade"], prod_nome))
        
        desc = f"{item['quantidade']}x {item['produto']} ({item['tamanho']})"
        if item["personalizado"]:
            desc += f" [Pers: {item['nome']} N°{item['numero']}]"
        detalhes.append(desc)

    conexao.commit()
    construir_catalogo()

    detalhes_texto = " | ".join(detalhes)
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    previsao_data = (datetime.now() + timedelta(days=4)).strftime("%d/%m/%Y")
    rastreio = "NM" + str(random.randint(100000, 999999)) + "BR"
    status = "Aguardando Envio"

    # Salva no Banco de Dados
    with conexao:
        cursor.execute("""
            INSERT INTO pedidos (cliente, telefone, cpf, endereco, regiao, obs, detalhes, subtotal, desconto, taxa_entrega, total, data, previsao, rastreio, pagamento, banco, brinde, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (cliente, telefone, cpf, endereco, regiao, obs, detalhes_texto, subtotal, desconto, entrega, total, data, previsao_data, rastreio, pagamento, banco, brinde, status))

    carrinho.clear()
    global desconto_aplicado, cupom_ativo
    desconto_aplicado = 0.0
    cupom_ativo = ""
    atualizar_carrinho()
    campo_cliente.delete(0, 'end')
    campo_tel.delete(0, 'end')
    campo_cpf.delete(0, 'end')
    campo_endereco.delete(0, 'end')
    campo_obs.delete(0, 'end')

    messagebox.showinfo("Sucesso", f"✅ Pedido finalizado e gravado no Banco de Dados!\nBanco Registrado: {banco}\nRastreio: {rastreio}")

ctk.CTkButton(
    frame_direito, 
    text="FINALIZAR PEDIDO 🚀", 
    font=ctk.CTkFont(size=14, weight="bold"), 
    fg_color="#00E676", 
    hover_color="#00C853", 
    text_color="#000000",
    height=36, 
    command=finalizar_pedido
).pack(fill="x", padx=15, pady=(4, 6))

frame_botoes_gestao = ctk.CTkFrame(frame_direito, fg_color="transparent")
frame_botoes_gestao.pack(fill="x", padx=15, pady=(0, 10))

# =====================================================
# FUNÇÃO CORRIGIDA: GESTÃO DE ESTOQUE (ADMIN)
# =====================================================
def abrir_painel_admin():
    global win_admin
    
    if win_admin is not None and win_admin.winfo_exists():
        win_admin.lift()
        win_admin.focus_force()
        return

    win_admin = ctk.CTkToplevel(janela)
    win_admin.title("Gestão de Estoque e Produtos")
    win_admin.geometry("900x450")
    
    win_admin.lift()
    win_admin.focus_force()

    tabela = ttk.Treeview(win_admin, columns=("id", "nome", "preco", "pp", "p", "m", "g", "gg", "xg"), show="headings")
    colunas = {"id": "ID", "nome": "Produto", "preco": "Preço", "pp": "PP", "p": "P", "m": "M", "g": "G", "gg": "GG", "xg": "XG"}
    for c, t in colunas.items():
        tabela.heading(c, text=t)
        tabela.column(c, width=80 if c != "nome" else 180)
    tabela.pack(fill="both", expand=True, padx=10, pady=10)

    def carregar_dados_admin():
        for row in tabela.get_children():
            tabela.delete(row)
        cursor.execute("SELECT id, nome, preco, estoque_pp, estoque_p, estoque_m, estoque_g, estoque_gg, estoque_xg FROM produtos")
        for p in cursor.fetchall():
            tabela.insert("", "end", values=(p[0], p[1], f"R$ {p[2]:.2f}", p[3], p[4], p[5], p[6], p[7], p[8]))

    carregar_dados_admin()

    def alterar_preco():
        sel = tabela.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um produto.")
            return
        item = tabela.item(sel[0])
        prod_id = item["values"][0]
        
        top_preco = ctk.CTkToplevel(win_admin)
        top_preco.geometry("300x150")
        top_preco.title("Alterar Preço")
        top_preco.lift()
        top_preco.focus_force()
        
        ent = ctk.CTkEntry(top_preco, placeholder_text="Novo Preço (ex: 159.90)")
        ent.pack(padx=20, pady=20, fill="x")
        
        def salvar():
            try:
                novo_p = float(ent.get().replace(",", "."))
                with conexao:
                    cursor.execute("UPDATE produtos SET preco = ? WHERE id = ?", (novo_p, prod_id))
                carregar_dados_admin()
                construir_catalogo()
                top_preco.destroy()
                messagebox.showinfo("Sucesso", "Preço atualizado no Banco de Dados!")
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido.")

        ctk.CTkButton(top_preco, text="Salvar", command=salvar, fg_color="#00E676", text_color="#000000").pack(padx=20)

    ctk.CTkButton(win_admin, text="💰 Alterar Preço do Produto Selecionado", fg_color="#2979FF", command=alterar_preco).pack(pady=10)

# =====================================================
# FUNÇÃO CORRIGIDA: HISTÓRICO DE PEDIDOS
# =====================================================
def mostrar_historico():
    global win_historico

    if win_historico is not None and win_historico.winfo_exists():
        win_historico.lift()
        win_historico.focus_force()
        return

    win_historico = ctk.CTkToplevel(janela)
    win_historico.title("Histórico de Pedidos e Recibos")
    win_historico.geometry("1150x480")

    win_historico.lift()
    win_historico.focus_force()

    tabela = ttk.Treeview(
        win_historico,
        columns=("id", "cliente", "telefone", "total", "pagamento", "banco", "data", "status"),
        show="headings"
    )
    colunas_hist = {
        "id": "ID", 
        "cliente": "Cliente", 
        "telefone": "Telefone", 
        "total": "Total", 
        "pagamento": "Pgto", 
        "banco": "Banco",
        "data": "Data",
        "status": "Status"
    }
    
    for c, t in colunas_hist.items():
        tabela.heading(c, text=t)
        tabela.column(c, width=110 if c in ["cliente", "data"] else 80)
        
    tabela.pack(fill="both", expand=True, padx=10, pady=10)

    def carregar_pedidos():
        for row in tabela.get_children():
            tabela.delete(row)
        cursor.execute("SELECT id, cliente, telefone, total, pagamento, banco, data, status FROM pedidos ORDER BY id DESC")
        for p in cursor.fetchall():
            tabela.insert("", "end", values=(p[0], p[1], p[2], f"R$ {p[3]:.2f}", p[4], p[5], p[6], p[7]))

    carregar_pedidos()

    def ver_detalhes_pedido():
        sel = tabela.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um pedido na lista.")
            return
        pedido_id = tabela.item(sel[0])["values"][0]
        
        cursor.execute("SELECT * FROM pedidos WHERE id = ?", (pedido_id,))
        p = cursor.fetchone()
        
        if p:
            info = f"""
📄 RECIBO DE PEDIDO #{p[0]}
----------------------------------------
Cliente: {p[1]}
CPF: {p[3]}
Telefone: {p[2]}
Endereço: {p[4]} ({p[5]})
----------------------------------------
Itens: {p[7]}
Observações: {p[6]}
----------------------------------------
Subtotal: R$ {p[8]:.2f}
Desconto: R$ {p[9]:.2f}
Frete: R$ {p[10]:.2f}
TOTAL: R$ {p[11]:.2f}
----------------------------------------
Forma de Pgto: {p[15]}
Banco: {p[16]}
Brinde: {p[17]}
Rastreio: {p[14]} | Previsão: {p[13]}
Status: {p[18]}
            """
            top_recibo = ctk.CTkToplevel(win_historico)
            top_recibo.title(f"Recibo #{pedido_id}")
            top_recibo.geometry("450x550")
            top_recibo.lift()
            top_recibo.focus_force()
            
            txt = ctk.CTkTextbox(top_recibo, font=ctk.CTkFont(family="Consolas", size=12))
            txt.pack(fill="both", expand=True, padx=10, pady=10)
            txt.insert("1.0", info)

    btn_frame = ctk.CTkFrame(win_historico, fg_color="transparent")
    btn_frame.pack(fill="x", padx=10, pady=(0, 10))

    ctk.CTkButton(btn_frame, text="🔍 Ver Detalhes / Recibo", fg_color="#2979FF", command=ver_detalhes_pedido).pack(side="left", padx=5)

ctk.CTkButton(frame_botoes_gestao, text="📦 Estoque (Admin)", fg_color="#2979FF", hover_color="#1565C0", font=ctk.CTkFont(weight="bold"), height=28, command=abrir_painel_admin).pack(side="left", fill="x", expand=True, padx=(0, 2))
ctk.CTkButton(frame_botoes_gestao, text="📋 Histórico", fg_color="#651FFF", hover_color="#4527A0", font=ctk.CTkFont(weight="bold"), height=28, command=mostrar_historico).pack(side="left", fill="x", expand=True, padx=(2, 0))

# Inicialização do loop principal
janela.mainloop()