import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# =========================
# VERIFICAR POSTAGEM
# =========================

ja_postou = False

# =========================
# VALIDAR NOME EM TEMPO REAL
# =========================

def validar_nome(event=None):

    nome = entrada_nome.get()

    # APENAS LETRAS
    if nome.replace(" ", "").isalpha():

        entrada_nome.config(
            fg="black"
        )

        mensagem_nome.config(
            text=""
        )

    else:

        # TEXTO VERMELHO
        entrada_nome.config(
            fg="red"
        )

        # MENSAGEM
        mensagem_nome.config(
            text="Nome inválido, reveja o que escreveu.",
            fg="red"
        )

# =========================
# FUNÇÃO FINALIZAR
# =========================

def finalizar():

    nome = entrada_nome.get()

    dia = entrada_dia.get()
    mes = entrada_mes.get()
    ano = entrada_ano.get()

    email = entrada_email.get()

    texto_descricao = descricao.get("1.0", tk.END)

    erro = False

    # =========================
    # VALIDAR NOME
    # =========================

    if not nome.replace(" ", "").isalpha():

        erro = True

    # =========================
    # VALIDAR DATA
    # =========================

    try:

        dia_int = int(dia)
        mes_int = int(mes)
        ano_int = int(ano)

        data = datetime(
            ano_int,
            mes_int,
            dia_int
        )

        ano_atual = datetime.now().year

        idade = ano_atual - ano_int

        # MAIS DE 100 ANOS
        if idade > 100:

            erro = True

    except:

        erro = True

    # =========================
    # VALIDAR EMAIL
    # =========================

    if "@gmail.com" not in email:

        erro = True

    # =========================
    # VALIDAR DESCRIÇÃO
    # =========================

    if texto_descricao.strip() == "":

        erro = True

    # =========================
    # SE TIVER ERRO
    # =========================

    if erro:

        messagebox.showerror(
            "Erro",
            "Não foi possível finalizar a conta pois algo está incorreto."
        )

        return

    # =========================
    # BOTÃO VERDE
    # =========================

    botao_finalizar.config(
        bg="green",
        fg="white"
    )

    # =========================
    # ESCONDER CRIAR CONTA
    # =========================

    frame_conta.pack_forget()

    # =========================
    # MOSTRAR POEMA
    # =========================

    frame_poema.pack(pady=30)

# =========================
# FUNÇÃO PUBLICAR
# =========================

def publicar():

    global ja_postou

    poema = caixa_poema.get("1.0", tk.END)

    # =========================
    # JÁ POSTOU
    # =========================

    if ja_postou:

        messagebox.showerror(
            "Erro",
            "Você já publicou um poema."
        )

        return

    # =========================
    # POEMA VAZIO
    # =========================

    if poema.strip() == "":

        messagebox.showerror(
            "Erro",
            "Escreva um poema."
        )

        return

    # =========================
    # LIMITE DE CARACTERES
    # =========================

    if len(poema) > 500:

        messagebox.showerror(
            "Erro",
            "Máximo de 500 caracteres."
        )

        return

    # =========================
    # BOTÃO VERDE
    # =========================

    ja_postou = True

    botao_publicar.config(
        bg="green",
        fg="white"
    )

    # =========================
    # MENSAGEM
    # =========================

    messagebox.showinfo(
        "Postado",
        "✅ Poema postado com sucesso!"
    )

# =========================
# JANELA
# =========================

janela = tk.Tk()

janela.title("Rede de Poemas")

janela.geometry("700x700")

janela.configure(bg="white")

# =========================
# SCROLL
# =========================

canvas = tk.Canvas(
    janela,
    bg="white"
)

scrollbar = tk.Scrollbar(
    janela,
    orient="vertical",
    command=canvas.yview
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side="right",
    fill="y"
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)

# =========================
# FRAME PRINCIPAL
# =========================

frame_principal = tk.Frame(
    canvas,
    bg="white"
)

canvas.create_window(
    (350, 0),
    window=frame_principal,
    anchor="n"
)

frame_principal.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

# =========================
# ROLAR MOUSE
# =========================

canvas.bind_all(
    "<MouseWheel>",
    lambda event: canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )
)

# =========================
# TÍTULO
# =========================

titulo = tk.Label(
    frame_principal,
    text="📖 Rede de Poemas",
    font=("Arial", 28, "bold"),
    bg="white"
)

