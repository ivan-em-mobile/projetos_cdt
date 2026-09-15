# =============================================================================
# 🍔 SISTEMA DE HAMBURGUERIA EM CLI (TERMINAL)
# Linguagem: Python 3
# Bibliotecas: sqlite3, urllib.request, json, pwinput e os (para pastas)
# =============================================================================

import sqlite3
import json
import urllib.request
import pwinput  # 🔒 Biblioteca para mascarar senhas com asteriscos (****)
import os       # 📁 Módulo nativo para manipulação de pastas e caminhos

# -----------------------------------------------------------------------------
# PASSO 1: Configuração do Caminho e Banco de Dados (SQLite3)
# -----------------------------------------------------------------------------
# Definimos o nome da pasta onde o banco de dados será salvo.
# (Você pode alterar 'projetos_cdt_seunome' para o nome que desejar)
NOME_PASTA = "projetos_cdt_seunome"
NOME_BANCO = "hamburgueria_cli.db"

def conectar_banco():
    """
    Garante que a pasta exista e conecta ao banco de dados dentro dela.
    """
    # Cria a pasta caso ela ainda não exista na máquina
    os.makedirs(NOME_PASTA, exist_ok=True)
    
    # Define o caminho completo: projetos_cdt_seunome/hamburgueria_cli.db
    caminho_banco = os.path.join(NOME_PASTA, NOME_BANCO)
    
    # Conecta ao arquivo do banco na pasta indicada
    return sqlite3.connect(caminho_banco)

def inicializar_banco():
    """Cria as tabelas necessárias no banco de dados, caso não existam."""
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Tabela de Usuários (Clientes)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    
    # Tabela de Pedidos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            resumo_itens TEXT NOT NULL,
            endereco TEXT NOT NULL,
            forma_pagamento TEXT NOT NULL,
            valor_total REAL NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)
    
    # Tabela de Avaliações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nota INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)
    
    conexao.commit()
    conexao.close()

# -----------------------------------------------------------------------------
# PASSO 2: Integração com API Externa (ViaCEP)
# -----------------------------------------------------------------------------
def buscar_endereco_por_cep(cep):
    """
    Consome a API do ViaCEP usando a biblioteca nativa urllib.
    Retorna um dicionário com o endereço ou None se falhar.
    """
    cep_limpo = "".join(filter(str.isdigit, cep))
    
    if len(cep_limpo) != 8:
        return None

    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    
    try:
        requisicao = urllib.request.urlopen(url)
        dados = json.loads(requisicao.read().decode('utf-8'))
        
        if "erro" in dados:
            return None
        return dados
    except Exception:
        return None

# -----------------------------------------------------------------------------
# PASSO 3: Módulo de Autenticação (Com Senha Mascarada em ****)
# -----------------------------------------------------------------------------
def cadastrar_usuario():
    """Cadastra um novo usuário no sistema com senha exibida em ****."""
    print("\n--- 📝 TELA DE CADASTRO ---")
    nome = input("Digite seu nome completo: ").strip()
    email = input("Digite seu e-mail: ").strip().lower()
    
    # pwinput mascara cada caractere digitado com '*'
    senha = pwinput.pwinput(prompt="Digite sua senha: ", mask="*").strip()

    if not nome or not email or not senha:
        print("❌ [ERRO] Todos os campos devem ser preenchidos!")
        return

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        conexao.commit()
        conexao.close()
        print("✅ Cadastro realizado com sucesso! Faça login para continuar.")
    except sqlite3.IntegrityError:
        print("❌ [ERRO] Este e-mail já está cadastrado no sistema!")

def fazer_login():
    """Autentica o usuário com senha exibida em ****."""
    print("\n--- 🔑 TELA DE LOGIN ---")
    email = input("E-mail: ").strip().lower()
    
    # pwinput mascara cada caractere digitado com '*'
    senha = pwinput.pwinput(prompt="Senha: ", mask="*").strip()

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    usuario = cursor.fetchone()
    conexao.close()

    if usuario:
        print(f"\n✅ Bem-vindo(a) de volta, {usuario[1]}!")
        return {"id": usuario[0], "nome": usuario[1]}
    else:
        print("❌ [ERRO] E-mail ou senha incorretos!")
        return None

