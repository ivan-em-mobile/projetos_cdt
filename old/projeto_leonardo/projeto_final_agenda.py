import json
import sqlite3
import hashlib
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

TEXTOS = {
    "Português": {
        "titulo": "Sistema de Clientes",
        "login_titulo": "Acesso ao Sistema",
        "usuario": "Usuário",
        "senha": "Senha",
        "entrar": "Entrar",
        "tentativas": "Tentativas restantes: ",
        "aba_cadastro": "Cadastro",
        "aba_clientes": "Clientes",
        "aba_config": "Configurações",
        "nome_cliente": "Nome do Cliente",
        "placeholder_nome": "Ex: João Silva",
        "selecione_plano": "Selecione o Plano",
        "salvar_cliente": "Salvar Cliente",
        "total_clientes": "Total: {} cliente(s)",
        "exportar": "Exportar JSON",
        "excluir": "Excluir Selecionado",
        "config_titulo": "Customização do Sistema",
        "seletor_idioma": "Idioma do Sistema",
        "seletor_cor": "Cor Principal do Tema",
        "aviso_nome": "Digite o nome do cliente.",
        "sucesso_cadastro": "Cliente cadastrado com sucesso!",
        "sucesso_excluir": "Cliente removido do banco de dados.",
        "sucesso_exportar": "Dados exportados para: {}",
        "erro_login": "Senha incorreta",
        "bloqueado": "Número de tentativas excedido. Sistema encerrado.",
        "placeholder_senha": "Digite sua senha",
        "alterar_senha_titulo": "Alterar Senha do Administrador",
        "senha_atual": "Senha Atual",
        "nova_senha": "Nova Senha",
        "btn_alterar_senha": "Atualizar Senha",
        "erro_senha_atual": "A senha atual digitada está incorreta.",
        "erro_senha_vazia": "Os campos de senha não podem estar vazios.",
        "sucesso_senha": "Senha alterada com sucesso!",
        "plano_Gratuito": "Gratuito",
        "plano_Básico": "Básico",
        "plano_Premium": "Premium",
        "cor_Azul": "Azul",
        "cor_Verde": "Verde",
        "cor_Roxo": "Roxo"
    },
    "English": {
        "titulo": "Client System",
        "login_titulo": "System Access",
        "usuario": "Username",
        "senha": "Password",
        "entrar": "Login",
        "tentativas": "Attempts left: ",
        "aba_cadastro": "Register",
        "aba_clientes": "Clients",
        "aba_config": "Settings",
        "nome_cliente": "Client Name",
        "placeholder_nome": "E.g., John Doe",
        "selecione_plano": "Select a Plan",
        "salvar_cliente": "Save Client",
        "total_clientes": "Total: {} client(s)",
        "exportar": "Export JSON",
        "excluir": "Delete Selected",
        "config_titulo": "System Customization",
        "seletor_idioma": "System Language",
        "seletor_cor": "Main Theme Color",
        "aviso_nome": "Please enter the client's name.",
        "sucesso_cadastro": "Client registered successfully!",
        "sucesso_excluir": "Client removed from database.",
        "sucesso_exportar": "Data exported to: {}",
        "erro_login": "Incorrect password",
        "bloqueado": "No attempts left. System closed.",
        "placeholder_senha": "Enter your password",
        "alterar_senha_titulo": "Change Administrator Password",
        "senha_atual": "Current Password",
        "nova_senha": "New Password",
        "btn_alterar_senha": "Update Password",
        "erro_senha_atual": "The current password entered is incorrect.",
        "erro_senha_vazia": "Password fields cannot be empty.",
        "sucesso_senha": "Password changed successfully!",
        "plano_Gratuito": "Free",
        "plano_Básico": "Basic",
        "plano_Premium": "Premium",
        "cor_Azul": "Blue",
        "cor_Verde": "Green",
        "cor_Roxo": "Purple"
    }
}

PLANOS = {
    "Gratuito": "R$ 0,00",
    "Básico": "R$ 4,99",
    "Premium": "R$ 9,99"
}

