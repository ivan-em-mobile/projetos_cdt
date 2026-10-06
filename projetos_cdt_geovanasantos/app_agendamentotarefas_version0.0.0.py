import json
import tkinter as tk
from datetime import date, timedelta
from tkinter import messagebox, ttk

# ================= CONFIGURAÇÃO INICIAL =================

ROOT_USER = "root"
ROOT_PASS = "root"

ARQUIVO_AGENDAMENTOS = "agendamentos.json"
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_PROFISSIONAIS = "profissionais.json"
ARQUIVO_SERVICOS = "servicos.json"

SERVICOS = [
    "Encanador", "Eletricista", "Pintor", "Pedreiro", "Marceneiro", "Mecânico",
    "Chaveiro", "Informática", "Faxineiro", "Jardineiro", "Vidraceiro",
    "Ar-condicionado", "Celular", "Televisão", "Geladeira", "Máquina de lavar",
    "Internet", "Manicure", "Cabeleireiro", "Barbeiro", "Maquiadora", "Esteticista",
    "Massagista", "Professor particular", "Professor de inglês", "Professor de matemática",
    "Professor de música", "Personal trainer", "Fotógrafo", "Editor de vídeo",
    "Desenvolvedor de sites", "Designer gráfico", "Social media", "Contador", "Advogado",
    "Arquiteto", "Engenheiro", "Corretor de imóveis", "Veterinário", "Adestrador",
    "Passeador de cães", "Cuidador de idosos", "Babá", "DJ", "Organizador de festas",
    "Decorador", "Buffet", "Garçom", "Cerimonialista", "Motorista", "Entregador",
    "Guincho", "Borracheiro", "Lava-rápido", "Funileiro", "Pintor automotivo",
    "Eletricista automotivo", "Montador de móveis", "Instalador de câmeras",
    "Energia solar", "Técnico de impressora", "Técnico de computador", "Tradutor",
    "Redator", "Digitador", "Marketing", "Designer de interiores", "Fotógrafo de eventos",
    "Técnico de som", "Instalador de alarmes", "Costureira", "Sapateiro", "Piscineiro",
    "Serralheiro", "Técnico de gás", "Tapeceiro", "Calheiro", "Desentupidora",
    "Dedetizador", "Cuidador de animais", "Professor de dança", "Professor de reforço",
    "Micro-ondas", "Limpeza de sofá", "Limpeza de piscina", "Limpeza pós-obra",
    "Impermeabilização", "Instalador de cortinas", "Montador de cozinha",
    "Montador de TV", "Instalador de energia", "Outro problema"
]

NOMES = [
    "João", "Ana", "Carlos", "Marcos", "Julia", "Lucas", "Beatriz", "Rafael",
    "Gabriela", "Pedro", "Larissa", "Matheus", "Camila", "Felipe", "Amanda",
    "Diego", "Isabela", "Bruno", "Mariana", "Gustavo"
]

HORARIOS = ["08:00", "10:00", "13:00", "15:00", "17:00", "19:00"]

PROFISSIONAIS_INICIAIS = []
for i, servico in enumerate(SERVICOS):
  for j in range(10):
    PROFISSIONAIS_INICIAIS.append({
        "nome": f"{NOMES[(i+j)%len(NOMES)]} {j+1}",
        "servico": servico,
        "preco": 70 + ((i * 19 + j * 17) % 230),
        "nota": round(4.1 + ((i + j) % 9) / 10, 1),
        "distancia": round(1 + ((i * 3 + j * 2) % 100) / 10, 1),
    })

# ================= FUNÇÕES DE PERSISTÊNCIA =================


def carregar_json(caminho):
  try:
    with open(caminho, "r", encoding="utf-8") as f:
      return json.load(f)
  except (FileNotFoundError, json.JSONDecodeError):
    return []


def salvar_json(caminho, dados):
  with open(caminho, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=4)


def exportar_dados_pre_carregados():
  salvar_json(ARQUIVO_PROFISSIONAIS, PROFISSIONAIS_INICIAIS)
  salvar_json(ARQUIVO_SERVICOS, SERVICOS)


# ================= CLASSE PRINCIPAL =================


