import tkinter as tk
from tkinter import messagebox
import sqlite3
import requests

# aqui, faz a conexão com o banco de dados
conexao = sqlite3.connect("hamburgueria.db")
cursor = conexao.cursor()

# aqui, cria a tabela de usuários
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT UNIQUE,
    senha TEXT
)
""")

# aqui, cria a tabela de pedidos
cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT,
    itens TEXT,
    endereco TEXT,
    pagamento TEXT,
    total REAL
)
""")

# aqui, salva a alteração do bd
conexao.commit()

# aqui, é as variaveis, quando o usuario loga, adiciona no carrinho e o desconto
usuario_logado = None
carrinho = []
desconto = 0

# aqui, tem os combo, bebida, que quando clica, vai pro carrinho
combos = {
    "X Burguer": 15.0,
    "X Bacon": 18.0,
    "X Salada": 16.0,
    "X Egg": 17.0,
    "X Tudo": 22.0
}

# aqui, lista das bebidas da hamburgueria
bebidas = {
    "Coca-Cola": 6.0,
    "Pepsi": 5.5,
    "Guaraná": 5.0,
    "Suco": 7.0,
    "Água": 3.0
}

# aqui, cria uma função de adicionar no carrinho
def adicionar_ao_carrinho(item, preco):

    # aqui, adiciona as coisas no carrinho
    carrinho.append((item, preco))

    # aqui, quando o cliente clica, ja vai pro carinho
    messagebox.showinfo(
        "Carrinho",
        f"{item} adicionado!"
    )

# aqui, criou a função de cadastro, que quando o cliente cria uma conta, salva no bd
def cadastro():

    # aqui, criou a janela de cadastro
    janela_cadastro = tk.Toplevel(janela)
    janela_cadastro.title("Cadastro")
    janela_cadastro.geometry("300x250")

    # aqui, cria o campo do nome
    tk.Label(janela_cadastro, text="Nome").pack()
    entry_nome = tk.Entry(janela_cadastro)
    entry_nome.pack()

    # aqui, cria o campo do email
    tk.Label(janela_cadastro, text="Email").pack()
    entry_email = tk.Entry(janela_cadastro)
    entry_email.pack()

    # aqui, cria o campo da senha
    tk.Label(janela_cadastro, text="Senha").pack()
    entry_senha = tk.Entry(janela_cadastro, show="*")
    entry_senha.pack()

    # aqui, cria a função para salvar os dados
    def salvar():

        # aqui, pega os dados digitados
        nome = entry_nome.get()
        email = entry_email.get()
        senha = entry_senha.get()

        # aqui, verifica se os campos estão vazios
        if nome == "" or email == "" or senha == "":

            # aqui, mostra mensagem de erro
            messagebox.showwarning(
                "Erro",
                "Preencha todos os campos!"
            )
            return

        # aqui, tenta salvar no banco
        try:

            # aqui, insere os dados na tabela usuarios
            cursor.execute("""
            INSERT INTO usuarios (nome, email, senha)
            VALUES (?, ?, ?)
            """, (nome, email, senha))

            # aqui, salva alteração no banco
            conexao.commit()

            # aqui, mostra mensagem de sucesso
            messagebox.showinfo(
                "Sucesso",
                "Cadastro realizado!"
            )

            # aqui, fecha a janela
            janela_cadastro.destroy()

        except:

            # aqui, mostra erro caso email já exista
            messagebox.showerror(
                "Erro",
                "Email já cadastrado!"
            )

    # aqui, cria botão de cadastro
    tk.Button(
        janela_cadastro,
        text="Cadastrar",
        command=salvar
    ).pack(pady=10)

