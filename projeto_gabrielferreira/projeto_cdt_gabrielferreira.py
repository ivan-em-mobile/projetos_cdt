import sqlite3
import os
from datetime import datetime
import random 

# =====================================================================
# 1. CONFIGURAÇÃO DO BANCO DE DADOS (In-Memory para teste rápido)
# =====================================================================
conn = sqlite3.connect(':memory:')  
cursor = conn.cursor()

# Criação das tabelas
cursor.executescript('''
CREATE TABLE categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_categoria TEXT NOT NULL
);

CREATE TABLE produtos (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    id_categoria INTEGER,
    nome TEXT NOT NULL,
    preco REAL NOT NULL, 
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

CREATE TABLE mesas (
    id_mesa INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_mesa INTEGER UNIQUE NOT NULL,
    status TEXT DEFAULT 'Livre'
);

CREATE TABLE comandas (
    id_comanda INTEGER PRIMARY KEY AUTOINCREMENT,
    id_mesa INTEGER,
    quantidade_pessoas INTEGER NOT NULL,
    preco_rodizio_por_pessoa REAL NOT NULL,
    status_comanda TEXT DEFAULT 'Aberta',
    FOREIGN KEY (id_mesa) REFERENCES mesas(id_mesa)
);

CREATE TABLE itens_pedidos (
    id_item_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_comanda INTEGER,
    id_produto INTEGER,
    quantidade REAL NOT NULL, 
    valor_unitario REAL NOT NULL,
    FOREIGN KEY (id_comanda) REFERENCES comandas(id_comanda),
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);
''')

# Carga inicial de dados
cursor.executescript('''
INSERT INTO categorias (nome_categoria) VALUES ('Rodízio'), ('Bebidas'), ('Sobremesas');

INSERT INTO produtos (id_categoria, nome, preco) VALUES 
(1, 'Picanha', 0.00),
(1, 'Coração de Frango', 0.00),
(1, 'Cupim', 0.00),
(1, 'Costela Premium', 0.00),
(1, 'Paleta de Cordeiro', 0.00),
(1, 'Queijo Coalho com Melaço', 0.00),
(2, 'Água Mineral', 5.00),
(2, 'Refrigerante lata', 7.50),
(2, 'Cerveja 0.0%', 9.00),
(2, 'Suco Natural de Laranja', 10.00),
(2, 'Chopp Artesanal 300ml', 12.00),
(3, 'Pudim (Preço por Kg)', 60.00),      
(3, 'Grand Gateau (Preço por Kg)', 85.00);

INSERT INTO mesas (numero_mesa) VALUES 
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10),
(11), (12), (13), (14), (15), (16), (17), (18), (19), (20);
''')
conn.commit()

VALOR_RODIZIO_PADRAO = 89.90

# =====================================================================
# 2. LÓGICA DE NEGÓCIO DO RODÍZIO
# =====================================================================

def abrir_mesa():
    print("\n--- ABRIR NOVA MESA ---")
    try:
        num_mesa = int(input("Número da mesa (1 a 20): "))
        
        cursor.execute("SELECT status FROM mesas WHERE numero_mesa = ?", (num_mesa,))
        mesa = cursor.fetchone()
        
        if not mesa:
            print("❌ Mesa não encontrada. Escolha de 1 a 20.")
            return
            
        if mesa[0] == 'Ocupada':
            print("❌ Esta mesa já está ocupada!")
            return
            
        pessoas = int(input("Quantidade de pessoas na mesa (Máximo 10): "))
        if pessoas <= 0:
            print("❌ Quantidade inválida.")
            return
        if pessoas > 10:
            print("❌ Limite excedido! Máximo 10 pessoas por mesa.")
            return

        cursor.execute("UPDATE mesas SET status = 'Ocupada' WHERE numero_mesa = ?", (num_mesa,))
        cursor.execute("""
            INSERT INTO comandas (id_mesa, quantidade_pessoas, preco_rodizio_por_pessoa) 
            VALUES ((SELECT id_mesa FROM mesas WHERE numero_mesa = ?), ?, ?)
        """, (num_mesa, pessoas, VALOR_RODIZIO_PADRAO))
        
        conn.commit()
        print(f"✅ Mesa {num_mesa} aberta com sucesso para {pessoas} pessoas!")
    except ValueError:
        print("❌ Entrada inválida. Digite apenas números.")

