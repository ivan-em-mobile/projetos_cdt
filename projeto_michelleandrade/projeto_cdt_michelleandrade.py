import tkinter as tk
from PIL import Image, ImageTk

# dados dos pets
pets = [
    {
        "nome": "Amora",
        "idade": 5,
        "tipo": "Cachorro",
        "raça": "Pitbull",
        "descricao": "Brincalhona, dócil, companheira e dorminhoca",
        "imagem": "C:/Users/vetan/OneDrive/Área de Trabalho/imagens/Amora.jpeg"
    },

    {
        "nome": "Ralph",
        "idade": 5,
        "tipo": "Cachorro",
        "raça": "Pitbull",
        "descricao": "Calmo, medo de novas pessoas, reativo com alimentos e outros animais e carinhoso",
        "imagem": "C:/Users/vetan/OneDrive/Área de Trabalho/imagens/Ralph.jpeg"
    },

    {
        "nome": "Colar",
        "idade": 5,
        "tipo": "Cachorro",
        "raça": "Pitbull",
        "descricao": "Calmo, medo de novas pessoas e carinhosa",
        "imagem": "C:/Users/vetan/OneDrive/Área de Trabalho/imagens/Colar.jpeg"
    },

    {
        "nome": "Marido",
        "idade": 5,
        "tipo": "Gato",
        "raça": "SRD",
        "descricao": "Calmo, carinhoso e tem histórico de problemas urinários",
        "imagem": "C:/Users/vetan/OneDrive/Área de Trabalho/imagens/Marido.jpeg"
    },

    {
        "nome": "Linda",
        "idade": 10,
        "tipo": "Cachorro",
        "raça": "Pitbull",
        "descricao": "Calma, idosa e precisa de carinho e cuidados",
        "imagem": "C:/Users/vetan/OneDrive/Área de Trabalho/imagens/Linda.jpeg"
    },

    {
        "nome": "Bob",
        "idade": 9,
        "tipo": "Cachorro",
        "raça": "Pitbull",
        "descricao": "Calmo, medo de novas pessoas, reativo com alimentos e outros animais e carinhoso",
        "imagem": "c:\\Users\\vetan\\OneDrive\\Área de Trabalho\\imagens.pgn\\Bob.png.jpeg"
    },

    {
        "nome": "Lilico",
        "idade": 5,
        "tipo": "Gato",
        "raça": "SRD",
        "descricao": "Agitado, não convive com outros animais e se adapta lentamente",
        "imagem": "C:/Users/vetan/OneDrive/Área de Trabalho/imagens/Lilico.jpeg"
    },

    {
        "nome": "Willie",
        "idade": 6,
        "tipo": "Cachorro",
        "raça": "Pharaoh Hound",
        "descricao": "Calmo, educado e carinhoso",
        "imagem": "C:/Users/vetan/OneDrive/Área de Trabalho/imagens/Willie.jpeg"
    }
]

fila = []

# janela principal
janela = tk.Tk()
janela.title("Patinhas do Bem 🐾")
janela.geometry("390x844")
janela.configure(bg="#DFF5E1")

# limpar tela
def limpar():
    for widget in janela.winfo_children():
        widget.destroy()

# tela inicial
def tela_inicial():
    limpar()

    titulo = tk.Label(
        janela,
        text="Patinhas do Bem 🐾",
        font=("Arial", 22, "bold"),
        bg="#DFF5E1"
    )

    titulo.pack(pady=20)

    for pet in pets:

        # abrir imagem
        imagem = Image.open(pet["imagem"])

        # tamanho da imagem
        imagem = imagem.resize((150, 150))

        # converter para tkinter
        foto = ImageTk.PhotoImage(imagem)

        # card
        card = tk.Frame(
            janela,
            bg="white",
            bd=2,
            relief="ridge"
        )

        card.pack(pady=10)

        # imagem
        label_img = tk.Label(
            card,
            image=foto,
            bg="white"
        )

        label_img.image = foto
        label_img.pack(pady=5)

        # nome
        nome_pet = tk.Label(
            card,
            text=pet["nome"],
            font=("Arial", 14, "bold"),
            bg="white"
        )

        nome_pet.pack()

        # botão perfil
        botao = tk.Button(
            card,
            text="Ver perfil 🐾",
            bg="#A8E6CF",
            fg="black",
            font=("Arial", 10, "bold"),
            command=lambda p=pet: ver_pet(p)
        )

        botao.pack(pady=5)