# aqui, cria a função de login
def login():

    # aqui, cria janela de login
    janela_login = tk.Toplevel(janela)
    janela_login.title("Login")
    janela_login.geometry("300x200")

    # aqui, cria campo de email
    tk.Label(janela_login, text="Email").pack()
    entry_email = tk.Entry(janela_login)
    entry_email.pack()

    # aqui, cria campo de senha
    tk.Label(janela_login, text="Senha").pack()
    entry_senha = tk.Entry(janela_login, show="*")
    entry_senha.pack()

    # aqui, verifica os dados do login
    def verificar():

        global usuario_logado

        # aqui, pega email e senha digitados
        email = entry_email.get()
        senha = entry_senha.get()

        # aqui, procura usuario no banco
        cursor.execute("""
        SELECT nome FROM usuarios
        WHERE email=? AND senha=?
        """, (email, senha))

        usuario = cursor.fetchone()

        # aqui, verifica se encontrou usuario
        if usuario:

            # aqui, salva o usuario logado
            usuario_logado = usuario[0]

            # aqui, mostra mensagem de boas vindas
            messagebox.showinfo(
                "Login",
                f"Bem-vindo, {usuario_logado}!"
            )

            # aqui, fecha janela de login
            janela_login.destroy()

        else:

            # aqui, mostra erro de login
            messagebox.showerror(
                "Erro",
                "Email ou senha incorretos!"
            )

    # aqui, cria botão de entrar
    tk.Button(
        janela_login,
        text="Entrar",
        command=verificar
    ).pack(pady=10)

# aqui, cria função do cupom
def cupom():

    global desconto

    # aqui, cria janela do cupom
    janela_cupom = tk.Toplevel(janela)
    janela_cupom.title("Cupom")
    janela_cupom.geometry("300x150")

    # aqui, texto da janela
    tk.Label(
        janela_cupom,
        text="Digite o cupom:"
    ).pack(pady=10)

    # aqui, campo do cupom
    entry_cupom = tk.Entry(janela_cupom)
    entry_cupom.pack()

    # aqui, aplica o desconto
    def aplicar():

        global desconto

        # aqui, pega o cupom digitado
        codigo = entry_cupom.get().upper()

        # aqui, verifica se o cupom existe
        if codigo == "DESCONTO10":

            # aqui, aplica desconto de 10%
            desconto = 10

            # aqui, mostra mensagem de sucesso
            messagebox.showinfo(
                "Cupom",
                "10% aplicado!"
            )

            # aqui, fecha janela
            janela_cupom.destroy()

        else:

            # aqui, mostra erro
            messagebox.showerror(
                "Erro",
                "Cupom inválido!"
            )

    # aqui, cria botão de aplicar
    tk.Button(
        janela_cupom,
        text="Aplicar",
        command=aplicar
    ).pack(pady=10)

# aqui, mostra os combos disponíveis
def mostrar_combos():

    # aqui, cria janela dos combos
    janela_combos = tk.Toplevel(janela)
    janela_combos.title("Combos")

    # aqui, percorre os combos
    for item, preco in combos.items():

        # aqui, cria botão de cada combo
        tk.Button(
            janela_combos,
            text=f"{item} - R$ {preco:.2f}",
            command=lambda i=item, p=preco:
            adicionar_ao_carrinho(i, p)
        ).pack(pady=5)

# aqui, mostra as bebidas disponíveis
def mostrar_bebidas():

    # aqui, cria janela das bebidas
    janela_bebidas = tk.Toplevel(janela)
    janela_bebidas.title("Bebidas")

    # aqui, percorre as bebidas
    for item, preco in bebidas.items():

        # aqui, cria botão de cada bebida
        tk.Button(
            janela_bebidas,
            text=f"{item} - R$ {preco:.2f}",
            command=lambda i=item, p=preco:
            adicionar_ao_carrinho(i, p)
        ).pack(pady=5)

# aqui, busca o endereço pelo cep
def buscar_cep(cep):

    try:

        # aqui, faz requisição para api via cep
        resposta = requests.get(
            f"https://viacep.com.br/ws/{cep}/json/"
        )

        # aqui, transforma resposta em json
        dados = resposta.json()

        # aqui, verifica se o cep existe
        if "erro" in dados:
            return None

        # aqui, retorna os dados do endereço
        return dados

    except:

        # aqui, retorna none caso dê erro
        return None

