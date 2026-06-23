import sqlite3

conn = sqlite3.connect("cafeteria.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM produtos")  # evita duplicar

produtos = [
    # ☕ CAFÉS
    ("Café Expresso Paris", 5.0, "Café", "expresso.jpg"),
    ("Cappuccino Cremoso", 8.0, "Café", "cappuccino.webp"),
    ("Latte Vanilla", 9.0, "Café", "latte.jpg"),
    ("Mocha Chocolate Belga", 10.0, "Café", "mocha.jpg"),
    ("Café com Chantilly", 9.0, "Café", "chantilly.jpg"),

    # 🥐 BOULANGERIE (clima parisiense)
    ("Croissant Butter", 7.0, "Doces", "croissant.webp"),
    ("Pain au Chocolat", 8.0, "Doces", "pain_choco.jpg"),
    ("Tarte aux Fraises", 12.0, "Doces", "tarte_fraise.webp"),
    ("Macarons Sortidos", 14.0, "Doces", "macarons.jpg"),
    ("Éclair de Chocolate", 11.0, "Doces", "eclair.jpg"),

    # 🍰 DOCES ARTESANAIS
    ("Cheesecake de Frutas Vermelhas", 13.0, "Doces", "cheesecake.jpg"),
    ("Brownie Gourmet", 10.0, "Doces", "brownie.jpg"),
    ("Madeleine Tradicional", 6.0, "Doces", "madeleine.jpg"),

    # 🥪 SALGADOS LEVES
    ("Sanduíche de Brie e Mel", 12.0, "Salgados", "brie_mel.jpg"),
    ("Quiche Lorraine", 11.0, "Salgados", "quiche.jpg"),
    ("Croissant de Presunto e Queijo", 9.0, "Salgados", "croissant_salgado.webp"),

    # 🥤 BEBIDAS FRIAS
    ("Iced Coffee Paris", 8.0, "Bebidas", "iced_coffee.jpg"),
    ("Limonade Francesa", 7.0, "Bebidas", "limonade.jpg"),
    ("Chá de Frutas Vermelhas", 6.0, "Bebidas", "cha.jpg"),
]


cursor.executemany(
    "INSERT INTO produtos (nome, preco, categoria, imagem) VALUES (?, ?, ?, ?)",
    produtos
)

conn.commit()
conn.close()

print("Cardápio inserido!")