class ResolucionadorApp:

  def __init__(self, root):
    self.root = root
    self.root.title("RESOLUCIONADOR DE PROBLEMAS")
    self.root.geometry("760x650")
    self.root.resizable(False, False)

    self.escuro = False
    self.usuario_logado = None
    self.tipo_usuario = None
    self.servico_selecionado = ""
    self.profissional_selecionado = None

    self.tela_inicio()

  def limpar_tela(self):
    for widget in self.root.winfo_children():
      widget.destroy()

  def obter_cores(self):
    bg = "#111827" if self.escuro else "#F5F3FF"
    fg = "#FFFFFF" if self.escuro else "#171329"
    return bg, fg

  def aplicar_tema(self):
    bg, fg = self.obter_cores()
    self.root.configure(bg=bg)
    for w in self.root.winfo_children():
      if w.winfo_class() in ["Label", "Button"]:
        w.configure(bg=bg, fg=fg)

  def alternar_tema(self, f_redesenhar):
    self.escuro = not self.escuro
    f_redesenhar()

  # ================= TELAS =================

  def tela_inicio(self):
    self.limpar_tela()

    tk.Label(
        self.root, text="👩‍🔧 Provision", font=("Arial", 30, "bold")
    ).pack(pady=(70, 5))
    tk.Button(
        self.root,
        text="INICIAR SISTEMA",
        command=self.tela_login,
        width=28,
        height=2,
        bg="#6C4BF4",
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        cursor="hand2",
    ).pack(pady=30)

    texto_tema = "☀️ Modo claro" if self.escuro else "🌙 Modo escuro"
    tk.Button(
        self.root,
        text=texto_tema,
        command=lambda: self.alternar_tema(self.tela_inicio),
        width=20,
    ).pack()
    self.aplicar_tema()

  def tela_login(self):
    self.limpar_tela()

    tk.Label(
        self.root, text="🔐 CENTRAL DE ACESSO", font=("Arial", 24, "bold")
    ).pack(pady=40)

    tk.Label(self.root, text="Usuário").pack()
    usuario_entry = tk.Entry(self.root, width=32)
    usuario_entry.pack(pady=8)

    tk.Label(self.root, text="Senha").pack()
    senha_entry = tk.Entry(self.root, width=32, show="●")
    senha_entry.pack(pady=8)

    def autenticar():
      user = usuario_entry.get().strip()
      pwd = senha_entry.get().strip()

      if user == ROOT_USER and pwd == ROOT_PASS:
        self.usuario_logado = ROOT_USER
        self.tipo_usuario = "Administrador"
        if messagebox.askyesno(
            "Acesso Root Master",
            "Deseja cadastrar seu usuário próprio e exportar os dados"
            " pré-carregados agora?",
        ):
          self.tela_criar_usuario_root()
        else:
          self.tela_sistema()
        return

      usuarios = carregar_json(ARQUIVO_USUARIOS)
      for u in usuarios:
        if u["usuario"] == user and u["senha"] == pwd:
          self.usuario_logado = user
          self.tipo_usuario = u.get("tipo", "Comum")
          self.tela_sistema()
          return

      messagebox.showerror("Acesso Negado", "Usuário ou senha incorretos.")

    tk.Button(
        self.root,
        text="ENTRAR NO SISTEMA",
        command=autenticar,
        width=28,
        height=2,
        bg="#6C4BF4",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
    ).pack(pady=20)

    tk.Button(self.root, text="← Voltar", command=self.tela_inicio).pack()
    self.aplicar_tema()

  def tela_criar_usuario_root(self):
    self.limpar_tela()

    tk.Label(
        self.root,
        text="👑 CADASTRO DE USUÁRIO MASTER",
        font=("Arial", 20, "bold"),
    ).pack(pady=30)
    tk.Label(
        self.root,
        text=(
            "Crie suas credenciais personalizadas e exporte os dados dosistema."
        ),
        font=("Arial", 10),
    ).pack(pady=5)

    tk.Label(self.root, text="Novo Nome de Usuário").pack(pady=(20, 5))
    novo_user_entry = tk.Entry(self.root, width=32)
    novo_user_entry.pack()

    tk.Label(self.root, text="Nova Senha").pack(pady=(15, 5))
    nova_senha_entry = tk.Entry(self.root, width=32, show="●")
    nova_senha_entry.pack()

    def confirmar_criacao_e_exportacao():
      u = novo_user_entry.get().strip()
      s = nova_senha_entry.get().strip()

      if not u or not s:
        messagebox.showwarning("Atenção", "Preencha o usuário e a senha.")
        return

      usuarios = carregar_json(ARQUIVO_USUARIOS)
      if any(user["usuario"] == u for user in usuarios):
        messagebox.showwarning("Atenção", "Este nome de usuário já existe.")
        return

      usuarios.append({"usuario": u, "senha": s, "tipo": "Administrador"})
      salvar_json(ARQUIVO_USUARIOS, usuarios)
      exportar_dados_pre_carregados()

      messagebox.showinfo(
          "Sucesso 🎉",
          f"Usuário '{u}' criado com sucesso!\n\nDados pré-carregados"
          f" exportados para:\n- {ARQUIVO_PROFISSIONAIS}\n-"
          f" {ARQUIVO_SERVICOS}",
      )
      self.usuario_logado = u
      self.tela_sistema()

    tk.Button(
        self.root,
        text="💾 SALVAR USUÁRIO E EXPORTAR DADOS",
        command=confirmar_criacao_e_exportacao,
        width=32,
        height=2,
        bg="#10B981",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
    ).pack(pady=25)

    tk.Button(
        self.root,
        text="Pular / Ir para o Sistema",
        command=self.tela_sistema,
    ).pack()
    self.aplicar_tema()

  # ================= TELA DE GERENCIAMENTO DE USUÁRIOS =================

  def tela_gerenciar_usuarios(self):
    self.limpar_tela()

    tk.Label(
        self.root,
        text="👥 GERENCIAMENTO DE USUÁRIOS",
        font=("Arial", 20, "bold"),
    ).pack(pady=15)

    # Frame Formulário de Novo Usuário
    frame_form = tk.LabelFrame(
        self.root, text=" Criar Novo Usuário ", font=("Arial", 10, "bold")
    )
    frame_form.pack(pady=10, padx=20, fill="x")

    tk.Label(frame_form, text="Usuário:").grid(
        row=0, column=0, padx=5, pady=8, sticky="e"
    )
    entry_novo_u = tk.Entry(frame_form, width=20)
    entry_novo_u.grid(row=0, column=1, padx=5, pady=8)

    tk.Label(frame_form, text="Senha:").grid(
        row=0, column=2, padx=5, pady=8, sticky="e"
    )
    entry_nova_s = tk.Entry(frame_form, width=20, show="●")
    entry_nova_s.grid(row=0, column=3, padx=5, pady=8)

    tk.Label(frame_form, text="Tipo:").grid(
        row=0, column=4, padx=5, pady=8, sticky="e"
    )
    combo_tipo = ttk.Combobox(
        frame_form,
        values=["Comum", "Administrador"],
        state="readonly",
        width=14,
    )
    combo_tipo.grid(row=0, column=5, padx=5, pady=8)
    combo_tipo.set("Comum")

    def salvar_usuario():
      u = entry_novo_u.get().strip()
      s = entry_nova_s.get().strip()
      t = combo_tipo.get()

      if not u or not s:
        messagebox.showwarning(
            "Atenção", "Preencha usuário e senha para cadastrar."
        )
        return

      usuarios = carregar_json(ARQUIVO_USUARIOS)
      if any(item["usuario"] == u for item in usuarios):
        messagebox.showwarning("Atenção", f"O usuário '{u}' já existe.")
        return

      usuarios.append({"usuario": u, "senha": s, "tipo": t})
      salvar_json(ARQUIVO_USUARIOS, usuarios)

      messagebox.showinfo("Sucesso", f"Usuário '{u}' cadastrado com sucesso!")
      self.tela_gerenciar_usuarios()

    tk.Button(
        frame_form,
        text="➕ Cadastrar",
        command=salvar_usuario,
        bg="#10B981",
        fg="white",
        font=("Arial", 9, "bold"),
        relief="flat",
        cursor="hand2",
    ).grid(row=0, column=6, padx=10, pady=8)

    # Tabela de Usuários Cadastrados
    frame_tabela = tk.Frame(self.root)
    frame_tabela.pack(pady=10)

    colunas = ("usuario", "tipo")
    tree_user = ttk.Treeview(
        frame_tabela, columns=colunas, show="headings", height=8
    )

    tree_user.heading("usuario", text="Nome do Usuário")
    tree_user.heading("tipo", text="Tipo de Perfil")

    tree_user.column("usuario", width=250, anchor="w")
    tree_user.column("tipo", width=180, anchor="center")

    scrollbar = ttk.Scrollbar(
        frame_tabela, orient="vertical", command=tree_user.yview
    )
    tree_user.configure(yscrollcommand=scrollbar.set)

    tree_user.pack(side="left", fill="both")
    scrollbar.pack(side="right", fill="y")

    usuarios_lista = carregar_json(ARQUIVO_USUARIOS)
    for idx, usr in enumerate(usuarios_lista):
      tree_user.insert(
          "",
          "end",
          iid=str(idx),
          values=(usr.get("usuario", "-"), usr.get("tipo", "Comum")),
      )

    def excluir_usuario():
      selecao = tree_user.selection()
      if not selecao:
        messagebox.showwarning("Atenção", "Selecione um usuário na tabela.")
        return

      idx = int(selecionado[0]) if (selecionado := selecao) else None
      user_alvo = usuarios_lista[idx]["usuario"]

      if user_alvo == self.usuario_logado:
        messagebox.showerror(
            "Erro", "Você não pode excluir o seu próprio usuário conectado!"
        )
        return

      if messagebox.askyesno(
          "Confirmar Exclusão", f"Deseja remover o usuário '{user_alvo}'?"
      ):
        usuarios_lista.pop(idx)
        salvar_json(ARQUIVO_USUARIOS, usuarios_lista)
        messagebox.showinfo("Sucesso", "Usuário removido!")
        self.tela_gerenciar_usuarios()

    tk.Button(
        self.root,
        text="🗑️ EXCLUIR USUÁRIO SELECIONADO",
        command=excluir_usuario,
        bg="#EF4444",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        width=32,
    ).pack(pady=10)

    tk.Button(
        self.root,
        text="← Voltar à Central",
        command=self.tela_sistema,
        width=20,
    ).pack(pady=5)
    self.aplicar_tema()

  def tela_sistema(self):
    self.limpar_tela()

    tk.Label(
        self.root, text="AGENDAR", font=("Arial", 24, "bold")
    ).pack(pady=(20, 5))
    tk.Label(
        self.root,
      text=f"Usuário ativo: {self.usuario_logado} | Tipo: {self.tipo_usuario or 'Comum'}",
        font=("Arial", 10, "italic"),
    ).pack(pady=(0, 15))

    tk.Label(
        self.root,
        text="Escreva seu problema:",
        font=("Arial", 11),
    ).pack()

    problema_entry = tk.Entry(self.root, width=65, font=("Arial", 12))
    problema_entry.pack(pady=15)
    problema_entry.focus()

    def analisar_problema():
      texto = problema_entry.get().lower().strip()
      if not texto:
        messagebox.showwarning("Atenção", "Descreva seu problema.")
        return

      palavras_chave = {
          "vazamento": "Encanador",
          "torneira": "Encanador",
          "tomada": "Eletricista",
          "luz": "Eletricista",
          "geladeira": "Geladeira",
          "celular": "Celular",
          "computador": "Informática",
          "notebook": "Informática",
          "internet": "Internet",
          "cabelo": "Cabeleireiro",
          "unha": "Manicure",
          "carro": "Mecânico",
          "pneu": "Borracheiro",
          "piscina": "Piscineiro",
          "cachorro": "Veterinário",
          "gato": "Veterinário",
      }

      self.servico_selecionado = "Outro problema"
      for palavra, servico in palavras_chave.items():
        if palavra in texto:
          self.servico_selecionado = servico
          break

      self.tela_profissionais()

    tk.Button(
        self.root,
        text="Selecionar",
        command=analisar_problema,
        width=32,
        height=2,
        bg="#6C4BF4",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
    ).pack(pady=4)

    tk.Button(
        self.root,
        text="Agendamentos",
        command=self.tela_meus_agendamentos,
        width=32,
        height=2,
        bg="#10B981",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
    ).pack(pady=4)

    tk.Button(
        self.root,
        text="👥 GERENCIAR / CRIAR USUÁRIOS",
        command=self.tela_gerenciar_usuarios,
        width=32,
        height=2,
        bg="#F59E0B",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
    ).pack(pady=4)

    texto_tema = "☀️ Modo claro" if self.escuro else "🌙 Modo escuro"
    tk.Button(
        self.root,
        text=texto_tema,
        command=lambda: self.alternar_tema(self.tela_sistema),
    ).pack(pady=10)
    self.aplicar_tema()

  def tela_profissionais(self):
    self.limpar_tela()

    profissionais_base = (
        carregar_json(ARQUIVO_PROFISSIONAIS) or PROFISSIONAIS_INICIAIS
    )
    lista = [
        p for p in profissionais_base if p["servico"] == self.servico_selecionado
    ]
    if not lista:
      messagebox.showwarning(
          "Serviço indisponível",
          f"Não há profissionais cadastrados para {self.servico_selecionado}.",
      )
      self.tela_sistema()
      return

    melhor = max(
        lista,
        key=lambda p: (p["nota"] * 20) - (p["preco"] * 0.08) - p["distancia"],
    )

    tk.Label(
        self.root, text="✨ SOLUÇÃO ENCONTRADA", font=("Arial", 23, "bold")
    ).pack(pady=25)
    tk.Label(
        self.root,
        text=f"Serviço identificado: {self.servico_selecionado}",
        font=("Arial", 12),
    ).pack()

    tk.Label(
        self.root,
        text=(
            f"🤖 Recomendação automática: {melhor['nome']}\n"
            f"⭐ {melhor['nota']}  •  R$ {melhor['preco']:.2f}  •  "
            f"📍 {melhor['distancia']} km"
        ),
        font=("Arial", 12, "bold"),
    ).pack(pady=15)

    lista_box = tk.Listbox(self.root, width=85, height=10, font=("Arial", 10))
    lista_box.pack()

    for p in lista:
      lista_box.insert(
          tk.END,
          f"{p['nome']} | ⭐ {p['nota']} | R$ {p['preco']:.2f} |"
          f" {p['distancia']} km",
      )

    idx_melhor = lista.index(melhor)
    lista_box.selection_set(idx_melhor)

    def confirmar_escolha():
      selecao = lista_box.curselection()
      if not selecao:
        messagebox.showwarning("Atenção", "Escolha um profissional.")
        return
      self.profissional_selecionado = lista[selecao[0]]
      self.tela_agendamento()

    tk.Button(
        self.root,
        text="✅ USAR ESTA SOLUÇÃO",
        command=confirmar_escolha,
        width=28,
        height=2,
        bg="#6C4BF4",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
    ).pack(pady=15)

    self.aplicar_tema()

  def tela_agendamento(self):
    self.limpar_tela()

    p = self.profissional_selecionado

    tk.Label(
        self.root, text="📅 FINALIZAR SOLUÇÃO", font=("Arial", 23, "bold")
    ).pack(pady=30)
    tk.Label(
        self.root,
        text=f"{p['nome']}  •  ⭐ {p['nota']}  •  R$ {p['preco']:.2f}",
        font=("Arial", 12),
    ).pack()

    datas = [
        (date.today() + timedelta(days=i)).strftime("%d/%m/%Y")
        for i in range(7)
    ]

    tk.Label(self.root, text="Quando você quer resolver?").pack(pady=(25, 5))

    data_combo = ttk.Combobox(
        self.root, values=datas, state="readonly", width=25
    )
    data_combo.pack()
    data_combo.set(datas[0])

    horario_combo = ttk.Combobox(
        self.root, values=HORARIOS, state="readonly", width=20
    )
    horario_combo.pack(pady=15)
    horario_combo.set(HORARIOS[0])

    def salvar_e_concluir():
      agendamentos = carregar_json(ARQUIVO_AGENDAMENTOS)
      agendamentos.append({
          "usuario": self.usuario_logado,
          "profissional": p["nome"],
          "servico": p["servico"],
          "valor": p["preco"],
          "data": data_combo.get(),
          "horario": horario_combo.get(),
          "status": "Confirmado",
      })
      salvar_json(ARQUIVO_AGENDAMENTOS, agendamentos)

      messagebox.showinfo(
          "Tudo certo! 🎉", "Seu problema foi encaminhado com sucesso!"
      )
      self.tela_sistema()

    tk.Button(
        self.root,
        text="🚀 RESOLVER AGORA",
        command=salvar_e_concluir,
        width=28,
        height=2,
        bg="#6C4BF4",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
    ).pack(pady=25)

    self.aplicar_tema()

  def tela_meus_agendamentos(self):
    self.limpar_tela()

    tk.Label(
        self.root, text="📋 MEUS AGENDAMENTOS", font=("Arial", 22, "bold")
    ).pack(pady=20)

    agendamentos = carregar_json(ARQUIVO_AGENDAMENTOS)
    if self.tipo_usuario != "Administrador":
      agendamentos = [
          item
          for item in agendamentos
          if item.get("usuario") == self.usuario_logado
      ]

    if not agendamentos:
      tk.Label(
          self.root, text="Nenhum agendamento encontrado.", font=("Arial", 12)
      ).pack(pady=40)
    else:
      frame_tabela = tk.Frame(self.root)
      frame_tabela.pack(pady=10)

      colunas = ("servico", "profissional", "data", "horario", "valor", "usuario")
      tree = ttk.Treeview(
          frame_tabela, columns=colunas, show="headings", height=10
      )

      tree.heading("servico", text="Serviço")
      tree.heading("profissional", text="Profissional")
      tree.heading("data", text="Data")
      tree.heading("horario", text="Horário")
      tree.heading("valor", text="Valor (R$)")
      tree.heading("usuario", text="Usuário")

      tree.column("servico", width=120, anchor="w")
      tree.column("profissional", width=110, anchor="w")
      tree.column("data", width=80, anchor="center")
      tree.column("horario", width=65, anchor="center")
      tree.column("valor", width=75, anchor="e")
      tree.column("usuario", width=100, anchor="center")

      scrollbar = ttk.Scrollbar(
          frame_tabela, orient="vertical", command=tree.yview
      )
      tree.configure(yscrollcommand=scrollbar.set)

      tree.pack(side="left", fill="both")
      scrollbar.pack(side="right", fill="y")

      for idx, item in enumerate(agendamentos):
        tree.insert(
            "",
            "end",
            iid=str(idx),
            values=(
                item.get("servico", "-"),
                item.get("profissional", "-"),
                item.get("data", "-"),
                item.get("horario", "-"),
                f"R$ {item.get('valor', 0):.2f}",
                item.get("usuario", "-"),
            ),
        )

      def cancelar_item():
        selecionado = tree.selection()
        if not selecionado:
          messagebox.showwarning(
              "Atenção", "Selecione um agendamento na lista."
          )
          return

        index = int(selecionado[0])
        if messagebox.askyesno(
            "Confirmar Cancelamento",
            "Deseja realmente cancelar este agendamento?",
        ):
          agendamentos.pop(index)
          salvar_json(ARQUIVO_AGENDAMENTOS, agendamentos)
          messagebox.showinfo("Sucesso", "Agendamento cancelado com sucesso!")
          self.tela_meus_agendamentos()

      tk.Button(
          self.root,
          text="❌ CANCELAR AGENDAMENTO SELECIONADO",
          command=cancelar_item,
          bg="#EF4444",
          fg="white",
          font=("Arial", 10, "bold"),
          relief="flat",
          cursor="hand2",
          width=35,
          height=2,
      ).pack(pady=15)

    tk.Button(
        self.root,
        text="← Voltar à Central",
        command=self.tela_sistema,
        width=20,
    ).pack(pady=5)
    self.aplicar_tema()


# ================= EXECUÇÃO =================

if __name__ == "__main__":
  root = tk.Tk()
  app = ResolucionadorApp(root)
  root.mainloop()