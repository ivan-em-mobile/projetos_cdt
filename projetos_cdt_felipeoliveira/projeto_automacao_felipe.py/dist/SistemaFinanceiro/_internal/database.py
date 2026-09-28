import os
import sqlite3

# Define o caminho absoluto para evitar erros de escrita no Linux/Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "monitor_data.db")

def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metas_financeiras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                valor_alvo REAL NOT NULL,
                valor_atual REAL DEFAULT 0.0,
                data_limite TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                moeda_origem TEXT,
                moeda_destino TEXT,
                valor_origem REAL,
                valor_convertido REAL,
                taxa REAL,
                data_conversao TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alertas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                alvo TEXT,
                preco_alvo REAL,
                ativo INTEGER DEFAULT 1
            )
        """)
        conn.commit()