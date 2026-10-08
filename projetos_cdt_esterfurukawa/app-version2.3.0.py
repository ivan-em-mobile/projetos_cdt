import os
import unicodedata
import requests

from flask import Flask, redirect, request, render_template, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv


# ============================================================
# CARREGAR VARIÁVEIS DO .ENV
# ============================================================

load_dotenv()


# ============================================================
# CONFIGURAÇÃO
# ============================================================

app = Flask(__name__)

app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "chave-secreta-temporaria"
)


# ============================================================
# CREDENCIAIS DO SPOTIFY
# ============================================================

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

SCOPE = (
    "playlist-modify-public "
    "playlist-modify-private "
    "user-read-private"
)


# ============================================================
# OPENWEATHER
# ============================================================

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


# ============================================================
# FUNÇÃO PARA REMOVER ACENTOS
# ============================================================

def remover_acentos(texto):

    if not texto:
        return ""

    return "".join(
        c
        for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


# ============================================================
# OBTER CLIMA
# ============================================================

def obter_clima(cidade="Sao Paulo"):

    url = "https://api.openweathermap.org/data/2.5/weather"

    parametros = {
        "q": cidade,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }

    try:

        resposta = requests.get(
            url,
            params=parametros,
            timeout=5
        )

        resposta.raise_for_status()

        dados = resposta.json()

        if dados.get("cod") == 200:

            condicao = dados["weather"][0]["main"]

            if condicao in [
                "Rain",
                "Drizzle",
                "Thunderstorm"
            ]:
                tag = "Chuvoso"

            elif condicao == "Clouds":
                tag = "Nublado"

            else:
                tag = "Ensolarado"

            return {
                "temp": dados["main"]["temp"],
                "tag": tag,
                "desc": dados["weather"][0]["description"]
            }

    except Exception as erro:

        print("Erro ao obter clima:", erro)

    # Caso a API do clima falhe
    return {
        "temp": 22.0,
        "tag": "Ensolarado",
        "desc": "céu limpo"
    }


# ============================================================
# AUTENTICAÇÃO DO SPOTIFY
# ============================================================

def criar_autenticador_spotify():

    return SpotifyOAuth(

        client_id=SPOTIPY_CLIENT_ID,

        client_secret=SPOTIPY_CLIENT_SECRET,

        redirect_uri=SPOTIPY_REDIRECT_URI,

        scope=SCOPE,

        show_dialog=True
    )


# ============================================================
# OBTER CLIENTE DO SPOTIFY
# ============================================================

def obter_spotify_cliente():

    token_info = session.get("token_info")

    if not token_info:
        return None

    sp_oauth = criar_autenticador_spotify()

    try:

        if sp_oauth.is_token_expired(token_info):

            refresh_token = token_info.get(
                "refresh_token"
            )

            if not refresh_token:

                session.clear()

                return None

            token_info = sp_oauth.refresh_access_token(
                refresh_token
            )

            session["token_info"] = token_info

        return spotipy.Spotify(
            auth=token_info["access_token"]
        )

    except Exception as erro:

        print(
            "Erro ao obter cliente Spotify:",
            erro
        )

        session.clear()

        return None


# ============================================================
# PÁGINA INICIAL
# ============================================================

@app.route("/")
def home():

    sp = obter_spotify_cliente()

    if sp:

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "login.html"
    )


# ============================================================
# LOGIN DO SPOTIFY
# ============================================================

@app.route("/login")
def login():

    sp_oauth = criar_autenticador_spotify()

    auth_url = sp_oauth.get_authorize_url()

    return redirect(auth_url)


# ============================================================
# CALLBACK DO SPOTIFY
# ============================================================

@app.route("/callback")
def callback():

    sp_oauth = criar_autenticador_spotify()

    # Verifica se o Spotify retornou algum erro
    if request.args.get("error"):

        erro = request.args.get("error")

        return (
            f"<h2>Erro na autenticação</h2>"
            f"<p>{erro}</p>"
        )

    # Obtém o código de autorização
    code = request.args.get("code")

    if not code:

        return (
            "<h2>Erro</h2>"
            "<p>Código de autorização não recebido.</p>"
        )

    try:

        token_info = sp_oauth.get_access_token(
            code
        )

        session["token_info"] = token_info

        return redirect(
            url_for("dashboard")
        )

    except Exception as erro:

        print(
            "Erro ao obter token:",
            erro
        )

        return (
            "<h2>Erro ao conectar ao Spotify</h2>"
            f"<p>{erro}</p>"
        )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    sp = obter_spotify_cliente()

    if not sp:

        return redirect(
            url_for("home")
        )

    try:

        usuario = sp.current_user()

        nome_usuario = usuario.get(
            "display_name",
            "Usuário"
        )

    except Exception as erro:

        print(
            "Erro ao obter usuário:",
            erro
        )

        nome_usuario = "Usuário"

    return render_template(

        "dashboard.html",

        nome_usuario=nome_usuario
    )