# -----------------------------------------------------------------------------
# PASSO 4: Módulo do Cardápio e Vendas
# -----------------------------------------------------------------------------
CARDAPIO = {
    1: {"nome": "Combo Smash Burguer (Hambúrguer + Batata)", "preco": 28.00},
    2: {"nome": "Combo Bacon Salad (Hambúrguer + Batata)", "preco": 32.00},
    3: {"nome": "Combo Monster Double (2 Carnes + Batata)", "preco": 38.00},
    4: {"nome": "Refrigerante Lata 350ml", "preco": 6.00},
    5: {"nome": "Suco Natural 500ml", "preco": 8.00},
    6: {"nome": "Milkshake de Chocomaltado 400ml", "preco": 15.00}
}

def exibir_cardapio():
    """Exibe os itens disponíveis no cardápio."""
    print("\n" + "="*50)
    print(" 🍔 CARDÁPIO DA HAMBURGUERIA ")
    print("="*50)
    for codigo, item in CARDAPIO.items():
        print(f" [{codigo}] {item['nome']} - R$ {item['preco']:.2f}")
    print("="*50)

def gerenciar_carrinho(carrinho):
    """Exibe os itens no carrinho e calcula o total."""
    print("\n--- 🛒 SEU CARRINHO DE COMPRAS ---")
    if not carrinho:
        print("Seu carrinho está vazio!")
        return 0.0

    total = 0.0
    for idx, item in enumerate(carrinho, start=1):
        print(f" {idx}. {item['nome']} - R$ {item['preco']:.2f}")
        total += item['preco']
    
    print("-" * 35)
    print(f" Total parcial: R$ {total:.2f}")
    return total

def finalizar_pedido(usuario, carrinho):
    """Realiza o checkout, aplica cupom, busca o CEP e salva o pedido."""
    total = gerenciar_carrinho(carrinho)
    if total == 0:
        print("\n❌ Adicione pelo menos um item ao carrinho antes de finalizar!")
        return False

    cupom = input("\nPossui cupom de desconto? (ou aperte Enter para pular): ").strip().upper()
    if cupom == "DESCONTO10":
        desconto = total * 0.10
        total -= desconto
        print(f"🎉 Cupom 'DESCONTO10' aplicado com sucesso! Desconto de R$ {desconto:.2f}")
    elif cupom != "":
        print("⚠️ Cupom inválido! Prosseguindo sem desconto.")

    print("\n--- 📍 ENDEREÇO DE ENTREGA ---")
    while True:
        cep = input("Digite seu CEP (apenas números): ").strip()
        print("🔍 Buscando endereço...")
        dados_cep = buscar_endereco_por_cep(cep)
        
        if dados_cep:
            logradouro = dados_cep.get("logradouro", "")
            bairro = dados_cep.get("bairro", "")
            localidade = dados_cep.get("localidade", "")
            uf = dados_cep.get("uf", "")
            
            print(f"📍 Endereço encontrado: {logradouro}, {bairro} - {localidade}/{uf}")
            numero = input("Digite o número da residência / complemento: ").strip()
            endereco_formatado = f"{logradouro}, Nº {numero} - {bairro}, {localidade}/{uf} (CEP: {cep})"
            break
        else:
            print("❌ CEP não encontrado ou inválido. Tente novamente!")

    print("\n--- 💳 FORMA DE PAGAMENTO ---")
    print("1 - Cartão de Crédito/Débito")
    print("2 - PIX")
    print("3 - Dinheiro na Entrega")
    opcao_pagamento = input("Escolha a opção (1-3): ").strip()
    
    pagamentos = {"1": "Cartão", "2": "PIX", "3": "Dinheiro"}
    forma_pagamento = pagamentos.get(opcao_pagamento, "Cartão")

    resumo_itens = ", ".join([item['nome'] for item in carrinho])

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO pedidos (usuario_id, resumo_itens, endereco, forma_pagamento, valor_total)
        VALUES (?, ?, ?, ?, ?)
    """, (usuario["id"], resumo_itens, endereco_formatado, forma_pagamento, total))
    conexao.commit()
    conexao.close()

    print("\n" + "="*50)
    print(" 🎉 PEDIDO FINALIZADO COM SUCESSO! ")
    print(f" Total a pagar: R$ {total:.2f}")
    print(f" Forma de Pagamento: {forma_pagamento}")
    print(f" Entrega em: {endereco_formatado}")
    print("="*50)
    return True

def ver_historico_pedidos(usuario):
    """Consulta os pedidos salvos do usuário logado."""
    print("\n--- 📜 SEU HISTÓRICO DE PEDIDOS ---")
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, resumo_itens, valor_total, forma_pagamento, endereco
        FROM pedidos WHERE usuario_id = ?
    """, (usuario["id"],))
    pedidos = cursor.fetchall()
    conexao.close()

    if not pedidos:
        print("Você ainda não realizou nenhum pedido.")
        return

    for p in pedidos:
        print(f"\n📦 Pedido #{p[0]}")
        print(f"   Itens: {p[1]}")
        print(f"   Valor Total: R$ {p[2]:.2f}")
        print(f"   Pagamento: {p[3]}")
        print(f"   Endereço: {p[4]}")
        print("-" * 40)

