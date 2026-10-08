import os
import sys
import subprocess
import json
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# ============================================================
# INTEGRAÇÃO COM RECONHECIMENTO FACIAL E MÓDULOS
# ============================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from src.camera import reconhecer_cliente
except ImportError:
    def reconhecer_cliente():
        return {"status": "novo_cliente"}

DB_NAME = 'acaiteria.db'

def cadastrar_cliente_db(nome, telefone, cpf):
    """Garante o registo básico de um cliente caso necessário."""
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                cpf TEXT
            );
        """)
        cursor.execute("INSERT INTO clientes (nome, telefone, cpf) VALUES (?, ?, ?);", (nome, telefone, cpf))
        conexao.commit()
    except Exception as e:
        print(f"[ERRO BD] {e}")
    finally:
        conexao.close()

def obter_todos_pedidos():
    """Busca todos os pedidos registados para o painel do administrador."""
    if not os.path.exists(DB_NAME):
        return []
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    pedidos = []
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pedidos';")
        if cursor.fetchone():
            cursor.execute("SELECT * FROM pedidos;")
            pedidos = cursor.fetchall()
    except Exception as e:
        print(f"[ERRO BD] {e}")
    finally:
        conexao.close()
    return pedidos

def exportar_banco_para_json(caminho_destino="backup_delirio_roxo.json"):
    """Exporta todas as tabelas do SQLite para um ficheiro JSON."""
    if not os.path.exists(DB_NAME):
        return False, "Base de dados não encontrada."
    conexao = sqlite3.connect(DB_NAME)
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    dados_completos = {}
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = cursor.fetchall()
        for tabela in tabelas:
            nome_tabela = tabela['name']
            cursor.execute(f"SELECT * FROM {nome_tabela};")
            linhas = cursor.fetchall()
            dados_completos[nome_tabela] = [dict(linha) for linha in linhas]
        with open(caminho_destino, 'w', encoding='utf-8') as f:
            json.dump(dados_completos, f, ensure_ascii=False, indent=4)
        return True, caminho_destino
    except Exception as e:
        return False, str(e)
    finally:
        conexao.close()

# ============================================================
# CONFIGURAÇÕES E CORES (PADRÃO DELÍRIO ROXO)
# ============================================================
LARGURA = 1200
ALTURA = 700

ROXO_ESCURO = "#17062F"
ROXO = "#3A126B"
ROXO_MEDIO = "#5A1B91"
ROSA = "#E91E83"
ROSA_CLARO = "#F52B91"
AMARELO = "#FFD21C"
BRANCO = "#FFFFFF"
CINZA = "#B9AFC8"
VERDE = "#42A62A"

cliente_logado = None
carrinho = []
logo_cardapio = None

janela = tk.Tk()
janela.title("Delírio Roxo - Sistema PDV com Biometria e Gestão")
janela.geometry(f"{LARGURA}x{ALTURA}")
janela.minsize(1000, 600)
janela.configure(bg=ROXO_ESCURO)

def limpar_conteudo():
    for widget in area_conteudo.winfo_children():
        widget.destroy()

def mascarar_dado(texto, visiveis=3):
    if not texto or texto == "-":
        return "-"
    if len(texto) <= visiveis:
        return "*" * len(texto)
    return "*" * (len(texto) - visiveis) + texto[-visiveis:]

def atualizar_painel_direito():
    for widget in painel_direito.winfo_children():
        widget.destroy()

    titulo = tk.Label(painel_direito, text="👤 Painel do Cliente", font=("Arial", 11, "bold"), fg=BRANCO, bg="#21103D")
    titulo.pack(pady=(15, 10))

    if cliente_logado:
        info_frame = tk.Frame(painel_direito, bg="#261044", highlightbackground=ROXO_MEDIO, highlightthickness=1)
        info_frame.pack(fill="x", padx=15, pady=5)

        nome = cliente_logado.get("nome", "Cliente")
        cpf_m = mascarar_dado(cliente_logado.get("cpf", ""), visiveis=3)
        tel_m = mascarar_dado(cliente_logado.get("telefone", ""), visiveis=4)
        pontos = cliente_logado.get("pontos", 120)

        tk.Label(info_frame, text=f"Olá, {nome}!", font=("Arial", 10, "bold"), fg=AMARELO, bg="#261044").pack(anchor="w", padx=10, pady=(8, 2))
        tk.Label(info_frame, text=f"CPF: ***.***.{cpf_m}", font=("Arial", 8), fg=BRANCO, bg="#261044").pack(anchor="w", padx=10)
        tk.Label(info_frame, text=f"Tel: (**) *****-{tel_m}", font=("Arial", 8), fg=BRANCO, bg="#261044").pack(anchor="w", padx=10)
        tk.Label(info_frame, text=f"Pontos: {pontos} pts 💜", font=("Arial", 9, "bold"), fg=ROSA_CLARO, bg="#261044").pack(anchor="w", padx=10, pady=(2, 8))

        btn_sair = tk.Button(
            painel_direito, text="Sair da Conta", font=("Arial", 9, "bold"), bg=ROSA, fg=BRANCO,
            relief="flat", cursor="hand2", command=deslogar_cliente
        )
        btn_sair.pack(fill="x", padx=15, pady=5)
    else:
        lbl_msg = tk.Label(painel_direito, text="Olá!\nFaça seu reconhecimento\nou cadastro para ter uma\nexperiência especial!", font=("Arial", 9), fg=CINZA, bg="#21103D", justify="center")
        lbl_msg.pack(pady=5)

        btn_login = tk.Button(
            painel_direito, text="🔑 Entrar na Conta", font=("Arial", 9, "bold"), bg=ROXO_MEDIO, fg=BRANCO,
            relief="flat", cursor="hand2", command=abrir_modal_login
        )
        btn_login.pack(fill="x", padx=15, pady=3)

        btn_cad = tk.Button(
            painel_direito, text="👤 Cadastrar Cliente", font=("Arial", 10, "bold"), bg=AMARELO, fg="#3B2600",
            activebackground="#FFE45C", relief="flat", cursor="hand2", command=abrir_modal_cadastro
        )
        btn_cad.pack(fill="x", padx=15, pady=3)

    tk.Label(painel_direito, text="♻ Últimos Pedidos / Carrinho", font=("Arial", 10, "bold"), fg=VERDE, bg="#21103D").pack(anchor="w", padx=15, pady=(15, 5))

    frame_pedidos = tk.Frame(painel_direito, bg="#261044", highlightbackground=ROXO_MEDIO, highlightthickness=1)
    frame_pedidos.pack(fill="x", padx=15)

    if carrinho:
        total_carrinho = sum(item['preco'] for item in carrinho)
        for item in carrinho[-3:]:
            tk.Label(frame_pedidos, text=f"• {item['nome']} (R$ {item['preco']:.2f})", font=("Arial", 8), fg=BRANCO, bg="#261044", anchor="w").pack(fill="x", padx=8, pady=2)
        
        tk.Label(frame_pedidos, text=f"Subtotal: R$ {total_carrinho:.2f}", font=("Arial", 9, "bold"), fg=AMARELO, bg="#261044").pack(pady=5)
        
        btn_checkout = tk.Button(
            frame_pedidos, text="🛒 Finalizar Pedido", font=("Arial", 9, "bold"), bg=VERDE, fg=BRANCO,
            relief="flat", cursor="hand2", command=mostrar_checkout
        )
        btn_checkout.pack(fill="x", padx=10, pady=5)
    else:
        tk.Label(frame_pedidos, text="🥣", font=("Arial", 25), fg=BRANCO, bg="#261044").pack(pady=(12, 3))
        tk.Label(frame_pedidos, text="Nenhum pedido encontrado", font=("Arial", 9, "bold"), fg=BRANCO, bg="#261044").pack()
        tk.Label(frame_pedidos, text="Ainda não há pedidos registrados.", font=("Arial", 8), fg=CINZA, bg="#261044").pack(pady=(3, 12))

def deslogar_cliente():
    global cliente_logado
    cliente_logado = None
    atualizar_painel_direito()
    messagebox.showinfo("Delírio Roxo", "Você saiu da sua conta.")

# ============================================================
# MODAL DE LOGIN / ACESSO ADMINISTRATIVO
# ============================================================
def abrir_modal_login():
    win = tk.Toplevel(janela)
    win.title("Entrar na Conta / Admin")
    win.geometry("380x280")
    win.configure(bg=ROXO_ESCURO)

    tk.Label(win, text="Login / Acesso Administrativo", font=("Arial", 13, "bold"), fg=BRANCO, bg=ROXO_ESCURO).pack(pady=15)
    tk.Label(win, text="Digite seu CPF ou 'admin' para Gestão:", font=("Arial", 9), fg=CINZA, bg=ROXO_ESCURO).pack(anchor="w", padx=25)
    ent_dado = tk.Entry(win, font=("Arial", 11))
    ent_dado.pack(fill="x", padx=25, pady=5)

    def efetuar_login():
        global cliente_logado
        dado = ent_dado.get().strip()
        if not dado:
            messagebox.showwarning("Atenção", "Preencha o campo de login.")
            return
            
        # Acesso de Administrador
        if dado.lower() == "admin" or dado == "000.000.000-00":
            win.destroy()
            abrir_painel_administrativo()
            return
            
        cliente_logado = {"id": 1, "nome": "Cliente Delírio", "cpf": dado, "telefone": dado, "pontos": 150}
        atualizar_painel_direito()
        win.destroy()
        messagebox.showinfo("Sucesso", "Login efetuado com sucesso!")

    tk.Button(win, text="Entrar", font=("Arial", 10, "bold"), bg=ROSA, fg=BRANCO, command=efetuar_login).pack(pady=15, ipadx=10)

def abrir_painel_administrativo():
    """Painel exclusivo de gestão do Administrador."""
    admin_win = tk.Toplevel(janela)
    admin_win.title("Delírio Roxo - Painel do Administrador")
    admin_win.geometry("620x480")
    admin_win.configure(bg=ROXO_ESCURO)

    tk.Label(admin_win, text="🛠️ Painel de Controlo Administrativo", font=("Arial", 15, "bold"), fg=AMARELO, bg=ROXO_ESCURO).pack(pady=15)

    frame_acoes = tk.Frame(admin_win, bg="#21103D", highlightbackground=ROXO_MEDIO, highlightthickness=1)
    frame_acoes.pack(fill="x", padx=25, pady=10)

    def acao_exportar():
        sucesso, resultado = exportar_banco_para_json("backup_delirio_roxo.json")
        if sucesso:
            messagebox.showinfo("Exportação Concluída", f"Base de dados exportada para:\n{os.path.abspath(resultado)}")
        else:
            messagebox.showerror("Erro", f"Falha ao exportar: {resultado}")

    tk.Button(frame_acoes, text="📥 Exportar Base de Dados (JSON)", font=("Arial", 10, "bold"), bg=VERDE, fg=BRANCO, command=acao_exportar).pack(side="left", padx=15, pady=15)

    tk.Label(admin_win, text="📋 Histórico de Pedidos Registados:", font=("Arial", 11, "bold"), fg=BRANCO, bg=ROXO_ESCURO).pack(anchor="w", padx=25, pady=(10, 5))
    
    txt_pedidos = tk.Text(admin_win, height=12, width=68, bg="#261044", fg=BRANCO, font=("Courier", 9))
    txt_pedidos.pack(padx=25, pady=5)

    pedidos = obter_todos_pedidos()
    if pedidos:
        for p in pedidos:
            txt_pedidos.insert(tk.END, f"{str(p)}\n" + "-"*50 + "\n")
    else:
        txt_pedidos.insert(tk.END, "Nenhum pedido registado na base de dados até ao momento.")
    
    txt_pedidos.config(state="disabled")
    tk.Button(admin_win, text="Fechar Painel Admin", font=("Arial", 10), bg="#757575", fg=BRANCO, command=admin_win.destroy).pack(pady=10)

def abrir_modal_cadastro():
    win = tk.Toplevel(janela)
    win.title("Cadastro de Cliente")
    win.geometry("350x320")
    win.configure(bg=ROXO_ESCURO)

    tk.Label(win, text="Novo Cadastro", font=("Arial", 14, "bold"), fg=BRANCO, bg=ROXO_ESCURO).pack(pady=10)
    tk.Label(win, text="Nome Completo:", font=("Arial", 9), fg=CINZA, bg=ROXO_ESCURO).pack(anchor="w", padx=25)
    ent_nome = tk.Entry(win)
    ent_nome.pack(fill="x", padx=25, pady=2)

    tk.Label(win, text="CPF:", font=("Arial", 9), fg=CINZA, bg=ROXO_ESCURO).pack(anchor="w", padx=25)
    ent_cpf = tk.Entry(win)
    ent_cpf.pack(fill="x", padx=25, pady=2)

    tk.Label(win, text="Telefone:", font=("Arial", 9), fg=CINZA, bg=ROXO_ESCURO).pack(anchor="w", padx=25)
    ent_tel = tk.Entry(win)
    ent_tel.pack(fill="x", padx=25, pady=2)

    def salvar():
        global cliente_logado
        if not ent_nome.get() or not ent_cpf.get():
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios.")
            return
        cadastrar_cliente_db(ent_nome.get(), ent_tel.get(), ent_cpf.get())
        cliente_logado = {"id": 1, "nome": ent_nome.get(), "cpf": ent_cpf.get(), "telefone": ent_tel.get(), "pontos": 50}
        atualizar_painel_direito()
        win.destroy()
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")

    tk.Button(win, text="Cadastrar Cliente", font=("Arial", 10, "bold"), bg=AMARELO, fg="#3B2600", command=salvar).pack(pady=15)

# ============================================================
# TELA INICIAL COM RECONHECIMENTO FACIAL INTEGRADO
# ============================================================
def mostrar_inicio():
    limpar_conteudo()

    titulo = tk.Label(area_conteudo, text="Bem-vindo ao Delírio Roxo!", font=("Arial", 24, "bold"), fg=BRANCO, bg=ROXO_ESCURO)
    titulo.pack(pady=(35, 10))

    subtitulo = tk.Label(area_conteudo, text="Mais que açaí, uma energia pra você!", font=("Arial", 12), fg=CINZA, bg=ROXO_ESCURO)
    subtitulo.pack()

    caixa = tk.Frame(area_conteudo, bg="#21103D", highlightbackground=ROXO_MEDIO, highlightthickness=1)
    caixa.pack(fill="both", expand=True, padx=35, pady=30)

    icone = tk.Label(caixa, text="◉", font=("Arial", 50), fg="#BBA8CC", bg="#21103D")
    icone.pack(pady=(15, 2))

    texto = tk.Label(caixa, text="Posicione seu rosto\nna câmera para continuar", font=("Arial", 13, "bold"), fg=BRANCO, bg="#21103D", justify="center")
    texto.pack()

    def acionar_biometria_facial():
        global cliente_logado
        print("[PDV] A acionar câmara para reconhecimento facial...")
        
        resultado = reconhecer_cliente()
        
        if not resultado:
            return

        status = resultado.get("status")

        if status == "encontrado":
            nome = resultado.get('nome', 'Cliente')
            acai = resultado.get('acai_preferido', 'Tradicional')
            
            cliente_logado = {
                "id": resultado.get('id', 1),
                "nome": nome,
                "cpf": "123.456.789-00",
                "telefone": "(11) 98888-8888",
                "pontos": 150,
                "acai_preferido": acai
            }
            atualizar_painel_direito()
            messagebox.showinfo("Delírio Roxo", f"Bem-vindo de volta, {nome}!\nAçaí favorito: {acai}")
            mostrar_cardapio()
            
        elif status == "novo_cliente":
            resposta = messagebox.askyesno("Novo Cliente", "Rosto não reconhecido. Deseja abrir a tela de cadastro biométrico?")
            if resposta:
                try:
                    caminho_cadastro = os.path.abspath("reconhecimento_facial_cadastro-GUI.py")
                    if not os.path.exists(caminho_cadastro):
                        caminho_cadastro = "reconhecimento_facial_cadastro-GUI.py"
                    subprocess.run([sys.executable, caminho_cadastro], check=True)
                    messagebox.showinfo("Sucesso", "Cadastro concluído! Pressione o botão de reconhecimento novamente.")
                except Exception as e:
                    print(f"[ERRO] Falha ao abrir o cadastro: {e}")

    btn_biometria = tk.Button(
        caixa, text="📷 Iniciar Reconhecimento Facial", font=("Arial", 11, "bold"),
        bg=ROSA, fg=BRANCO, activebackground=ROSA_CLARO, relief="flat", cursor="hand2",
        command=acionar_biometria_facial
    )
    btn_biometria.pack(pady=12, ipadx=15, ipady=6)

    linha = tk.Frame(caixa, bg=AMARELO, height=2, width=100)
    linha.pack(pady=5)

    dica = tk.Label(caixa, text="Ou escolha uma opção no menu ao lado.", font=("Arial", 9), fg=CINZA, bg="#21103D")
    dica.pack(pady=(0, 15))

def mostrar_cardapio():
    global logo_cardapio
    limpar_conteudo()

    try:
        caminho_logo = os.path.join(os.path.dirname(__file__), "..", "logo_acai.jpeg")
        if os.path.exists(caminho_logo):
            imagem_logo = Image.open(caminho_logo)
            imagem_logo = imagem_logo.resize((180, 100))
            logo_cardapio = ImageTk.PhotoImage(imagem_logo)
            label_logo = tk.Label(area_conteudo, image=logo_cardapio, bg=ROXO_ESCURO)
            label_logo.image = logo_cardapio
            label_logo.pack(pady=(15, 5))
    except Exception as e:
        print(f"Aviso Imagem: {e}")

    tk.Label(area_conteudo, text="🥣 Cardápio", font=("Arial", 24, "bold"), fg=BRANCO, bg=ROXO_ESCURO).pack(pady=5)

    aba_parent = ttk.Notebook(area_conteudo)
    aba_parent.pack(fill="both", expand=True, padx=10, pady=5)

    tab_custom = tk.Frame(aba_parent, bg="#21103D")
    aba_parent.add(tab_custom, text=" 🛠 Monte o Seu ")

    tk.Label(tab_custom, text="Escolha o Tamanho:", font=("Arial", 11, "bold"), fg=AMARELO, bg="#21103D").pack(anchor="w", padx=20, pady=(10, 2))
    var_tamanho = tk.StringVar(value="300ml - R$ 15,00")
    tamanhos = [("300ml - R$ 15,00", 15.0), ("500ml - R$ 20,00", 20.0), ("700ml - R$ 25,00", 25.0)]
    for text, price in tamanhos:
        tk.Radiobutton(tab_custom, text=text, variable=var_tamanho, value=text, bg="#21103D", fg=BRANCO, selectcolor=ROXO_MEDIO, activebackground="#21103D").pack(anchor="w", padx=35)

    def add_custom():
        tam_str = var_tamanho.get()
        preco_base = float(tam_str.split("R$ ")[1].replace(",", "."))
        item = {"nome": f"Açaí Custom ({tam_str.split(' -')[0]})", "detalhes": "Personalizado", "preco": preco_base}
        carrinho.append(item)
        atualizar_painel_direito()
        messagebox.showinfo("Delírio Roxo", "Açaí adicionado ao pedido!")

    tk.Button(tab_custom, text="Adicionar Personalizado", font=("Arial", 10, "bold"), bg=ROSA, fg=BRANCO, command=add_custom).pack(pady=15)

def mostrar_delirio_roxo():
    limpar_conteudo()
    tk.Label(area_conteudo, text="💜 Delírio Roxo (Fidelidade)", font=("Arial", 24, "bold"), fg=BRANCO, bg=ROXO_ESCURO).pack(pady=20)

def mostrar_configuracoes():
    limpar_conteudo()
    tk.Label(area_conteudo, text="⚙ Configurações", font=("Arial", 22, "bold"), fg=BRANCO, bg=ROXO_ESCURO).pack(pady=20)
    tk.Button(area_conteudo, text="🚪 Sair do Sistema", bg=ROSA, fg=BRANCO, command=janela.destroy).pack(pady=10)

def mostrar_checkout():
    limpar_conteudo()
    tk.Label(area_conteudo, text="🛒 Finalizar Pedido", font=("Arial", 22, "bold"), fg=BRANCO, bg=ROXO_ESCURO).pack(pady=20)
    def finalizar():
        carrinho.clear()
        atualizar_painel_direito()
        messagebox.showinfo("Sucesso", "Pedido finalizado com sucesso!")
        mostrar_inicio()
    tk.Button(area_conteudo, text="Confirmar Pedido", bg=VERDE, fg=BRANCO, command=finalizar).pack(pady=20)

# ============================================================
# CABEÇALHO E MENU LATERAL
# ============================================================
cabecalho = tk.Frame(janela, bg="#3A075C", height=105)
cabecalho.pack(side="top", fill="x")
cabecalho.pack_propagate(False)

tk.Label(cabecalho, text="Delírio Roxo", font=("Arial", 28, "bold"), fg=BRANCO, bg="#3A075C").pack(side="left", padx=35)

corpo = tk.Frame(janela, bg=ROXO_ESCURO)
corpo.pack(fill="both", expand=True)

menu_lateral = tk.Frame(corpo, bg="#21103D", width=220)
menu_lateral.pack(side="left", fill="y", padx=(10, 5), pady=10)
menu_lateral.pack_propagate(False)

tk.Button(menu_lateral, text="🏠   Início", bg=ROSA, fg=BRANCO, relief="flat", command=mostrar_inicio).pack(fill="x", padx=10, pady=7, ipady=8)
tk.Button(menu_lateral, text="🥣   Cardápio", bg="#32134F", fg=BRANCO, relief="flat", command=mostrar_cardapio).pack(fill="x", padx=10, pady=7, ipady=8)
tk.Button(menu_lateral, text="💜   Delírio Roxo", bg="#32134F", fg=BRANCO, relief="flat", command=mostrar_delirio_roxo).pack(fill="x", padx=10, pady=7, ipady=8)
tk.Button(menu_lateral, text="⚙   Configurações", bg="#32134F", fg=BRANCO, relief="flat", command=mostrar_configuracoes).pack(fill="x", padx=10, pady=7, ipady=8)

area_conteudo = tk.Frame(corpo, bg=ROXO_ESCURO)
area_conteudo.pack(side="left", fill="both", expand=True, padx=5, pady=10)

painel_direito = tk.Frame(corpo, bg="#21103D", width=290)
painel_direito.pack(side="right", fill="y", padx=(5, 10), pady=10)
painel_direito.pack_propagate(False)

if __name__ == "__main__":
    atualizar_painel_direito()
    mostrar_inicio()
    janela.mainloop()