def lancar_pedido():
    print("\n--- LANÇAR PEDIDO ---")
    try:
        num_mesa = int(input("Número da mesa: "))
        
        cursor.execute("""
            SELECT c.id_comanda FROM comandas c 
            JOIN mesas m ON c.id_mesa = m.id_mesa 
            WHERE m.numero_mesa = ? AND c.status_comanda = 'Aberta'
        """, (num_mesa,))
        comanda = cursor.fetchone()
        
        if not comanda:
            print("❌ Não há comanda aberta para esta mesa.")
            return
            
        id_comanda = comanda[0]
        
        print("\n--- CARDÁPIO ---")
        cursor.execute("SELECT id_produto, id_categoria, nome, preco FROM produtos")
        produtos = cursor.fetchall()
        for p in produtos:
            if p[3] == 0:
                preco_str = "Incluso no Rodízio"
            elif p[1] == 3: # Categoria 3 = Sobremesas por KG
                preco_str = f"R$ {p[3]:.2f}/kg" 
            else:           # Categoria 2 = Bebidas por Unidade
                preco_str = f"R$ {p[3]:.2f}/un"
            print(f"[{p[0]}] {p[2]} - {preco_str}")
            
        id_prod = int(input("\nCódigo do produto: "))
        
        # CORRIGIDO: Busca a categoria antes para fazer a pergunta certa ao usuário
        cursor.execute("SELECT nome, preco, id_categoria FROM produtos WHERE id_produto = ?", (id_prod,))
        prod_data = cursor.fetchone()
        
        if not prod_data:
            print("❌ Produto inválido.")
            return
            
        nome_prod, preco_unitario, id_categoria = prod_data
        
        # CORRIGIDO: Se for sobremesa pede o peso, se for bebida/rodízio pede quantidade inteira
        if id_categoria == 3:
            qtd = float(input("Digite o peso (em kg, use ponto. Ex: 0.350): "))
        else:
            qtd = float(int(input("Digite a quantidade (unidades inteiras): ")))
        
        if qtd <= 0:
            print("❌ Quantidade/Peso inválido.")
            return
        
        cursor.execute("""
            INSERT INTO itens_pedidos (id_comanda, id_produto, quantidade, valor_unitario)
            VALUES (?, ?, ?, ?)
        """, (id_comanda, id_prod, qtd, preco_unitario))
        
        conn.commit()
        
        # CORRIGIDO: Exibição textual alinhada com a categoria do produto lançado
        if id_categoria == 3:
            print(f"✅ {qtd:.3f}kg de '{nome_prod}' adicionado à Mesa {num_mesa}!")
        else:
            print(f"✅ {int(qtd)}un de '{nome_prod}' adicionado à Mesa {num_mesa}!")
        
        if id_categoria == 1:
            tempo_base = random.randint(2, 5)  
            tipo_preparo = "Próximo passador chegando em"
        elif id_categoria == 2:
            tempo_base = random.randint(1, 3)  
            tipo_preparo = "Tempo estimado de entrega do Bar:"
        else:
            tempo_base = random.randint(5, 10) 
            tipo_preparo = "Tempo de montagem na cozinha:"
            
        print(f"⏳ [LOG COZINHA] {tipo_preparo} {tempo_base} minutos.")
        if preco_unitario > 0:
            print(f"💵 Valor parcial deste item: R$ {(preco_unitario * qtd):.2f}")
            
    except ValueError:
        print("❌ Entrada inválida. Digite valores numéricos válidos.")

