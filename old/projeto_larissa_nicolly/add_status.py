id="o1ix8r"
import sqlite3

conn = sqlite3.connect("cafeteria.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE pedidos
ADD COLUMN status TEXT DEFAULT 'Recebido'
""")

conn.commit()
conn.close()

print("Coluna status adicionada com sucesso!")
