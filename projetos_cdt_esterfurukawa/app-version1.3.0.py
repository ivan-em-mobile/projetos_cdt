import os
import webbrowser
import requests
import unicodedata
from flask import Flask, redirect, request, render_template, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = "chave_secreta_sessao_spotify_player"

# Credenciais
SPOTIPY_CLIENT_ID = "2afb6b4ba69e4aeaa32b965e9c3e51cc"
SPOTIPY_CLIENT_SECRET = "f5a27ecd48e048e7969194bc35c8c8d5"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "playlist-modify-public playlist-modify-private"

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
        scope=SCOPE
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/gerar")
def gerar():
    session["humor"] = request.args.get("humor", "Feliz")
    session["cidade"] = request.args.get("cidade", "Sao Paulo")
    session["artista"] = request.args.get("artista", "").strip()

    sp_oauth = criar_autenticador_spotify()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    sp_oauth = criar_autenticador_spotify()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_id = sp.current_user()['id']
    
    humor = session.get("humor", "Feliz")
    cidade = session.get("cidade", "Sao Paulo")
    artista = session.get("artista", "")
    clima = obter_clima(cidade)
    
    humor_limpo = remover_acentos(humor)
    clima_limpo = remover_acentos(clima['tag'])
    
    # Formatação de busca ajustada sem prefixos para evitar erro 400
    if artista:
        termo_busca = f"{remover_acentos(artista)} {humor_limpo}"
    else:
        termo_busca = f"{humor_limpo} {clima_limpo}"
    
    try:
        resultados = sp.search(q=termo_busca, type='track', limit=15)
        tracks_uris = [item['uri'] for item in resultados['tracks']['items']]
    except Exception:
        tracks_uris = []

    # Fallback se a busca específica não retornar músicas
    if not tracks_uris:
        resultados = sp.search(q=humor_limpo, type='track', limit=15)
        tracks_uris = [item['uri'] for item in resultados['tracks']['items']]
    
    nome_playlist = f"Vibe {humor} | {clima['tag']}"
    if artista:
        nome_playlist += f" ({artista})"
    
    playlist = sp.user_playlist_create(
        user=user_id, 
        name=nome_playlist, 
        public=True,
        description=f"Gerada para {cidade} ({clima['desc']}, {clima['temp']}°C)."
    )
    
    if tracks_uris:
        sp.playlist_add_items(playlist_id=playlist['id'], items=tracks_uris)
    
    url_spotify = playlist['external_urls']['spotify']
    webbrowser.open(url_spotify)
    
    return f"""
    <div style="font-family: sans-serif; text-align: center; padding: 60px; background: #121212; color: #fff; height: 100vh;">
        <h1 style="color: #ff69b4;">🎉 Playlist criada com sucesso!</h1>
        <p style="font-size: 1.2rem; margin-top: 10px; color: #1db954;"><strong>Nome:</strong> {nome_playlist}</p>
        <p style="margin-top: 20px;">
            <a href="{url_spotify}" target="_blank" style="background: #1db954; color: #000; padding: 12px 24px; text-decoration: none; font-weight: bold; border-radius: 20px;">
                Abrir no Spotify
            </a>
        </p>
        <br><br>
        <a href="/" style="color: #ff69b4; text-decoration: none;">← Criar Outra Playlist</a>
    </div>
    """

if __name__ == "__main__":
    print("🚀 Server rodando em http://127.0.0.1:8888")
    app.run(debug=True, port=8888)