def fechar_conta():
    print("\n--- FECHAR CONTA ---")
    try:
        num_mesa = int(input("Número da mesa: "))
        
        cursor.execute("""
            SELECT c.id_comanda, c.quantidade_pessoas, c.preco_rodizio_por_pessoa 
            FROM comandas c 
            JOIN mesas m ON c.id_mesa = m.id_mesa 
            WHERE m.numero_mesa = ? AND c.status_comanda = 'Aberta'
        """, (num_mesa,))
        comanda = cursor.fetchone()
        
        if not comanda:
            print("❌ Nenhuma comanda aberta para esta mesa.")
            return
            
        id_comanda, qtd_pessoas, valor_rodizio = comanda
        total_rodizio = qtd_pessoas * valor_rodizio
        
        print("\n==========================================")
        print(f"            CONTA MESA {num_mesa}             ")
        print("==========================================")
        print(f"{qtd_pessoas}x Rodízio (R$ {valor_rodizio:.2f}/pess) : R$ {total_rodizio:.2f}")
        print("------------------------------------------")
        print("Itens adicionais consumidos:")
        
        cursor.execute("""
            SELECT p.nome, ip.quantidade, ip.valor_unitario, p.id_categoria 
            FROM itens_pedidos ip
            JOIN produtos p ON ip.id_produto = p.id_produto
            WHERE ip.id_comanda = ?
        """, (id_comanda,))
        itens = cursor.fetchall()
        
        total_extras = 0.0
        for item in itens:
            nome, qtd, preco, id_cat = item
            subtotal_item = qtd * preco 
            total_extras += subtotal_item
            
            if preco == 0:
                preco_exibicao = "Incluso"
            else:
                preco_exibicao = f"R$ {subtotal_item:.2f}"
            
            # CORRIGIDO: Agora formata estritamente Categoria 3 como kg e o resto como unidade (un)
            if id_cat == 3:
                print(f" - {qtd:.3f}kg {nome}: {preco_exibicao} (R$ {preco:.2f}/kg)")
            else:
                print(f" - {int(qtd)}un {nome}: {preco_exibicao}")
            
        total_geral = total_rodizio + total_extras
        taxa_servico = total_geral * 0.10
        total_com_taxa = total_geral + taxa_servico
        
        print("------------------------------------------")
        print(f"Subtotal Consumo        : R$ {total_geral:.2f}")
        print(f"Taxa de Serviço (10%)   : R$ {taxa_servico:.2f}")
        print(f"TOTAL DA CONTA          : R$ {total_com_taxa:.2f}")
        print(f"Valor por pessoa ({qtd_pessoas}p) : R$ {(total_com_taxa/qtd_pessoas):.2f}")
        print("==========================================")
        
        confirmar = input("Confirmar pagamento e liberar mesa? (S/N): ").upper()
        if confirmar == 'S':
            cursor.execute("UPDATE comandas SET status_comanda = 'Paga' WHERE id_comanda = ?", (id_comanda,))
            cursor.execute("UPDATE mesas SET status = 'Livre' WHERE numero_mesa = ?", (num_mesa,))
            conn.commit()
            print("✅ Conta paga! Mesa liberada.")
        else:
            print("⚠️ Conta mantida aberta.")
            
    except ValueError:
        print("❌ Entrada inválida.")

def menu():
    while True:
        print("\n=== SISTEMA DE RODÍZIO CHIQUE ===")
        print("[1] Abrir Mesa (Check-in)")
        print("[2] Lançar Pedido (Cozinha/Bar)")
        print("[3] Fechar Conta (Check-out)")
        print("[4] Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            abrir_mesa()
        elif opcao == '2':
            lancar_pedido()
        elif opcao == '3':
            fechar_conta()
        elif opcao == '4':
            print("Saindo do sistema... Até logo!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")

if __name__ == '__main__':
    menu()