titulo.pack(pady=30)

# =========================
# FRAME CRIAR CONTA
# =========================

frame_conta = tk.Frame(
    frame_principal,
    bg="white"
)

frame_conta.pack()

# =========================
# TEXTO CRIAR CONTA
# =========================

texto_conta = tk.Label(
    frame_conta,
    text="Criar Conta",
    font=("Arial", 20, "bold"),
    bg="white",
    fg="#3b2c85"
)

texto_conta.pack(pady=20)

# =========================
# NOME
# =========================

label_nome = tk.Label(
    frame_conta,
    text="Nome:",
    font=("Arial", 14, "bold"),
    bg="white"
)

label_nome.pack(anchor="w")

entrada_nome = tk.Entry(
    frame_conta,
    width=50,
    font=("Arial", 13)
)

entrada_nome.pack(pady=10)

# VALIDAR ENQUANTO ESCREVE
entrada_nome.bind(
    "<KeyRelease>",
    validar_nome
)

# MENSAGEM DE ERRO
mensagem_nome = tk.Label(
    frame_conta,
    text="",
    bg="white",
    fg="red",
    font=("Arial", 10)
)

mensagem_nome.pack()

# =========================
# DATA DE NASCIMENTO
# =========================

label_data = tk.Label(
    frame_conta,
    text="Data de nascimento",
    font=("Arial", 14, "bold"),
    bg="white"
)

label_data.pack(anchor="w")

# DIA
entrada_dia = tk.Entry(
    frame_conta,
    width=10,
    font=("Arial", 13)
)

entrada_dia.pack(pady=5)

entrada_dia.insert(0, "Dia")

# MÊS
entrada_mes = tk.Entry(
    frame_conta,
    width=10,
    font=("Arial", 13)
)

entrada_mes.pack(pady=5)

entrada_mes.insert(0, "Mês")

# ANO
entrada_ano = tk.Entry(
    frame_conta,
    width=10,
    font=("Arial", 13)
)

entrada_ano.pack(pady=5)

entrada_ano.insert(0, "Ano")

# =========================
# EMAIL
# =========================

label_email = tk.Label(
    frame_conta,
    text="E-mail:",
    font=("Arial", 14, "bold"),
    bg="white"
)

label_email.pack(anchor="w")

entrada_email = tk.Entry(
    frame_conta,
    width=50,
    font=("Arial", 13)
)

entrada_email.pack(pady=10)

# =========================
# DESCRIÇÃO
# =========================

label_descricao = tk.Label(
    frame_conta,
    text="Descrição:",
    font=("Arial", 14, "bold"),
    bg="white"
)

label_descricao.pack(anchor="w")

descricao = tk.Text(
    frame_conta,
    width=50,
    height=6,
    font=("Arial", 12)
)

descricao.pack(pady=10)

# =========================
# BOTÃO FINALIZAR
# =========================

botao_finalizar = tk.Button(
    frame_conta,
    text="Finalizar",
    width=20,
    height=2,
    bg="white",
    fg="black",
    font=("Arial", 12, "bold"),
    command=finalizar
)

botao_finalizar.pack(pady=20)

# =========================
# FRAME POEMA
# =========================

frame_poema = tk.Frame(
    frame_principal,
    bg="white"
)

# ESCONDER NO COMEÇO
frame_poema.pack_forget()

# =========================
# TEXTO POEMA
# =========================

texto_poema = tk.Label(
    frame_poema,
    text="✍️ Publique seu poema",
    font=("Arial", 20, "bold"),
    bg="white",
    fg="#3b2c85"
)

texto_poema.pack(pady=20)

# =========================
# CAIXA POEMA
# =========================

caixa_poema = tk.Text(
    frame_poema,
    width=50,
    height=10,
    font=("Arial", 12)
)

caixa_poema.pack(pady=10)

# =========================
# BOTÃO PUBLICAR
# =========================

botao_publicar = tk.Button(
    frame_poema,
    text="Publicar",
    width=20,
    height=2,
    bg="white",
    fg="black",
    font=("Arial", 12, "bold"),
    command=publicar
)

botao_publicar.pack(pady=20)

# =========================
# ESPAÇO EXTRA
# =========================

espaco = tk.Label(
    frame_principal,
    text="",
    bg="white"
)

espaco.pack(pady=200)

# =========================
# INICIAR APP
# =========================

janela.mainloop()
