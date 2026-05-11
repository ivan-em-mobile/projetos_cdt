import tkinter as tk

# dados
pets = [
    {"nome": "Amora", "idade": 5, "tipo": "Cachorro", "raça": "Pitbull", "descricao": "Brincalhona, docil, companheira e dorminhoca"},
    {"nome": "Ralph", "idade": 5, "tipo": "Cachorro", "raça": "Pitbull", "descricao": "Calmo, medo de novas pessoas, reativo com alimentos e outros animais e carinhoso"},
    {"nome": "Colar", "idade": 5, "tipo": "Cachorro", "raça": "Pitbull", "descricao": "Calmo, medo de novas pessoas, reativo com alimentos e outros animais e carinhoso"},
    {"nome": "Amora", "idade": 5, "tipo": "Cachorro", "raça": "Pitbull", "descricao": "Calmo, medo de novas pessoas, reativo com alimentos e outros animais e carinhoso"},
    {"nome": "Linda", "idade": 10, "tipo": "Cachorro", "raça": "Pitbull", "descricao": "Calmo, medo de novas pessoas, reativo com alimentos e outros animais e carinhoso"},
    {"nome": "Bob", "idade": 9, "tipo": "Cachorro", "raça": "Pitbull", "descricao": "Calmo, medo de novas pessoas, reativo com alimentos e outros animais e carinhoso"},
    {"nome": "Lilico", "idade": 5, "tipo": "Gato", "raça": "SRD", "descricao": "Calmo, medo de novas pessoas, reativo com alimentos e outros animais e carinhoso"}
]
fila = []

# janela
janela = tk.Tk()
janela.title("Patinhas do Bem 🐾")
janela.geometry("300x640")

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

    tk.Label(janela, text=pet["nome"], font=("Arial", 14)).pack()
    tk.Label(janela, text=f"Idade: {pet['idade']}").pack()
    tk.Label(janela, text=pet["descricao"]).pack()

    tk.Button(janela, text="Quero adotar",
              command=lambda: tela_cadastro(pet)).pack(pady=10)

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