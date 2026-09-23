import os
import sqlite3
import requests
import webbrowser
from datetime import datetime
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Garante que o banco seja criado SEMPRE na mesma pasta do app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "database.db")

# Suporte a requisições CORS
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Rota principal para carregar o frontend
@app.route("/")
def home():
    return render_template("index.html")

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS musicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            artista TEXT NOT NULL,
            album TEXT,
            duracao TEXT,
            humor TEXT NOT NULL,
            clima TEXT NOT NULL,
            youtube_id TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            tipo TEXT DEFAULT 'manual',
            data_criacao TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlist_itens (
            playlist_id INTEGER,
            musica_id INTEGER,
            PRIMARY KEY (playlist_id, musica_id),
            FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE,
            FOREIGN KEY (musica_id) REFERENCES musicas (id) ON DELETE CASCADE
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM musicas")
    if cursor.fetchone()[0] == 0:
        catalogo = [
            ("Happy", "Pharrell Williams", "Girl", "3:53", "Feliz", "Ensolarado", "ZbZSe6N_BXs"),
            ("Sunroof", "Nicky Youre", "Sunroof", "2:43", "Energético", "Ensolarado", "G5xS908lB28"),
            ("Sweater Weather", "The Neighbourhood", "I Love You.", "4:00", "Nostálgico", "Chuvoso", "GC862mACcwU"),
            ("Sad Songs", "Elton John", "Jump Up!", "4:10", "Triste", "Chuvoso", "m2S9B9tE9d4"),
            ("Weightless", "Marconi Union", "Weightless", "8:00", "Calmo", "Nublado", "UfcAVejslrU"),
            ("Perfect", "Ed Sheeran", "÷ (Divide)", "4:23", "Romântico", "Nublado", "2Vv-BfVoq4g"),
            ("Starboy", "The Weeknd", "Starboy", "3:50", "Energético", "Ensolarado", "34Na4j8AVgA"),
            ("Fix You", "Coldplay", "X&Y", "4:55", "Triste", "Chuvoso", "k4V3Mo61hJM"),
            ("Blinding Lights", "The Weeknd", "After Hours", "3:20", "Energético", "Ensolarado", "4NRXx6U8ABQ"),
            ("Flowers", "Miley Cyrus", "Endless Summer Vacation", "3:20", "Feliz", "Ensolarado", "G7KNmW9a75Y")
        ]
        cursor.executemany("""
            INSERT INTO musicas (titulo, artista, album, duracao, humor, clima, youtube_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, catalogo)
        conn.commit()

    conn.close()

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "f190d8a0735419d985475ff1c8262eb2").strip()

def obter_clima_detalhado(cidade="Sao Paulo"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={WEATHER_API_KEY}&units=metric&lang=pt_br"
    try:
        res = requests.get(url, timeout=5).json()
        if res.get("cod") == 200:
            temp = res["main"]["temp"]
            condicao_main = res["weather"][0]["main"]
            
            if condicao_main in ["Rain", "Drizzle", "Thunderstorm"]:
                clima_tag = "Chuvoso"
            elif condicao_main in ["Clouds"]:
                clima_tag = "Nublado"
            else:
                clima_tag = "Ensolarado"
                
            return {"temperatura": temp, "tag": clima_tag, "descricao": res["weather"][0]["description"]}
    except Exception:
        pass
    return {"temperatura": 22.0, "tag": "Ensolarado", "descricao": "Céu limpo"}


# API Endpoints
@app.route("/api/musicas", methods=["GET"])
def listar_musicas():
    conn = get_db_connection()
    musicas = conn.execute("SELECT * FROM musicas").fetchall()
    conn.close()
    return jsonify([dict(m) for m in musicas])


@app.route("/api/automacao/gerar", methods=["POST"])
def gerar_playlist_automatica():
    dados = request.get_json() or {}
    modo = dados.get("modo", "clima_humor")
    humor = dados.get("humor", "Feliz")
    cidade = dados.get("cidade", "Sao Paulo")

    info_clima = obter_clima_detalhado(cidade)
    clima_tag = info_clima["tag"]

    conn = get_db_connection()
    
    if modo == "clima_humor":
        query = "SELECT * FROM musicas WHERE humor = ? OR clima = ?"
        params = (humor, clima_tag)
        nome_playlist = f"Vibe: {humor} & Tempo {clima_tag}"
    elif modo == "apenas_humor":
        query = "SELECT * FROM musicas WHERE humor = ?"
        params = (humor,)
        nome_playlist = f"Sessão: {humor}"
    else:
        query = "SELECT * FROM musicas WHERE clima = ?"
        params = (clima_tag,)
        nome_playlist = f"Estilo {clima_tag} ({info_clima['temperatura']}°C)"

    musicas_filtradas = conn.execute(query, params).fetchall()
    
    if not musicas_filtradas:
        musicas_filtradas = conn.execute("SELECT * FROM musicas LIMIT 5").fetchall()

    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO playlists (nome, descricao, tipo, data_criacao)
        VALUES (?, ?, 'automatica', ?)
    """, (nome_playlist, f"Gerada via modo '{modo}' para {cidade}.", data_atual))
    playlist_id = cursor.lastrowid

    for m in musicas_filtradas:
        cursor.execute("INSERT INTO playlist_itens (playlist_id, musica_id) VALUES (?, ?)", (playlist_id, m["id"]))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "sucesso",
        "playlist_id": playlist_id,
        "nome": nome_playlist,
        "clima_info": info_clima,
        "total_faixas": len(musicas_filtradas),
        "musicas": [dict(m) for m in musicas_filtradas]
    })


if __name__ == "__main__":
    init_db()
    print("🚀 API Backend do Player rodando em http://127.0.0.1:5001")
    app.run(debug=True, port=5001)