"python"
# ==========================================
# IMPORTAÇÕES
# ==========================================

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

from tkcalendar import DateEntry
from PIL import Image, ImageTk

from datetime import datetime

# ==========================================
# CORES
# ==========================================

AZUL_FUNDO = "#1282A2"
AZUL_CLARO = "#1EB6E8"
BRANCO = "white"
AMARELO = "#D6E04B"
ROSA = "#FF2D8D"

# ==========================================
# VARIÁVEIS
# ==========================================

foto_perfil = None
foto_tk = None

# ==========================================
# JANELA
# ==========================================

janela = tk.Tk()

janela.title("Rede de Poemas")

janela.geometry("900x750")

janela.configure(
    bg=AZUL_FUNDO
)

# ==========================================
# SCROLL
# ==========================================

canvas_scroll = tk.Canvas(
    janela,
    bg=AZUL_FUNDO,
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    janela,
    orient="vertical",
    command=canvas_scroll.yview
)

canvas_scroll.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side="right",
    fill="y"
)

canvas_scroll.pack(
    side="left",
    fill="both",
    expand=True
)

frame_scroll = tk.Frame(
    canvas_scroll,
    bg=AZUL_FUNDO
)

canvas_scroll.create_window(
    (450, 0),
    window=frame_scroll,
    anchor="n"
)

frame_scroll.bind(
    "<Configure>",
    lambda e: canvas_scroll.configure(
        scrollregion=canvas_scroll.bbox("all")
    )
)

# ==========================================
# ROLAR MOUSE
# ==========================================

canvas_scroll.bind_all(
    "<MouseWheel>",
    lambda event: canvas_scroll.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )
)

# ==========================================
# CANVAS DECORAÇÃO
# ==========================================

canvas = tk.Canvas(
    frame_scroll,
    width=900,
    height=2000,
    bg=AZUL_FUNDO,
    highlightthickness=0
)

canvas.pack()

# ==========================================
# DECORAÇÕES
# ==========================================

def decoracao():

    canvas.create_oval(
        -120, -120, 150, 150,
        fill="#149BC7",
        outline=""
    )

    canvas.create_oval(
        650, 500, 980, 850,
        fill="#19B6E5",
        outline=""
    )

    canvas.create_oval(
        720, 100, 850, 230,
        outline=AMARELO,
        width=6
    )

    canvas.create_oval(
        600, 350, 690, 440,
        outline=ROSA,
        width=5
    )

    canvas.create_oval(
        200, 40, 320, 160,
        fill=AMARELO,
        outline=""
    )

    for linha in range(10):

        for coluna in range(12):

            x = 550 + (coluna * 18)
            y = 580 + (linha * 18)

            canvas.create_oval(
                x,
                y,
                x + 5,
                y + 5,
                fill="#5CC9EB",
                outline=""
            )

decoracao()

# ==========================================
# FRAME CENTRAL
# ==========================================

frame_central = tk.Frame(
    canvas,
    bg=AZUL_FUNDO
)

frame_central.place(
    relx=0.5,
    rely=0,
    anchor="n"
)

# ==========================================
# TELA INICIAL
# ==========================================

frame_inicio = tk.Frame(
    frame_central,
    bg=AZUL_FUNDO
)

frame_inicio.pack(
    pady=40
)

# ==========================================
# LOGO
# ==========================================

logo = tk.Label(
    frame_inicio,
    text="VOCAÇÃO",
    font=("Georgia", 38, "bold"),
    fg=BRANCO,
    bg=AZUL_FUNDO
)

logo.pack(
    pady=(30, 5)
)

# ==========================================
# POÉTICA
# ==========================================

poetica = tk.Label(
    frame_inicio,
    text="poética",
    font=("Segoe Script", 28, "italic"),
    fg=AMARELO,
    bg=AZUL_FUNDO
)

poetica.pack()

# ==========================================
# LINHA
# ==========================================

linha = tk.Frame(
    frame_inicio,
    bg=BRANCO,
    width=280,
    height=2
)

linha.pack(
    pady=20
)

# ==========================================
# CORAÇÃO
# ==========================================

coracao = tk.Label(
    frame_inicio,
    text="💛",
    font=("Arial", 24),
    fg=AMARELO,
    bg=AZUL_FUNDO
)

coracao.pack(
    pady=(0, 15)
)

# ==========================================
# TÍTULO
# ==========================================

titulo = tk.Label(
    frame_inicio,
    text="Seja bem-vindo ✨",
    font=("Georgia", 30, "italic"),
    fg=BRANCO,
    bg=AZUL_FUNDO
)

titulo.pack(
    pady=10
)

# ==========================================
# SUBTÍTULO
# ==========================================

subtitulo = tk.Label(
    frame_inicio,
    text="Compartilhe poemas e sentimentos\ncom o mundo.",
    font=("Arial", 15),
    fg=BRANCO,
    bg=AZUL_FUNDO,
    justify="center"
)

