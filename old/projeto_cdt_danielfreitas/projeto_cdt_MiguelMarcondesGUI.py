import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog

ARQUIVO_BANCO = "agendamentos.json"

SERVICOS = {
    "1": ("Degradê", 35),
    "2": ("Corte social", 30),
    "3": ("Barba completa", 25),
    "4": ("Pigmentação", 40),
    "5": ("Hidratação capilar", 50),
    "6": ("Platinado", 120),
    "7": ("Combo corte + barba", 50)
}

HORARIOS_PADRAO = ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:30"]

# --- PALETA DE CORES ANIME RETRÔ (ANOS 80/90) ---
COR_FUNDO = "#0a0a12"        # Azul escuro quase preto (vibe céu de anime clássico)
COR_CONTAINER = "#16162a"    # Container escuro contrastante
COR_TEXTO = "#ffffff"        # Texto branco limpo
COR_NEON = "#00ff66"         # Verde Neon / Ciano Cyberpunk para destaques
COR_BOTAO_PADRAO = "#1f1f3a" # Fundo dos botões normais
COR_IMPORTAR = "#2e7d32"     # Verde escuro para o botão de importar limpo
COR_ALERTA = "#ff0055"       # Vermelho Neon para Sair/Cancelar

# Cores estilo "preencha aqui" para os inputs
COR_INPUT_FUNDO = "#0f0f1c"  # Mais escuro que o container para dar profundidade
COR_INPUT_TEXTO = "#a0a0b0"  # Texto ligeiramente acinzentado (indica campo a preencher)

FONTE_TITULO = ("Courier New", 20, "bold")
FONTE_SUBTITULO = ("Courier New", 11, "bold")
FONTE_GERAL = ("Courier New", 10, "bold")