# ============================================================
# GERAR PLAYLIST
# ============================================================

@app.route("/gerar", methods=["POST"])
def gerar():

    sp = obter_spotify_cliente()

    if not sp:

        return redirect(
            url_for("home")
        )

    # --------------------------------------------------------
    # DADOS DO FORMULÁRIO
    # --------------------------------------------------------

    cidade = request.form.get(
        "cidade",
        "Sao Paulo"
    ).strip()

    artista = request.form.get(
        "artista",
        ""
    ).strip()

    humor = request.form.get(
        "humor",
        "Feliz"
    )

    # --------------------------------------------------------
    # CLIMA
    # --------------------------------------------------------

    clima = obter_clima(cidade)

    humor_limpo = remover_acentos(
        humor
    )

    clima_limpo = remover_acentos(
        clima["tag"]
    )

    # --------------------------------------------------------
    # TERMO DE BUSCA
    # --------------------------------------------------------

    if artista:

        termo_busca = (
            f"{remover_acentos(artista)} "
            f"{humor_limpo}"
        )

    else:

        termo_busca = (
            f"{humor_limpo} "
            f"{clima_limpo}"
        )

    print()
    print("===================================")
    print("BUSCA DE MÚSICAS")
    print("===================================")
    print("Cidade:", cidade)
    print("Humor:", humor)
    print("Clima:", clima["tag"])
    print("Artista:", artista)
    print("Termo pesquisado:", termo_busca)
    print("===================================")

    tracks_uris = []

    # --------------------------------------------------------
    # PRIMEIRA BUSCA
    # --------------------------------------------------------

    try:

        resultados = sp.search(

            q=termo_busca,

            type="track",

            limit=10
        )

        tracks_uris = [

            item["uri"]

            for item
            in resultados["tracks"]["items"]

        ]

        print(
            "Músicas encontradas:",
            len(tracks_uris)
        )

    except Exception as erro:

        print(
            "Erro ao buscar músicas:",
            erro
        )

    # --------------------------------------------------------
    # SEGUNDA BUSCA
    # --------------------------------------------------------

    if not tracks_uris:

        try:

            resultados = sp.search(

                q=humor_limpo,

                type="track",

                limit=10
            )

            tracks_uris = [

                item["uri"]

                for item
                in resultados["tracks"]["items"]

            ]

            print(
                "Músicas encontradas na segunda busca:",
                len(tracks_uris)
            )

        except Exception as erro:

            print(
                "Erro na segunda busca:",
                erro
            )

    # --------------------------------------------------------
    # NOME DA PLAYLIST
    # --------------------------------------------------------

    nome_playlist = (
        f"Sintonia | {humor} | {clima['tag']}"
    )

    if artista:

        nome_playlist += (
            f" | {artista}"
        )

    # --------------------------------------------------------
    # CRIAR PLAYLIST
    # --------------------------------------------------------

    try:

        playlist = sp.current_user_playlist_create(

            name=nome_playlist,

            public=True,

            description=(
                f"Playlist criada pelo Sintonia "
                f"para {cidade}. "
                f"Clima: {clima['desc']}, "
                f"{clima['temp']:.1f}°C."
            )
        )

        print(
            "Playlist criada com sucesso."
        )

    except Exception as erro:

        print(
            "ERRO AO CRIAR PLAYLIST:",
            erro
        )

        return (
            "<h2>Não foi possível criar a playlist.</h2>"
            f"<p>{erro}</p>"
        )

    # --------------------------------------------------------
    # ADICIONAR MÚSICAS
    # --------------------------------------------------------

    if tracks_uris:

        try:

            sp.playlist_add_items(

                playlist_id=playlist["id"],

                items=tracks_uris
            )

            print(
                "Músicas adicionadas:",
                len(tracks_uris)
            )

        except Exception as erro:

            print(
                "Erro ao adicionar músicas:",
                erro
            )

    else:

        print(
            "Nenhuma música foi encontrada."
        )

    # --------------------------------------------------------
    # ABRIR PLAYLIST
    # --------------------------------------------------------

    url_spotify = (
        playlist["external_urls"]["spotify"]
    )

    return redirect(
        url_spotify
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# ============================================================
# EXECUTAR A APLICAÇÃO
# ============================================================

if __name__ == "__main__":

    print()
    print("===================================")
    print("SINTONIA")
    print("===================================")
    print("Aplicação rodando em:")
    print("http://127.0.0.1:8888/callback")
    print("===================================")
    print()

    app.run(
        debug=True,
        port=8888
    )