subtitulo.pack(
    pady=15
)

# ==========================================
# ABRIR CADASTRO
# ==========================================

def abrir_cadastro():

    frame_inicio.pack_forget()

    frame_conta.pack(
        pady=40
    )

# ==========================================
# BOTÃO COMEÇAR
# ==========================================

botao_comecar = tk.Button(
    frame_inicio,
    text="Começar",
    font=("Arial", 15, "bold"),
    bg=AZUL_CLARO,
    fg="white",
    bd=0,
    padx=30,
    pady=12,
    cursor="hand2",
    command=abrir_cadastro
)

botao_comecar.pack(
    pady=40
)

# ==========================================
# FRAME CONTA
# ==========================================

frame_conta = tk.Frame(
    frame_central,
    bg=AZUL_FUNDO
)

# ==========================================
# CARD
# ==========================================

card = tk.Frame(
    frame_conta,
    bg="white",
    padx=40,
    pady=30
)

card.pack()

# ==========================================
# TÍTULO CONTA
# ==========================================

texto_conta = tk.Button(
    card,
    text="Criar Conta",
    font=("Arial", 20, "bold"),
    bg=AZUL_CLARO,
    fg="white",
    bd=0,
    padx=20,
    pady=10,
    cursor="hand2"
)

texto_conta.pack(
    pady=20
)

# ==========================================
# FOTO PERFIL
# ==========================================

texto_foto = tk.Label(
    card,
    text="Foto de Perfil",
    font=("Arial", 13, "bold"),
    bg="white"
)

texto_foto.pack(
    pady=10
)

label_foto = tk.Label(
    card,
    text="👤",
    font=("Arial", 40),
    bg="#F2F2F2",
    width=4,
    height=2
)

label_foto.pack(
    pady=10
)

# ==========================================
# ESCOLHER FOTO
# ==========================================

def escolher_foto():

    global foto_perfil
    global foto_tk

    caminho = filedialog.askopenfilename(
        title="Escolher Foto",
        filetypes=[
            ("Imagens", "*.png *.jpg *.jpeg")
        ]
    )

    if caminho:

        foto_perfil = caminho

        imagem = Image.open(caminho)

        imagem = imagem.resize((90, 90))

        foto_tk = ImageTk.PhotoImage(imagem)

        label_foto.config(
            image=foto_tk,
            text=""
        )

# ==========================================
# BOTÃO FOTO
# ==========================================

botao_foto = tk.Button(
    card,
    text="Escolher Foto",
    font=("Arial", 11, "bold"),
    bg=AZUL_CLARO,
    fg="white",
    bd=0,
    padx=20,
    pady=8,
    cursor="hand2",
    command=escolher_foto
)

botao_foto.pack(
    pady=10
)

# ==========================================
# NOME
# ==========================================

label_nome = tk.Label(
    card,
    text="👤 Nome",
    font=("Arial", 14, "bold"),
    bg="white"
)

label_nome.pack(anchor="w")

entrada_nome = tk.Entry(
    card,
    width=40,
    font=("Arial", 13),
    bd=2
)

entrada_nome.pack(
    pady=10
)

mensagem_nome = tk.Label(
    card,
    text="",
    bg="white",
    fg="red",
    font=("Arial", 10)
)

mensagem_nome.pack()

# ==========================================
# VALIDAR NOME
# ==========================================

def validar_nome(event=None):

    nome = entrada_nome.get()

    if nome.replace(" ", "").isalpha():

        entrada_nome.config(
            fg="black"
        )

        mensagem_nome.config(
            text=""
        )

    else:

        entrada_nome.config(
            fg="red"
        )

        mensagem_nome.config(
            text="Nome inválido.",
            fg="red"
        )

entrada_nome.bind(
    "<KeyRelease>",
    validar_nome
)

# ==========================================
# DATA
# ==========================================

label_data = tk.Label(
    card,
    text="📅 Data de nascimento",
    font=("Arial", 14, "bold"),
    bg="white"
)

label_data.pack(anchor="w")

calendario = DateEntry(
    card,
    width=20,
    background=AZUL_CLARO,
    foreground="white",
    borderwidth=2,
    date_pattern="dd/mm/yyyy",
    font=("Arial", 12),
    locale="pt_BR"
)

calendario.pack(
    pady=15
)

mensagem_data = tk.Label(
    card,
    text="",
    bg="white",
    fg="red",
    font=("Arial", 10)
)

mensagem_data.pack()

# ==========================================
# EMAIL
# ==========================================

label_email = tk.Label(
    card,
    text="✉️ E-mail",
    font=("Arial", 14, "bold"),
    bg="white"
)

label_email.pack(anchor="w")