def carregar_agendamentos():
    if not os.path.exists(ARQUIVO_BANCO):
        with open(ARQUIVO_BANCO, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo)
    with open(ARQUIVO_BANCO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

def salvar_agendamentos(lista_agendamentos):
    with open(ARQUIVO_BANCO, "w", encoding="utf-8") as arquivo:
        json.dump(lista_agendamentos, arquivo, indent=4, ensure_ascii=False)

def obter_horarios_disponiveis(data_selecionada):
    agendamentos = carregar_agendamentos()
    horarios_ocupados = [
        a["horario"] for a in agendamentos if a["data"] == data_selecionada
    ]
    return [h for h in HORARIOS_PADRAO if h not in horarios_ocupados]


class BarbeariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Barbearia Andrades // SYSTEM v1.0")
        self.root.geometry("450x580") #
        self.root.configure(bg=COR_FUNDO)
        
        # Estilização das Comboboxes (Menus de escolha)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "TCombobox", 
            fieldbackground=COR_INPUT_FUNDO, 
            background=COR_BOTAO_PADRAO, 
            foreground=COR_TEXTO,
            arrowcolor=COR_NEON
        )
        # Customiza a lista interna que cai da Combobox
        self.root.option_add("*TCombobox*Listbox.background", COR_INPUT_FUNDO)
        self.root.option_add("*TCombobox*Listbox.foreground", COR_INPUT_TEXTO)
        self.root.option_add("*TCombobox*Listbox.selectBackground", COR_BOTAO_PADRAO)
        self.root.option_add("*TCombobox*Listbox.selectForeground", COR_NEON)

        self.mostrar_menu_principal()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def criar_cabecalho(self, titulo):
        header = tk.Frame(self.root, bg=COR_FUNDO, pady=10)
        header.pack(fill="x")
        
        lbl_titulo = tk.Label(header, text=f"// {titulo.upper()} //", font=FONTE_TITULO, fg=COR_NEON, bg=COR_FUNDO)
        lbl_titulo.pack()
        
        linha = tk.Frame(self.root, height=2, bg=COR_NEON)
        linha.pack(fill="x", padx=20, pady=5)

    def criar_botao_voltar(self):
        btn_voltar = tk.Button(
            self.root, text="<< VOLTAR AO MENU", font=FONTE_SUBTITULO, 
            bg=COR_CONTAINER, fg=COR_TEXTO, activebackground=COR_NEON, 
            activeforeground=COR_FUNDO, bd=2, relief="solid", highlightbackground=COR_NEON,
            padx=15, pady=8, cursor="hand2", command=self.mostrar_menu_principal
        )
        btn_voltar.pack(side="bottom", pady=20)

    def mostrar_menu_principal(self):
        self.root.geometry("450x580") #
        self.limpar_tela()
        
        lbl_welcome = tk.Label(self.root, text="Barbearia Andrades", font=FONTE_TITULO, fg=COR_NEON, bg=COR_FUNDO, pady=15)
        lbl_welcome.pack()
        
        lbl_sub = tk.Label(self.root, text="--- SELECIONE UMA OPÇÃO DO SISTEMA ---", font=FONTE_SUBTITULO, fg=COR_TEXTO, bg=COR_FUNDO)
        lbl_sub.pack(pady=5)

        menu_frame = tk.Frame(self.root, bg=COR_CONTAINER, bd=2, relief="solid", highlightbackground=COR_NEON, padx=30, pady=15)
        menu_frame.pack(pady=10)

        botoes = [
            ("🎃 AGENDAR HORÁRIO", self.tela_agendar),
            ("❌ CANCELAR AGENDAMENTO", self.tela_cancelar),
            ("👁‍🗨 VER AGENDAMENTOS", self.tela_listar),
            ("💲 SERVIÇOS E PREÇOS", self.tela_servicos),
            ("📍 LOCALIZAÇÃO E CONTATO", self.tela_contato),
        ]

        for texto, comando in botoes:
            btn = tk.Button(
                menu_frame, text=texto, font=FONTE_SUBTITULO, 
                bg=COR_BOTAO_PADRAO, fg=COR_TEXTO, activebackground=COR_NEON, 
                activeforeground=COR_FUNDO, bd=2, relief="solid", 
                width=28, height=2, cursor="hand2", command=comando
            )
            btn.pack(pady=6)
            
        btn_importar = tk.Button(
            menu_frame, 
            text="Importar Agendamento JSON", 
            font=FONTE_SUBTITULO, 
            bg=COR_IMPORTAR, 
            fg=COR_TEXTO, 
            activebackground=COR_NEON, 
            activeforeground=COR_FUNDO, 
            bd=2, 
            relief="solid", 
            width=28, 
            height=2, 
            cursor="hand2", 
            command=self.importar_de_json
        )
        btn_importar.pack(pady=6)
            
        btn_sair = tk.Button(
            self.root, 
            text="[ SAIR DO SISTEMA ]", 
            font=FONTE_SUBTITULO, 
            bg=COR_ALERTA,               
            fg=COR_TEXTO, 
            activebackground=COR_TEXTO, 
            activeforeground=COR_ALERTA,
            bd=2, 
            relief="solid",
            width=28, 
            pady=10, 
            cursor="hand2", 
            command=self.root.quit
        )
        btn_sair.pack(side="bottom", pady=15)

    def importar_de_json(self):
        caminho_arquivo = filedialog.askopenfilename(
            filetypes=[("Arquivos JSON", "*.json")]
        )
        if caminho_arquivo:
            try:
                with open(caminho_arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                
                if all(k in dados for k in ("nome", "servico", "data", "horario")):
                    lista = carregar_agendamentos()
                    
                    conflito = any(a["data"] == dados["data"] and a["horario"] == dados["horario"] for a in lista)
                    if conflito:
                        messagebox.showerror("SISTEMA // ERRO", f"O horário {dados['horario']} no dia {dados['data']} já está ocupado!")
                        return
                        
                    lista.append(dados)
                    salvar_agendamentos(lista)
                    messagebox.showinfo("SISTEMA // SUCESSO", f"Agendamento de {dados['nome']} importado com sucesso!")
                else:
                    messagebox.showerror("SISTEMA // ERRO", "Formato de arquivo JSON inválido.")
            except Exception as e:
                messagebox.showerror("SISTEMA // ERRO", f"Falha crítica ao ler arquivo: {e}")

    def tela_agendar(self):
        self.limpar_tela()
        self.criar_cabecalho("Novo Agendamento")

        form_frame = tk.Frame(self.root, bg=COR_CONTAINER, bd=2, relief="solid", padx=20, pady=20)
        form_frame.pack(pady=10, fill="both", expand=True, padx=40)

        # Campo Nome (Efeito escurecido de "preencha aqui")
        tk.Label(form_frame, text="NOME DO CLIENTE:", font=FONTE_GERAL, fg=COR_NEON, bg=COR_CONTAINER).grid(row=0, column=0, sticky="w", pady=8)
        ent_nome = tk.Entry(form_frame, font=FONTE_GERAL, bg=COR_INPUT_FUNDO, fg=COR_TEXTO, insertbackground=COR_NEON, bd=2, relief="solid")
        ent_nome.grid(row=0, column=1, sticky="ew", pady=8, padx=10)

        tk.Label(form_frame, text="SERVIÇO DESEJADO:", font=FONTE_GERAL, fg=COR_NEON, bg=COR_CONTAINER).grid(row=1, column=0, sticky="w", pady=8)
        
        lista_servicos_texto = [f"{nome} (R$ {preco})" for cod, (nome, preco) in SERVICOS.items()]
        cb_servico = ttk.Combobox(form_frame, values=lista_servicos_texto, state="readonly", font=FONTE_GERAL)
        cb_servico.grid(row=1, column=1, sticky="ew", pady=8, padx=10)
        cb_servico.current(0)

        tk.Label(form_frame, text="DATA (DD/MM/AAAA):", font=FONTE_GERAL, fg=COR_NEON, bg=COR_CONTAINER).grid(row=2, column=0, sticky="w", pady=8)
        ent_data = tk.Entry(form_frame, font=FONTE_GERAL, bg=COR_INPUT_FUNDO, fg=COR_TEXTO, insertbackground=COR_NEON, bd=2, relief="solid")
        ent_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        ent_data.grid(row=2, column=1, sticky="ew", pady=8, padx=10)

        tk.Label(form_frame, text="HORÁRIO:", font=FONTE_GERAL, fg=COR_NEON, bg=COR_CONTAINER).grid(row=3, column=0, sticky="w", pady=8)
        cb_horario = ttk.Combobox(form_frame, state="readonly", font=FONTE_GERAL)
        cb_horario.grid(row=3, column=1, sticky="ew", pady=8, padx=10)

        def atualizar_horarios(*args):
            data_str = ent_data.get().strip()
            try:
                data_validada = datetime.strptime(data_str, "%d/%m/%Y")
                if data_validada.date() >= datetime.now().date():
                    vagos = obter_horarios_disponiveis(data_str)
                    cb_horario['values'] = vagos
                    if vagos:
                        cb_horario.current(0)
                    else:
                        cb_horario['values'] = ["NENHUM HORÁRIO VAGO"]
                        cb_horario.current(0)
                else:
                    cb_horario['values'] = ["DATA RETROATIVA"]
                    cb_horario.current(0)
            except ValueError:
                cb_horario['values'] = ["AGUARDANDO DATA VÁLIDA..."]
                cb_horario.current(0)

        ent_data.bind("<KeyRelease>", atualizar_horarios)
        atualizar_horarios()

        form_frame.columnconfigure(1, weight=1)

        def confirmar_agendamento():
            nome = ent_nome.get().strip()
            servico_escolhido = cb_servico.get()
            data_str = ent_data.get().strip()
            horario = cb_horario.get()

            if not nome:
                messagebox.showerror("SISTEMA // ERRO", "Por favor, digite seu nome.")
                return

            try:
                data_validada = datetime.strptime(data_str, "%d/%m/%Y")
                if data_validada.date() < datetime.now().date():
                    messagebox.showerror("SISTEMA // ERRO", "Não é possível agendar em datas passadas.")
                    return
            except ValueError:
                messagebox.showerror("SISTEMA // ERRO", "Formato de data inválido. Use DD/MM/AAAA.")
                return

            if horario in ["NENHUM HORÁRIO VAGO", "DATA RETROATIVA", "AGUARDANDO DATA VÁLIDA...", ""]:
                messagebox.showerror("SISTEMA // ERRO", "Por favor, selecione um horário válido.")
                return

            nome_servico = servico_escolhido.split(" (")[0]

            novo_agendamento = {
                "nome": nome,
                "servico": nome_servico,
                "data": data_str,
                "horario": horario
            }

            lista = carregar_agendamentos()
            lista.append(novo_agendamento)
            salvar_agendamentos(lista)

            messagebox.showinfo("SISTEMA // SUCESSO", f"Agendamento confirmado para {nome} às {horario}!")
            self.mostrar_menu_principal()

        btn_confirmar = tk.Button(
            form_frame, text="CONFIRMAR AGENDAMENTO", font=FONTE_SUBTITULO, 
            bg=COR_NEON, fg=COR_FUNDO, activebackground=COR_FUNDO, 
            activeforeground=COR_NEON, bd=2, relief="solid", pady=10, 
            cursor="hand2", command=confirmar_agendamento
        )
        btn_confirmar.grid(row=4, column=0, columnspan=2, pady=20, sticky="ew", padx=10)

        self.criar_botao_voltar()

    def tela_cancelar(self):
        self.limpar_tela()
        self.criar_cabecalho("Cancelar Agendamento")

        cancel_frame = tk.Frame(self.root, bg=COR_CONTAINER, bd=2, relief="solid", padx=20, pady=20)
        cancel_frame.pack(pady=20, padx=40, fill="x")

        tk.Label(cancel_frame, text="DIGITE O NOME DO CLIENTE PARA CANCELAR:", font=FONTE_GERAL, fg=COR_TEXTO, bg=COR_CONTAINER).pack(pady=5)
        ent_nome = tk.Entry(cancel_frame, font=FONTE_SUBTITULO, bg=COR_INPUT_FUNDO, fg=COR_TEXTO, insertbackground=COR_NEON, bd=2, relief="solid")
        ent_nome.pack(pady=8, fill="x", padx=20)

        def acao_cancelar():
            nome = ent_nome.get().strip()
            if not nome:
                messagebox.showerror("SISTEMA // ERRO", "Digite um nome para buscar.")
                return

            lista = carregar_agendamentos()
            novo_banco = [a for a in lista if a["nome"].lower() != nome.lower()]

            if len(lista) == len(novo_banco):
                messagebox.showwarning("SISTEMA // AVISO", "Nenhum agendamento encontrado com esse nome.")
            else:
                salvar_agendamentos(novo_banco)
                messagebox.showinfo("SISTEMA // SUCESSO", "Agendamento cancelado com sucesso!")
                self.mostrar_menu_principal()

        btn_cancelar = tk.Button(
            cancel_frame, text="REMOVER REGISTRO", font=FONTE_SUBTITULO, 
            bg=COR_ALERTA, fg=COR_TEXTO, activebackground=COR_TEXTO, 
            activeforeground=COR_ALERTA, bd=2, relief="solid", pady=8, 
            cursor="hand2", command=acao_cancelar
        )
        btn_cancelar.pack(pady=15)

        self.criar_botao_voltar()

    def exportar_para_json(self, dados_agendamento):
        nome_sugerido = f"comprovante_{dados_agendamento['nome'].replace(' ', '_')}.json"
        
        caminho_arquivo = filedialog.asksaveasfilename(
            initialfile=nome_sugerido,
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json")]
        )
        
        if caminho_arquivo:
            try:
                with open(caminho_arquivo, "w", encoding="utf-8") as f:
                    json.dump(dados_agendamento, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("SISTEMA // SUCESSO", "Comprovante exportado com sucesso!")
            except Exception as e:
                messagebox.showerror("SISTEMA // ERRO", f"Não foi possível salvar o arquivo: {e}")

    def tela_listar(self):
        self.root.geometry("740x640")
        self.limpar_tela()
        self.criar_cabecalho("Registros do Sistema")

        canvas = tk.Canvas(self.root, bg=COR_FUNDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COR_FUNDO)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")

        lista = carregar_agendamentos()

        if not lista:
            lbl_vazio = tk.Label(scroll_frame, text="// BANCO DE DADOS VAZIO //", font=FONTE_SUBTITULO, fg=COR_ALERTA, bg=COR_FUNDO)
            lbl_vazio.pack(pady=50, padx=180)
        else:
            for agendamento in lista:
                card = tk.Frame(scroll_frame, bg=COR_CONTAINER, padx=15, pady=10, bd=2, relief="solid")
                card.pack(fill="x", pady=6, padx=10)
                
                texto_card = f"CLIENTE: {agendamento['nome'].upper()}\nSERVIÇO: {agendamento['servico'].upper()}\nDATA/HORA: {agendamento['data']} - {agendamento['horario']}"
                lbl_info = tk.Label(card, text=texto_card, font=FONTE_GERAL, justify="left", fg=COR_TEXTO, bg=COR_CONTAINER)
                lbl_info.pack(side="left", anchor="w", pady=5)
                
                btn_exportar = tk.Button(
                    card, 
                    text="EXPORTAR JSON", 
                    font=FONTE_GERAL, 
                    bg=COR_BOTAO_PADRAO, 
                    fg=COR_NEON,
                    activebackground=COR_NEON,
                    activeforeground=COR_FUNDO,
                    bd=1,
                    relief="solid",
                    padx=12,
                    pady=6,
                    cursor="hand2",
                    command=lambda a=agendamento: self.exportar_para_json(a)
                )
                btn_exportar.pack(side="right", padx=10, pady=5, anchor="center")

        self.criar_botao_voltar()

    def tela_servicos(self):
        self.limpar_tela()
        self.criar_cabecalho("Data de Preços")

        tabela_frame = tk.Frame(self.root, bg=COR_CONTAINER, bd=2, relief="solid", padx=20, pady=20)
        tabela_frame.pack(pady=20, padx=40, fill="both", expand=True)

        for cod, (nome, preco) in SERVICOS.items():
            row_frame = tk.Frame(tabela_frame, bg=COR_CONTAINER)
            row_frame.pack(fill="x", pady=6)
            
            lbl_nome = tk.Label(row_frame, text=f"> {nome.upper()}", font=FONTE_GERAL, fg=COR_TEXTO, bg=COR_CONTAINER)
            lbl_nome.pack(side="left")
            
            lbl_preco = tk.Label(row_frame, text=f"R$ {preco:.2f}", font=FONTE_GERAL, fg=COR_NEON, bg=COR_CONTAINER)
            lbl_preco.pack(side="right")
            
            div = tk.Frame(tabela_frame, height=1, bg=COR_BOTAO_PADRAO)
            div.pack(fill="x", pady=4)

        self.criar_botao_voltar()

    def tela_contato(self):
        self.limpar_tela()
        self.criar_cabecalho("Terminais de Contato")

        info_frame = tk.Frame(self.root, bg=COR_CONTAINER, bd=2, relief="solid", padx=30, pady=30)
        info_frame.pack(pady=40, padx=50, fill="x")

        txt_contato = (
            "[ LOCALIZAÇÃO ]\n"
            "Jardim Macedônia - Rua Póva de Varzim - Nº67\n\n"
            "[ COMUNICAÇÃO ]\n"
            "TEL / WHATSAPP: +55 11 91539-7314\n\n"
            "[ CRONOGRAMA ]\n"
            "Terça a Sábado: 09:00 às 18:30"
        )

        lbl_info = tk.Label(info_frame, text=txt_contato, font=FONTE_GERAL, justify="left", fg=COR_TEXTO, bg=COR_CONTAINER, wraplength=450)
        lbl_info.pack(anchor="w")

        self.criar_botao_voltar()


if __name__ == "__main__":
    root = tk.Tk()
    app = BarbeariaApp(root)
    root.mainloop()