# aqui, finaliza o pedido
def finalizar_pedido():

    global desconto

    # aqui, verifica se o usuario fez login
    if not usuario_logado:

        messagebox.showwarning(
            "Login",
            "Faça login primeiro!"
        )

        return

    # aqui, verifica se o carrinho está vazio
    if len(carrinho) == 0:

        messagebox.showwarning(
            "Carrinho",
            "Carrinho vazio!"
        )

        return

    # aqui, cria janela de finalizar pedido
    janela_pedido = tk.Toplevel(janela)
    janela_pedido.title("Finalizar Pedido")
    janela_pedido.geometry("400x500")

    # aqui, cria os campos do endereço
    tk.Label(janela_pedido, text="CEP").pack()
    entry_cep = tk.Entry(janela_pedido)
    entry_cep.pack()

    tk.Label(janela_pedido, text="Rua").pack()
    entry_rua = tk.Entry(janela_pedido, width=40)
    entry_rua.pack()

    tk.Label(janela_pedido, text="Bairro").pack()
    entry_bairro = tk.Entry(janela_pedido, width=40)
    entry_bairro.pack()

    tk.Label(janela_pedido, text="Cidade").pack()
    entry_cidade = tk.Entry(janela_pedido, width=40)
    entry_cidade.pack()

    tk.Label(janela_pedido, text="Número").pack()
    entry_numero = tk.Entry(janela_pedido)
    entry_numero.pack()

    # aqui, cria texto da forma de pagamento
    tk.Label(
        janela_pedido,
        text="Forma de Pagamento"
    ).pack()

    # aqui, define pagamento padrão
    pagamento = tk.StringVar()
    pagamento.set("Pix")

    # aqui, cria menu de pagamento
    tk.OptionMenu(
        janela_pedido,
        pagamento,
        "Pix",
        "Cartão",
        "Dinheiro"
    ).pack()

    # aqui, busca cep
    def consultar():

        # aqui, pega cep digitado
        cep = entry_cep.get()

        # aqui, chama função de busca
        endereco = buscar_cep(cep)

        # aqui, verifica se encontrou endereço
        if endereco:

            # aqui, preenche rua
            entry_rua.delete(0, tk.END)
            entry_rua.insert(0, endereco["logradouro"])

            # aqui, preenche bairro
            entry_bairro.delete(0, tk.END)
            entry_bairro.insert(0, endereco["bairro"])

            # aqui, preenche cidade
            entry_cidade.delete(0, tk.END)
            entry_cidade.insert(0, endereco["localidade"])

            # aqui, mostra mensagem de sucesso
            messagebox.showinfo(
                "CEP",
                "Endereço encontrado!"
            )

        else:

            # aqui, mostra erro do cep
            messagebox.showerror(
                "Erro",
                "CEP inválido!"
            )

    # aqui, cria botão buscar cep
    tk.Button(
        janela_pedido,
        text="Buscar CEP",
        command=consultar,
        bg="#6c4300",
        fg="white"
    ).pack(pady=10)

    # aqui, confirma o pedido
    def confirmar():

        # aqui, pega os dados do endereço
        rua = entry_rua.get()
        numero = entry_numero.get()
        bairro = entry_bairro.get()
        cidade = entry_cidade.get()

        # aqui, verifica se o endereço foi preenchido
        if rua == "" or numero == "":

            messagebox.showwarning(
                "Erro",
                "Preencha o endereço!"
            )
            return

        # aqui, cria variaveis do pedido
        itens = ""
        total = 0

        # aqui, percorre itens do carrinho
        for item, preco in carrinho:

            itens += f"{item} - R$ {preco:.2f}\n"
            total += preco

        # aqui, aplica desconto se existir
        if desconto > 0:

            valor_desconto = total * (desconto / 100)
            total -= valor_desconto

        # aqui, monta endereço completo
        endereco = f"""
{rua}, {numero}
{bairro} - {cidade}
"""

        # aqui, salva pedido no banco
        cursor.execute("""
        INSERT INTO pedidos
        (cliente, itens, endereco, pagamento, total)
        VALUES (?, ?, ?, ?, ?)
        """, (
            usuario_logado,
            itens,
            endereco,
            pagamento.get(),
            total
        ))

        # aqui, salva alterações
        conexao.commit()

        # aqui, cria resumo do pedido
        resumo = f"""
PEDIDO CONFIRMADO

Cliente:
{usuario_logado}

Itens:
{itens}

Endereço:
{endereco}

Pagamento:
{pagamento.get()}

Tempo estimado:
40 minutos

Total:
R$ {total:.2f}
"""

        # aqui, mostra resumo do pedido
        messagebox.showinfo(
            "Pedido",
            resumo
        )

        # aqui, limpa carrinho
        carrinho.clear()

        # aqui, fecha janela
        janela_pedido.destroy()

    # aqui, cria botão de confirmar pedido
    tk.Button(
        janela_pedido,
        text="Confirmar Pedido",
        bg="green",
        fg="white",
        command=confirmar
    ).pack(pady=20)

