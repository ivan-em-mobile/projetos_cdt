import tkinter as tk
from PIL import Image, ImageTk

# dados{
pets = [
    {
        "nome": "Amora",
        "idade": 5,
        "tipo": "Cachorro",
        "raça": "Pitbull",
        "descricao": "Brincalhona, docil, companheira e dorminhoca",
        "imagem": "imagens/Amora.png"
    },

    {
        "nome": "Ralph",
        "idade": 5,
        "tipo": "Cachorro",
        "raça": "Pitbull",
        "descricao": "Calmo, medo de novas pessoas, reativo com alimentos e outros animais e carinhoso",
        "imagem": "imagens/Ralph.png"
    },

    {
        "nome": "Colar",
        "idade": 5,
        "tipo": "Cachorro",
        "raça": "Pitbull",
        "descricao": "Calmo, medo de novas pessoas, carinhosa",
        "imagem": "imagens/Colar.png"
    },

    {
        "nome": "Marido",
        "idade": 5,
        "tipo": "Gato",
        "raça": "SRD",
        "descricao": "Calmo, medo de novas pessoas, carinhoso e tem histórico de problemas urinários",
        "imagem": "imagens/Marido.png"
    },

    {
        "nome": "Linda",
        "idade": 10,
        "tipo": "Cachorro",
        "raça": "Pitbull",
        "descricao": "Calma, idosa e precisa de carinho e cuidados",
        "imagem": "imagens/Linda.png"
    },

    {
        "nome": "Bob",
        "idade": 9,
        "tipo": "Cachorro",
        "raça": "Pitbull",
        "descricao": "Calmo, medo de novas pessoas, reativo com alimentos e outros animais e carinhoso",
        "imagem": "imagens/Bob.png"
    },

    {
        "nome": "Lilico",
        "idade": 5,
        "tipo": "Gato",
        "raça": "SRD",
        "descricao": "Agitado, não convive com outros animais, medo de novas pessoas e se adapta lentamente a novos ambientes",
        "imagem": "imagens/Lilico.png"
    },

    {
        "nome": "Willie",
        "idade": 6,
        "tipo": "Cachorro",
        "raça": "Pharaoh hound",
        "descricao": "Calmo, educado e carinhoso",
        "imagem": "imagens/Willie.png"
    }
     
     ]
fila = []

# janela
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
    
    tk.Label(janela, text="Patinhas do Bem 🐾", font=("Arial", 16)).pack(pady=10)

    for pet in pets:
        tk.Button(janela, text=pet["nome"],
                  command=lambda p=pet: ver_pet(p)).pack(pady=5)

# tela pet
def ver_pet(pet):
    
    limpar()

    imagem_pet = Image.open(pet["imagem"])
    imagem_pet = imagem_pet.resize((180, 180))

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
        font=("Arial", 20, "bold"),
        bg="#DFF5E1"
    ).pack()

    tk.Label(
        janela,
        text=f"Idade: {pet['idade']} anos",
        bg="#DFF5E1"
    ).pack()

    tk.Label(
        janela,
        text=f"Raça: {pet['raça']}",
        bg="#DFF5E1"
    ).pack()

    tk.Label(
        janela,
        text=pet["descricao"],
        wraplength=300,
        justify="center",
        bg="#DFF5E1"
    ).pack(pady=10)

    tk.Button(
        janela,
        text="Quero adotar 🐾",
        command=lambda: tela_cadastro(pet)
    ).pack(pady=10)

# cadastro
def tela_cadastro(pet):
    limpar()

    tk.Label(janela, text="Seu nome").pack()
    nome = tk.Entry(janela)
    nome.pack()

    def enviar():
        fila.append({"pet": pet["nome"], "nome": nome.get()})
        tela_final()

    tk.Button(janela, text="Enviar", command=enviar).pack(pady=10)

# final
def tela_final():
    limpar()

    tk.Label(janela, text="Obrigado! 🐾").pack(pady=20)

    tk.Button(janela, text="Voltar",
              command=tela_inicial).pack()

# iniciar
tela_inicial()
janela.mainloop() 