MAPA_CORES = {
    "Azul": "#1A73E8",
    "Verde": "#2EA44F",
    "Roxo": "#8A3FFC"
}

MAPA_CORES_HOVER = {
    "Azul": "#1557B0",
    "Verde": "#227A3A",
    "Roxo": "#6929C4"
}

def conectar():
    return sqlite3.connect("sistema.db")

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def inicializar_banco():
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                plano TEXT NOT NULL,
                valor TEXT NOT NULL,
                horario TEXT NOT NULL
            )
        """)
        cursor.execute("CREATE TABLE IF NOT EXISTS configuracoes (chave TEXT PRIMARY KEY, valor TEXT NOT NULL)")
        cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('senha', ?)", (criptografar_senha("123456"),))
        
        cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('idioma', 'Português')")
        cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('cor_tema', 'Azul')")
        conexao.commit()

def obter_senha():
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT valor FROM configuracoes WHERE chave = 'senha'")
        res = cursor.fetchone()
        return res[0] if res else None

def obter_configuracao(chave, valor_padrao):
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT valor FROM configuracoes WHERE chave = ?", (chave,))
        res = cursor.fetchone()
        valor = res[0] if res else valor_padrao
        traducoes_antigas = {"Blue": "Azul", "Green": "Verde", "Purple": "Roxo"}
        return traducoes_antigas.get(valor, valor)

class SistemaApp:
    def __init__(self, root):
        self.root = root
        
        inicializar_banco()

        self.idioma_atual = obter_configuracao('idioma', 'Português')
        self.cor_atual = obter_configuracao('cor_tema', 'Azul')
        
        self.root.title(TEXTOS[self.idioma_atual]["titulo"])
        self.root.geometry("750x550")
        self.root.resizable(False, False)
        
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")
        
        self.tentativas = 5
        self.tela_login()

    def t(self, chave):
        return TEXTOS[self.idioma_atual].get(chave, "")

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def tela_login(self):
        self.limpar_tela()

        frame = ctk.CTkFrame(self.root, width=380, height=320, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text=self.t("login_titulo"), font=("Arial Bold", 20), text_color=MAPA_CORES[self.cor_atual]).pack(pady=(20, 10))

        ctk.CTkLabel(frame, text=self.t("usuario"), font=("Arial", 12)).pack(anchor="w", padx=40)
        self.ent_usuario = ctk.CTkEntry(frame, width=300)
        self.ent_usuario.pack(pady=5)
        self.ent_usuario.insert(0, "admin")

        ctk.CTkLabel(frame, text=self.t("senha"), font=("Arial", 12)).pack(anchor="w", padx=40)
        self.ent_senha = ctk.CTkEntry(frame, width=300, show="*", placeholder_text=self.t("placeholder_senha"))
        self.ent_senha.pack(pady=5)

        self.lbl_tentativas = ctk.CTkLabel(frame, text=f"{self.t('tentativas')}{self.tentativas}", text_color="gray")
        self.lbl_tentativas.pack(pady=5)

        btn_entrar = ctk.CTkButton(
            frame, text=self.t("entrar"), width=300, 
            fg_color=MAPA_CORES[self.cor_atual], 
            hover_color=MAPA_CORES_HOVER[self.cor_atual], 
            font=("Arial Bold", 14), command=self.validar_login
        )
        btn_entrar.pack(pady=(10, 20))

    def validar_login(self):
        usuario = self.ent_usuario.get()
        senha = self.ent_senha.get()

        if not usuario:
            messagebox.showwarning("Aviso", "Digite o usuário")
            return

        if criptografar_senha(senha) == obter_senha():
            self.painel_principal()
        else:
            self.tentativas -= 1
            self.lbl_tentativas.configure(text=f"{self.t('tentativas')}{self.tentativas}")
            messagebox.showerror("Erro", self.t("erro_login"))
            self.ent_senha.delete(0, 'end')

            if self.tentativas == 0:
                messagebox.showerror("Bloqueado", self.t("bloqueado"))
                self.root.quit()

    def painel_principal(self):
        self.limpar_tela()
        self.root.title(self.t("titulo"))

        # Criação de Abas
        self.abas = ctk.CTkTabview(
            self.root, width=720, height=520, corner_radius=12, 
            segmented_button_selected_color=MAPA_CORES[self.cor_atual]
        )
        self.abas.pack(padx=15, pady=15, fill="both", expand=True)

        self.aba_cadastro = self.abas.add(self.t("aba_cadastro"))
        self.aba_lista = self.abas.add(self.t("aba_clientes"))
        self.aba_config = self.abas.add(self.t("aba_config"))

        self.montar_cadastro()
        self.montar_lista()
        self.montar_config()

    def montar_cadastro(self):
        card = ctk.CTkFrame(self.aba_cadastro, fg_color="transparent")
        card.pack(pady=30, padx=50, fill="both", expand=True)

        ctk.CTkLabel(card, text=self.t("nome_cliente"), font=("Arial Bold", 14)).pack(anchor="w", pady=(0, 5))
        self.ent_nome = ctk.CTkEntry(card, width=400, placeholder_text=self.t("placeholder_nome"), height=35)
        self.ent_nome.pack(anchor="w", pady=(0, 20))

        ctk.CTkLabel(card, text=self.t("selecione_plano"), font=("Arial Bold", 14)).pack(anchor="w", pady=(0, 10))
        
        self.var_plano = ctk.StringVar(value="Gratuito")
        cores_planos = {"Gratuito": "#2EA44F", "Básico": "#1A73E8", "Premium": "#8A3FFC"}

        for plano, valor in PLANOS.items():
            texto_plano_traduzido = self.t(f"plano_{plano}")
            rb = ctk.CTkRadioButton(
                card, text=f"{texto_plano_traduzido} — {valor}", variable=self.var_plano, value=plano,
                font=("Arial", 13), hover_color=cores_planos[plano], fg_color=cores_planos[plano]
            )
            rb.pack(anchor="w", pady=6)

        btn_salvar = ctk.CTkButton(
            card, text=self.t("salvar_cliente"), 
            fg_color=MAPA_CORES[self.cor_atual],
            hover_color=MAPA_CORES_HOVER[self.cor_atual],
            font=("Arial Bold", 14), height=40, command=self.salvar_cliente
        )
        btn_salvar.pack(fill="x", pady=(40, 0))

    def salvar_cliente(self):
        nome = self.ent_nome.get().strip()
        plano = self.var_plano.get()

        if not nome:
            messagebox.showwarning("Aviso", self.t("aviso_nome"))
            return

        valor = PLANOS[plano]
        horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO clientes (nome, plano, valor, horario) VALUES (?, ?, ?, ?)", (nome, plano, valor, horario))
            conexao.commit()

        messagebox.showinfo("Sucesso", self.t("sucesso_cadastro"))
        self.ent_nome.delete(0, 'end')
        self.atualizar_tabela()

    def montar_lista(self):
        frame_topo = ctk.CTkFrame(self.aba_lista, fg_color="transparent")
        frame_topo.pack(fill="x", pady=(5, 15))

        self.lbl_total = ctk.CTkLabel(frame_topo, text="", font=("Arial Bold", 14))
        self.lbl_total.pack(side="left", padx=5)

        btn_exportar = ctk.CTkButton(
            frame_topo, text=self.t("exportar"), 
            fg_color=MAPA_CORES[self.cor_atual], 
            hover_color=MAPA_CORES_HOVER[self.cor_atual],
            width=120, command=self.exportar_json
        )
        btn_exportar.pack(side="right", padx=5)

        btn_excluir = ctk.CTkButton(frame_topo, text=self.t("excluir"), fg_color="#D93025", hover_color="#B31412", width=140, command=self.excluir_cliente)
        btn_excluir.pack(side="right", padx=5)

        self.container_lista = ctk.CTkScrollableFrame(self.aba_lista, width=650, height=350, fg_color="#F1F3F4")
        self.container_lista.pack(fill="both", expand=True)

        self.atualizar_tabela()

    def atualizar_tabela(self):
        for widget in self.container_lista.winfo_children():
            widget.destroy()

        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, plano, valor, horario FROM clientes")
            clientes = cursor.fetchall()

        self.lbl_total.configure(text=self.t("total_clientes").format(len(clientes)))
        cor_plano = {"Gratuito": "#2EA44F", "Básico": "#1A73E8", "Premium": "#8A3FFC"}

        self.selecionado_id = None
        self.cards_dict = {}

        for cli in clientes:
            id_cli, nome, plano, valor, data = cli
            
            card_cliente = ctk.CTkFrame(self.container_lista, height=70, fg_color="white", corner_radius=8, border_width=1, border_color="#E0E0E0")
            card_cliente.pack(fill="x", pady=5, padx=5)
            card_cliente.pack_propagate(False)

            faixa = ctk.CTkFrame(card_cliente, width=6, fg_color=cor_plano.get(plano, "gray"), corner_radius=0)
            faixa.pack(side="left", fill="y")

            info_frame = ctk.CTkFrame(card_cliente, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=8)

            lbl_nome = ctk.CTkLabel(info_frame, text=nome, font=("Arial Bold", 14), text_color="#202124")
            lbl_nome.pack(anchor="w")
            
            plano_traduzido = self.t(f"plano_{plano}")
            lbl_info = ctk.CTkLabel(info_frame, text=f"{plano_traduzido} • {valor} • {data}", font=("Arial", 11), text_color="#5F6368")
            lbl_info.pack(anchor="w")

            def marcar_selecionado(event, cid=id_cli, item_frame=card_cliente):
                for c in self.cards_dict.values():
                    c.configure(border_color="#E0E0E0", fg_color="white")
                item_frame.configure(border_color=MAPA_CORES[self.cor_atual], fg_color="#E8F0FE")
                self.selecionado_id = cid

            card_cliente.bind("<Button-1>", marcar_selecionado)
            faixa.bind("<Button-1>", marcar_selecionado)
            info_frame.bind("<Button-1>", marcar_selecionado)
            lbl_nome.bind("<Button-1>", marcar_selecionado)
            lbl_info.bind("<Button-1>", marcar_selecionado)

            self.cards_dict[id_cli] = card_cliente

    def excluir_cliente(self):
        if not hasattr(self, 'selecionado_id') or self.selecionado_id is None:
            return

        if messagebox.askyesno("Confirmar", "Deseja excluir?"):
            with conectar() as conexao:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM clientes WHERE id = ?", (self.selecionado_id,))
                conexao.commit()
            self.selecionado_id = None
            self.atualizar_tabela()

    def exportar_json(self):
        with conectar() as conexao:
            conexao.row_factory = sqlite3.Row
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, plano, valor, horario FROM clientes")
            dados = cursor.fetchall()

        if not dados: return
        lista = [dict(item) for item in dados]
        nome_arquivo = f"clientes_{datetime.now().strftime('%d%m%Y_%H%M%S')}.json"

        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(lista, arquivo, indent=4, ensure_ascii=False)

        messagebox.showinfo("Sucesso", self.t("sucesso_exportar").format(nome_arquivo))

    def montar_config(self):
        frame = ctk.CTkFrame(self.aba_config, corner_radius=12)
        frame.pack(fill="both", expand=True, pady=20, padx=20)

        # Container Esquerdo
        frame_esquerdo = ctk.CTkFrame(frame, fg_color="transparent")
        frame_esquerdo.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame_esquerdo, text=self.t("config_titulo"), font=("Arial Bold", 16), text_color=MAPA_CORES[self.cor_atual]).pack(anchor="w", pady=(0, 20))

        # 1. Seletor de Idioma
        ctk.CTkLabel(frame_esquerdo, text=self.t("seletor_idioma"), font=("Arial Bold", 13)).pack(anchor="w", pady=(10, 5))
        self.combo_idioma = ctk.CTkComboBox(frame_esquerdo, values=["Português", "English"], width=250, command=self.alterar_idioma)
        self.combo_idioma.set(self.idioma_atual)
        self.combo_idioma.pack(anchor="w", pady=(0, 20))

        # 2. Seletor de Cores do Tema
        ctk.CTkLabel(frame_esquerdo, text=self.t("seletor_cor"), font=("Arial Bold", 13)).pack(anchor="w", pady=(10, 5))
        opcoes_cores_visiveis = [self.t(f"cor_{cor}") for cor in MAPA_CORES.keys()]
        
        self.combo_cor = ctk.CTkComboBox(frame_esquerdo, values=opcoes_cores_visiveis, width=250, command=self.alterar_cor_tema)
        self.combo_cor.set(self.t(f"cor_{self.cor_atual}"))
        self.combo_cor.pack(anchor="w", pady=(0, 20))

        # Container Direito
        frame_direito = ctk.CTkFrame(frame, fg_color="transparent")
        frame_direito.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame_direito, text=self.t("alterar_senha_titulo"), font=("Arial Bold", 16), text_color=MAPA_CORES[self.cor_atual]).pack(anchor="w", pady=(0, 20))

        ctk.CTkLabel(frame_direito, text=self.t("senha_atual"), font=("Arial Bold", 13)).pack(anchor="w", pady=(10, 5))
        self.ent_senha_atual = ctk.CTkEntry(frame_direito, width=250, show="*")
        self.ent_senha_atual.pack(anchor="w", pady=(0, 15))

        ctk.CTkLabel(frame_direito, text=self.t("nova_senha"), font=("Arial Bold", 13)).pack(anchor="w", pady=(10, 5))
        self.ent_nova_senha = ctk.CTkEntry(frame_direito, width=250, show="*")
        self.ent_nova_senha.pack(anchor="w", pady=(0, 20))

        btn_alterar = ctk.CTkButton(
            frame_direito, text=self.t("btn_alterar_senha"), width=250,
            fg_color=MAPA_CORES[self.cor_atual], 
            hover_color=MAPA_CORES_HOVER[self.cor_atual],
            font=("Arial Bold", 13), command=self.atualizar_senha
        )
        btn_alterar.pack(anchor="w")

    def atualizar_senha(self):
        senha_atual = self.ent_senha_atual.get()
        nova_senha = self.ent_nova_senha.get()

        if not senha_atual or not nova_senha:
            messagebox.showwarning("Aviso", self.t("erro_senha_vazia"))
            return

        if criptografar_senha(senha_atual) != obter_senha():
            messagebox.showerror("Erro", self.t("erro_senha_atual"))
            return

        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("UPDATE configuracoes SET valor = ? WHERE chave = 'senha'", (criptografar_senha(nova_senha),))
            conexao.commit()

        messagebox.showinfo("Sucesso", self.t("sucesso_senha"))
        self.ent_senha_atual.delete(0, 'end')
        self.ent_nova_senha.delete(0, 'end')

    def alterar_idioma(self, novo_idioma):
        self.idioma_atual = novo_idioma
        
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("UPDATE configuracoes SET valor = ? WHERE chave = 'idioma'", (novo_idioma,))
            conexao.commit()
            
        self.painel_principal()
        self.abas.set(self.t("aba_config"))

    def alterar_cor_tema(self, nome_cor_escolhido):
        for cor_chave in MAPA_CORES.keys():
            if self.t(f"cor_{cor_chave}") == nome_cor_escolhido:
                self.cor_atual = cor_chave
                break
                
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("UPDATE configuracoes SET valor = ? WHERE chave = 'cor_tema'", (self.cor_atual,))
            conexao.commit()
            
        self.painel_principal()
        self.abas.set(self.t("aba_config"))


if __name__ == "__main__":
    root = ctk.CTk()
    app = SistemaApp(root)
    root.mainloop()