# aqui, cria função de avaliação
def avaliacao():

    # aqui, cria janela de avaliação
    janela_av = tk.Toplevel(janela)
    janela_av.title("Avaliação")
    janela_av.geometry("300x200")

    # aqui, cria texto da nota
    tk.Label(
        janela_av,
        text="Nota de 0 a 5"
    ).pack(pady=10)

    # aqui, cria campo da nota
    entry = tk.Entry(janela_av)
    entry.pack()

    # aqui, envia avaliação
    def enviar():

        # aqui, pega nota digitada
        nota = entry.get()

        # aqui, verifica se a nota é válida
        if nota in ["0", "1", "2", "3", "4", "5"]:

            # aqui, mostra mensagem de sucesso
            messagebox.showinfo(
                "Obrigado",
                "Avaliação enviada!"
            )

            # aqui, fecha janela
            janela_av.destroy()

        else:

            # aqui, mostra erro
            messagebox.showerror(
                "Erro",
                "Nota inválida!"
            )

    # aqui, cria botão de enviar avaliação
    tk.Button(
        janela_av,
        text="Enviar",
        command=enviar
    ).pack(pady=10)

# aqui, cria janela principal
janela = tk.Tk()
janela.title("Hamburgueria")
janela.geometry("400x550")
janela.configure(bg="#6c4300")

# aqui, cria titulo da hamburgueria
titulo = tk.Label(
    janela,
    text="Hamburgueria",
    font=("Arial", 18, "bold"),
    bg="#6c4300",
    fg="black"
)

titulo.pack(pady=15)

# aqui, cria botão de cadastro
tk.Button(
    janela,
    text="Cadastro",
    width=30,
    command=cadastro
).pack(pady=5)

# aqui, cria botão de login
tk.Button(
    janela,
    text="Login",
    width=30,
    command=login
).pack(pady=5)

# aqui, cria botão do cupom
tk.Button(
    janela,
    text="Cupom de Desconto",
    width=30,
    command=cupom
).pack(pady=5)

# aqui, cria botão dos combos
tk.Button(
    janela,
    text="Combos",
    width=30,
    command=mostrar_combos
).pack(pady=5)

# aqui, cria botão das bebidas
tk.Button(
    janela,
    text="Bebidas",
    width=30,
    command=mostrar_bebidas
).pack(pady=5)

# aqui, cria botão de finalizar pedido
tk.Button(
    janela,
    text="Carrinho / Finalizar Pedido",
    width=30,
    command=finalizar_pedido
).pack(pady=5)

# aqui, cria botão de avaliação
tk.Button(
    janela,
    text="Avaliação",
    width=30,
    command=avaliacao
).pack(pady=5)

# aqui, cria botão de sair
tk.Button(
    janela,
    text="Sair",
    width=30,
    command=janela.destroy
).pack(pady=20)

# aqui, mantém a janela rodando
janela.mainloop()

# aqui, fecha conexão com banco de dados
conexao.close()