def avaliar_sistema(usuario):
    """Registra uma nota de avaliação de 0 a 5."""
    print("\n--- ⭐ AVALIAÇÃO DO ESTABELECIMENTO ---")
    try:
        nota = int(input("Dê uma nota para o nosso atendimento (0 a 5): "))
        if 0 <= nota <= 5:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO avaliacoes (usuario_id, nota) VALUES (?, ?)", (usuario["id"], nota))
            conexao.commit()
            conexao.close()
            print("🌟 Muito obrigado pela sua avaliação!")
        else:
            print("❌ Por favor, digite um número de 0 a 5.")
    except ValueError:
        print("❌ Entrada inválida! Digite apenas números.")

# -----------------------------------------------------------------------------
# PASSO 5: Loop Principal do Sistema
# -----------------------------------------------------------------------------
def menu_cliente(usuario):
    """Menu exibido após o login bem-sucedido."""
    carrinho = []
    
    while True:
        print(f"\n=== PAINEL DO CLIENTE: {usuario['nome'].upper()} ===")
        print("1 - Ver Cardápio & Adicionar Item")
        print("2 - Ver Carrinho de Compras")
        print("3 - Finalizar Pedido (Checkout)")
        print("4 - Ver Histórico de Pedidos")
        print("5 - Avaliar o Estabelecimento")
        print("6 - Sair da Conta (Logout)")
        
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            exibir_cardapio()
            try:
                cod = int(input("Digite o código do item para adicionar (0 para voltar): "))
                if cod in CARDAPIO:
                    carrinho.append(CARDAPIO[cod])
                    print(f"✅ '{CARDAPIO[cod]['nome']}' adicionado ao carrinho!")
                elif cod == 0:
                    continue
                else:
                    print("❌ Código de item inválido!")
            except ValueError:
                print("❌ Por favor, digite um número válido.")

        elif opcao == "2":
            gerenciar_carrinho(carrinho)

        elif opcao == "3":
            if finalizar_pedido(usuario, carrinho):
                carrinho.clear()

        elif opcao == "4":
            ver_historico_pedidos(usuario)

        elif opcao == "5":
            avaliar_sistema(usuario)

        elif opcao == "6":
            print("\nSaindo da conta... Até logo!")
            break
        else:
            print("❌ Opção inválida! Escolha entre 1 e 6.")

def main():
    """Ponto de entrada do sistema."""
    inicializar_banco()
    
    while True:
        print("\n==========================================")
        print(" 🍔 BEM-VINDO À HAMBURGUERIA (CLI) ")
        print("==========================================")
        print("1 - Fazer Login")
        print("2 - Cadastrar Nova Conta")
        print("3 - Sair do Sistema")
        
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            usuario = fazer_login()
            if usuario:
                menu_cliente(usuario)
        elif opcao == "2":
            cadastrar_usuario()
        elif opcao == "3":
            print("\nObrigado por utilizar o nosso sistema. Até a próxima!")
            break
        else:
            print("❌ Opção inválida! Escolha entre 1 e 3.")

# Execução do Programa
if __name__ == "__main__":
    main()