entrada_email = tk.Entry(
    card,
    width=40,
    font=("Arial", 13),
    bd=2
)

entrada_email.pack(
    pady=10
)

mensagem_email = tk.Label(
    card,
    text="",
    bg="white",
    fg="red",
    font=("Arial", 10)
)

mensagem_email.pack()

# ==========================================
# VALIDAR EMAIL
# ==========================================

def validar_email(event=None):

    email = entrada_email.get()

    if "@gmail.com" in email or "@vocacao" in email:

        entrada_email.config(
            fg="black"
        )

        mensagem_email.config(
            text=""
        )

    else:

        entrada_email.config(
            fg="red"
        )

        mensagem_email.config(
            text="E-mail inválido.",
            fg="red"
        )

entrada_email.bind(
    "<KeyRelease>",
    validar_email
)

# ==========================================
# DESCRIÇÃO
# ==========================================

label_descricao = tk.Label(
    card,
    text="✨ Descrição",
    font=("Arial", 14, "bold"),
    bg="white"
)

label_descricao.pack(anchor="w")

# ==========================================
# CAIXA DESCRIÇÃO
# ==========================================

descricao = tk.Text(
    card,
    width=40,
    height=5,
    font=("Arial", 12),
    bd=2
)

descricao.pack(
    pady=10
)

# ==========================================
# MENSAGEM ERRO
# ==========================================

mensagem_descricao = tk.Label(
    card,
    text="",
    bg="white",
    fg="red",
    font=("Arial", 10)
)

mensagem_descricao.pack()

# ==========================================
# CONTADOR
# ==========================================

contador_descricao = tk.Label(
    card,
    text="0/128 caracteres",
    bg="white",
    fg="gray",
    font=("Arial", 10)
)

contador_descricao.pack(
    anchor="e",
    pady=(0, 10)
)

# ==========================================
# VALIDAR DESCRIÇÃO
# ==========================================

def validar_descricao(event=None):

    texto = descricao.get(
        "1.0",
        "end-1c"
    )

    quantidade = len(texto)

    contador_descricao.config(
        text=f"{quantidade}/128 caracteres"
    )

    if quantidade <= 128:

        descricao.config(
            fg="black"
        )

        contador_descricao.config(
            fg="gray"
        )

        mensagem_descricao.config(
            text=""
        )

    else:

        descricao.config(
            fg="red"
        )

        contador_descricao.config(
            fg="red"
        )

        mensagem_descricao.config(
            text="Máximo de 128 caracteres.",
            fg="red"
        )

# ==========================================
# ATUALIZAR ENQUANTO ESCREVE
# ==========================================

descricao.bind(
    "<KeyRelease>",
    validar_descricao
)

# ==========================================
# FRAME POEMA
# ==========================================

frame_poema = tk.Frame(
    frame_central,
    bg=AZUL_FUNDO
)

# ==========================================
# FINALIZAR
# ==========================================

def finalizar():

    nome = entrada_nome.get()

    email = entrada_email.get()

    texto = descricao.get(
        "1.0",
        tk.END
    )

    data_nascimento = calendario.get_date()

    hoje = datetime.now()

    idade = hoje.year - data_nascimento.year

    if (
        (hoje.month, hoje.day)
        <
        (data_nascimento.month, data_nascimento.day)
    ):

        idade -= 1

    erro = False

    # NOME
    if not nome.replace(" ", "").isalpha():

        entrada_nome.config(
            fg="red"
        )

        mensagem_nome.config(
            text="Nome inválido."
        )

        erro = True

    else:

        entrada_nome.config(
            fg="black"
        )

        mensagem_nome.config(
            text=""
        )

    # EMAIL
    if "@gmail.com" not in email and "@vocacao" not in email:

        entrada_email.config(
            fg="red"
        )

        mensagem_email.config(
            text="E-mail inválido."
        )

        erro = True

    else:

        entrada_email.config(
            fg="black"
        )

        mensagem_email.config(
            text=""
        )

    # DESCRIÇÃO
    if len(texto) > 128:

        descricao.config(
            fg="red"
        )

        mensagem_descricao.config(
            text="Máximo de 128 caracteres."
        )

        erro = True

    else:

        descricao.config(
            fg="black"
        )

        mensagem_descricao.config(
            text=""
        )

    # IDADE
    if idade < 10:

        mensagem_data.config(
            text="Você precisa ter mais de 10 anos."
        )

        erro = True

    elif idade > 100:

        mensagem_data.config(
            text="Idade inválida."
        )

        erro = True

    else:

        mensagem_data.config(
            text=""
        )

    # ERRO
    if erro:

        messagebox.showerror(
            "Erro",
            "Preencha os campos corretamente."
        )

        return

    frame_conta.pack_forget()

    frame_poema.pack(
        pady=40
    )

# ==========================================
# BOTÃO FINALIZAR
# ==========================================