# tela do pet
def ver_pet(pet):
    limpar()

    imagem_pet = Image.open(pet["imagem"])
    imagem_pet = imagem_pet.resize((200, 200))

    foto_pet = ImageTk.PhotoImage(imagem_pet)

    label_imagem = tk.Label(
        janela,
        image=foto_pet,
        bg="#DFF5E1"
    )

    label_imagem.image = foto_pet
    label_imagem.pack(pady=10)

    tk.Label(
        janela,
        text=pet["nome"],
        font=("Arial", 22, "bold"),
        bg="#DFF5E1"
    ).pack()

    tk.Label(
        janela,
        text=f"Idade: {pet['idade']} anos",
        bg="#DFF5E1",
        font=("Arial", 12)
    ).pack()

    tk.Label(
        janela,
        text=f"Raça: {pet['raça']}",
        bg="#DFF5E1",
        font=("Arial", 12)
    ).pack()

    tk.Label(
        janela,
        text=pet["descricao"],
        wraplength=300,
        justify="center",
        bg="#DFF5E1",
        font=("Arial", 11)
    ).pack(pady=15)

    tk.Button(
        janela,
        text="Quero adotar 🐾",
        bg="#FFB6C1",
        fg="white",
        font=("Arial", 11, "bold"),
        command=lambda: tela_cadastro(pet)
    ).pack(pady=10)

    tk.Button(
        janela,
        text="Voltar",
        bg="#A8E6CF",
        command=tela_inicial
    ).pack()

# tela cadastro
def tela_cadastro(pet):
    limpar()

    tk.Label(
        janela,
        text=f"Adoção de {pet['nome']} 🐾",
        font=("Arial", 18, "bold"),
        bg="#DFF5E1"
    ).pack(pady=20)

    tk.Label(
        janela,
        text="Digite seu nome:",
        bg="#DFF5E1"
    ).pack()

    nome = tk.Entry(
        janela,
        font=("Arial", 12)
    )

    nome.pack(pady=10)

    def enviar():
        fila.append({
            "pet": pet["nome"],
            "nome": nome.get()
        })

        tela_final()

    tk.Button(
        janela,
        text="Enviar cadastro",
        bg="#FFB6C1",
        fg="white",
        font=("Arial", 11, "bold"),
        command=enviar
    ).pack(pady=15)

# tela final
def tela_final():
    limpar()

    tk.Label(
        janela,
        text="Obrigado pelo cadastro! 🐾",
        font=("Arial", 18, "bold"),
        bg="#DFF5E1"
    ).pack(pady=30)

    tk.Label(
        janela,
        text="Entraremos em contato em breve.",
        bg="#DFF5E1",
        font=("Arial", 12)
    ).pack(pady=10)

    tk.Button(
        janela,
        text="Voltar ao início",
        bg="#A8E6CF",
        font=("Arial", 11, "bold"),
        command=tela_inicial
    ).pack(pady=20)

# iniciar app
tela_inicial()
def tela_inicial():
    limpar()

    titulo = tk.Label(
        janela,
        text="Patinhas do Bem 🐾",
        font=("Arial", 22, "bold"),
        bg="#DFF5E1"
    )

    titulo.pack(pady=15)

    for pet in pets:

        # card do pet
        card = tk.Frame(
            janela,
            bg="white",
            width=300,
            height=220,
            bd=2,
            relief="ridge"
        )

        card.pack(pady=10)
        card.pack_propagate(False)

        # abrir imagem
        imagem = Image.open(pet["imagem"])

        # tamanho padrão
        imagem = imagem.resize((100, 100))

        foto = ImageTk.PhotoImage(imagem)

        # imagem
        label_img = tk.Label(
            card,
            image=foto,
            bg="white"
        )

        label_img.image = foto
        label_img.pack(pady=8)

        # nome
        nome_pet = tk.Label(
            card,
            text=pet["nome"],
            font=("Arial", 14, "bold"),
            bg="F8FFF8"
        )

        nome_pet.pack()

        # botão
        botao = tk.Button(
            card,
            text="Ver Perfil 🐾",
            bg="#A8E6CF",
            fg="black",
            font=("Arial", 10, "bold"),
            command=lambda p=pet: ver_pet(p)
        )

        botao.pack(pady=8)

janela.mainloop()