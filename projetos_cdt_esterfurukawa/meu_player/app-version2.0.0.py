import os
import webbrowser
import requests
import unicodedata
from flask import Flask, redirect, request, render_template, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
# Chave secreta necessária para manter o login salvo na sessão
app.secret_key = "chave_secreta_super_segura_spotify_player"

# Credenciais do Spotify
SPOTIPY_CLIENT_ID = "2afb6b4ba69e4aeaa32b965e9c3e51cc"
SPOTIPY_CLIENT_SECRET = "f5a27ecd48e048e7969194bc35c8c8d5"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "playlist-modify-public playlist-modify-private user-read-private"

WEATHER_API_KEY = "f190d8a0735419d985475ff1c8262eb2"

def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def obter_clima(cidade="Sao Paulo"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={WEATHER_API_KEY}&units=metric&lang=pt_br"
    try:
        res = requests.get(url, timeout=5).json()
        if res.get("cod") == 200:
            cond = res["weather"][0]["main"]
            tag = "Chuvoso" if cond in ["Rain", "Drizzle", "Thunderstorm"] else "Nublado" if cond == "Clouds" else "Ensolarado"
            return {"temp": res["main"]["temp"], "tag": tag, "desc": res["weather"][0]["description"]}
    except Exception:
        pass
    return {"temp": 22.0, "tag": "Ensolarado", "desc": "céu limpo"}

def criar_autenticador_spotify():
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        show_dialog=True
    )

def obter_spotify_cliente():
    """Recupera o token da sessão ou atualiza se expirou."""
    token_info = session.get('token_info', None)
    if not token_info:
        return None
    
    sp_oauth = criar_autenticador_spotify()
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info

    return spotipy.Spotify(auth=token_info['access_token'])

# --- ROTAS DA APLICAÇÃO ---

@app.route("/")
def home():
    """Tela Inicial: Se já estiver logado vai para o App, senão mostra o Login."""
    sp = obter_spotify_cliente()
    if sp:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/login")
def login():
    """Inicia a autenticação com o Spotify."""
    sp_oauth = criar_autenticador_spotify()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    """Recebe a autorização do Spotify e salva a sessão."""
    sp_oauth = criar_autenticador_spotify()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    """O App principal onde seleciona Clima, Humor e Artista."""
    sp = obter_spotify_cliente()
    if not sp:
        return redirect(url_for("home"))
    
    try:
        user_info = sp.current_user()
        nome_usuario = user_info.get("display_name", "Usuário")
    except Exception:
        nome_usuario = "Usuário"

    return render_template("dashboard.html", nome_usuario=nome_usuario)

@app.route("/gerar", methods=["POST"])
def gerar():
    """Gera a playlist sem pedir login novamente."""
    sp = obter_spotify_cliente()
    if not sp:
        return redirect(url_for("home"))
    
    dados = request.form
    cidade = dados.get("cidade", "Sao Paulo").strip()
    artista = dados.get("artista", "").strip()
    humor = dados.get("humor", "Feliz")

    clima = obter_clima(cidade)
    humor_limpo = remover_acentos(humor)
    clima_limpo = remover_acentos(clima['tag'])

    if artista:
        termo_busca = f"{remover_acentos(artista)} {humor_limpo}"
    else:
        termo_busca = f"{humor_limpo} {clima_limpo}"

    try:
        resultados = sp.search(q=termo_busca, type='track', limit=15)
        tracks_uris = [item['uri'] for item in resultados['tracks']['items']]
    except Exception:
        tracks_uris = []

    if not tracks_uris:
        resultados = sp.search(q=humor_limpo, type='track', limit=15)
        tracks_uris = [item['uri'] for item in resultados['tracks']['items']]

    user_id = sp.current_user()['id']
    nome_playlist = f"Vibe {humor} | {clima['tag']}"
    if artista:
        nome_playlist += f" ({artista})"

    playlist = sp.user_playlist_create(
        user=user_id,
        name=nome_playlist,
        public=True,
        description=f"Playlist criada via Mood Player para {cidade} ({clima['desc']}, {clima['temp']}°C)."
    )

    if tracks_uris:
        sp.playlist_add_items(playlist_id=playlist['id'], items=tracks_uris)

    url_spotify = playlist['external_urls']['spotify']
    return redirect(url_spotify)

@app.route("/logout")
def logout():
    """Encerra a sessão."""
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    print("🚀 App rodando em http://127.0.0.1:8888")
    app.run(debug=True, port=8888)