texto_conta.config(
    command=finalizar
)

# ==========================================
# CARD POEMA
# ==========================================

card_poema = tk.Frame(
    frame_poema,
    bg="white",
    padx=40,
    pady=30
)

card_poema.pack()

# ==========================================
# TÍTULO POEMA
# ==========================================

titulo_poema = tk.Label(
    card_poema,
    text="📖 Publicar Poema",
    font=("Arial", 22, "bold"),
    bg="white",
    fg=AZUL_FUNDO
)

titulo_poema.pack(
    pady=20
)

# ==========================================
# CAIXA POEMA
# ==========================================

caixa_poema = tk.Text(
    card_poema,
    width=45,
    height=10,
    font=("Arial", 13),
    bd=2
)

caixa_poema.pack(
    pady=20
)

# ==========================================
# LIMPAR POEMA
# ==========================================

def limpar_poema():

    caixa_poema.delete(
        "1.0",
        tk.END
    )

# ==========================================
# POSTS
# ==========================================

frame_posts = tk.Frame(
    card_poema,
    bg="white"
)

frame_posts.pack(
    pady=20
)

# ==========================================
# CURTIR
# ==========================================

def curtir(label, botao):

    texto_atual = label.cget("text")

    numero = int(
        texto_atual.split()[1]
    )

    numero += 1

    label.config(
        text=f"❤️ {numero} curtidas"
    )

    botao.config(
        text="Curtido ❤️",
        state="disabled",
        bg="gray"
    )

# ==========================================
# PUBLICAR
# ==========================================

def publicar():

    poema = caixa_poema.get(
        "1.0",
        tk.END
    ).strip()

    if poema == "":

        messagebox.showerror(
            "Erro",
            "Escreva um poema."
        )

        return

    if len(poema) > 500:

        messagebox.showerror(
            "Erro",
            "Máximo de 500 caracteres."
        )

        return

    post = tk.Frame(
        frame_posts,
        bg="#F5F5F5",
        padx=20,
        pady=20
    )

    post.pack(
        pady=20,
        fill="x"
    )

    # FOTO PERFIL
    if foto_perfil:

        imagem_post = Image.open(
            foto_perfil
        )

        imagem_post = imagem_post.resize(
            (50, 50)
        )

        foto_post = ImageTk.PhotoImage(
            imagem_post
        )

        label_imagem = tk.Label(
            post,
            image=foto_post,
            bg="#F5F5F5"
        )

        label_imagem.image = foto_post

        label_imagem.pack(
            anchor="w",
            pady=5
        )

    nome_post = tk.Label(
        post,
        text=f"👤 {entrada_nome.get()}",
        font=("Arial", 13, "bold"),
        bg="#F5F5F5",
        fg=AZUL_FUNDO
    )

    nome_post.pack(anchor="w")

    texto_post = tk.Label(
        post,
        text=poema,
        font=("Arial", 12),
        bg="#F5F5F5",
        justify="left",
        wraplength=500
    )

    texto_post.pack(
        anchor="w",
        pady=15
    )

    curtidas_label = tk.Label(
        post,
        text="❤️ 0 curtidas",
        font=("Arial", 11, "bold"),
        bg="#F5F5F5",
        fg=ROSA
    )

    curtidas_label.pack(anchor="w")

    botao_curtir = tk.Button(
        post,
        text="Curtir ❤️",
        font=("Arial", 11, "bold"),
        bg=AZUL_CLARO,
        fg="white",
        bd=0,
        padx=15,
        pady=5,
        cursor="hand2"
    )

    botao_curtir.config(
        command=lambda: curtir(
            curtidas_label,
            botao_curtir
        )
    )

    botao_curtir.pack(
        anchor="w",
        pady=10
    )

    caixa_poema.delete(
        "1.0",
        tk.END
    )

    messagebox.showinfo(
        "Sucesso",
        "Poema publicado com sucesso!"
    )

# ==========================================
# BOTÃO PUBLICAR
# ==========================================

botao_publicar = tk.Button(
    card_poema,
    text="Publicar ✨",
    font=("Arial", 15, "bold"),
    bg=AZUL_CLARO,
    fg="white",
    bd=0,
    padx=30,
    pady=12,
    cursor="hand2",
    command=publicar
)

botao_publicar.pack(
    pady=10
)

# ==========================================
# BOTÃO LIMPAR
# ==========================================

botao_limpar = tk.Button(
    card_poema,
    text="🗑 Limpar",
    font=("Arial", 13, "bold"),
    bg="white",
    fg=AZUL_CLARO,
    bd=2,
    padx=20,
    pady=10,
    cursor="hand2",
    command=limpar_poema
)

botao_limpar.pack(
    pady=10
)

# ==========================================
# INICIAR
# ==========================================

janela.mainloop()