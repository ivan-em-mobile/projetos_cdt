import unicodedata
import requests

from flask import Flask, redirect, request, render_template, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# ============================================================
# CONFIGURAÇÃO
# ============================================================

app = Flask(__name__)

# Use uma chave nova aqui
app.secret_key = "SUA_CHAVE_SECRETA_DO_FLASK"

# Spotify
SPOTIPY_CLIENT_ID = "2afb6b4ba69e4aeaa32b965e9c3e51cc"
SPOTIPY_CLIENT_SECRET = "f5a27ecd48e048e7969194bc35c8c8d5"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

SCOPE = (
    "playlist-modify-public "
    "playlist-modify-private "
    "user-read-private"
)

# OpenWeather
WEATHER_API_KEY = "f190d8a0735419d985475ff1c8262eb2"


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def remover_acentos(texto):
    """
    Remove acentos de um texto.
    Exemplo:
    'São Paulo' -> 'Sao Paulo'
    """
    if not texto:
        return ""

    return "".join(
        c
        for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def obter_clima(cidade="Sao Paulo"):
    """
    Consulta o clima atual da cidade usando OpenWeather.
    """

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={cidade}"
        f"&appid={WEATHER_API_KEY}"
        "&units=metric"
        "&lang=pt_br"
    )

    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()

        res = resposta.json()

        if res.get("cod") == 200:

            condicao = res["weather"][0]["main"]

            if condicao in ["Rain", "Drizzle", "Thunderstorm"]:
                tag = "Chuvoso"

            elif condicao == "Clouds":
                tag = "Nublado"

            else:
                tag = "Ensolarado"

            return {
                "temp": res["main"]["temp"],
                "tag": tag,
                "desc": res["weather"][0]["description"]
            }

    except Exception as e:
        print("Erro ao obter clima:", e)

    # Caso a API falhe
    return {
        "temp": 22.0,
        "tag": "Ensolarado",
        "desc": "céu limpo"
    }


# ============================================================
# SPOTIFY
# ============================================================

def criar_autenticador_spotify():
    """
    Cria o objeto responsável pela autenticação do Spotify.
    """

    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        show_dialog=True
    )


def obter_spotify_cliente():
    """
    Recupera o token salvo na sessão e cria o cliente Spotify.
    """

    token_info = session.get("token_info")

    if not token_info:
        return None

    sp_oauth = criar_autenticador_spotify()

    try:

        # Verifica se o token expirou
        if sp_oauth.is_token_expired(token_info):

            refresh_token = token_info.get("refresh_token")

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

    except Exception as e:

        print("Erro ao obter cliente Spotify:", e)

        session.clear()

        return None


# ============================================================
# ROTAS
# ============================================================

@app.route("/")
def home():

    sp = obter_spotify_cliente()

    if sp:
        return redirect(url_for("dashboard"))

    return render_template("login.html")


# ------------------------------------------------------------
# LOGIN
# ------------------------------------------------------------

@app.route("/login")
def login():

    sp_oauth = criar_autenticador_spotify()

    auth_url = sp_oauth.get_authorize_url()

    return redirect(auth_url)


# ------------------------------------------------------------
# CALLBACK DO SPOTIFY
# ------------------------------------------------------------

@app.route("/callback")
def callback():

    sp_oauth = criar_autenticador_spotify()

    # Spotify informou algum erro
    if request.args.get("error"):

        erro = request.args.get("error")

        return f"Erro na autenticação do Spotify: {erro}"

    # Código de autorização
    code = request.args.get("code")

    if not code:

        return "Código de autorização não recebido."

    try:

        token_info = sp_oauth.get_access_token(code)

        session["token_info"] = token_info

        return redirect(url_for("dashboard"))

    except Exception as e:

        print("Erro ao obter token:", e)

        return f"Erro ao autenticar com o Spotify: {e}"


# ------------------------------------------------------------
# DASHBOARD
# ------------------------------------------------------------

@app.route("/dashboard")
def dashboard():

    sp = obter_spotify_cliente()

    if not sp:
        return redirect(url_for("home"))

    try:

        user_info = sp.current_user()

        nome_usuario = user_info.get(
            "display_name",
            "Usuário"
        )

    except Exception as e:

        print("Erro ao obter usuário:", e)

        nome_usuario = "Usuário"

    return render_template(
        "dashboard.html",
        nome_usuario=nome_usuario
    )


# ------------------------------------------------------------
# GERAR PLAYLIST
# ------------------------------------------------------------

@app.route("/gerar", methods=["POST"])
def gerar():

    sp = obter_spotify_cliente()

    if not sp:
        return redirect(url_for("home"))

    # Dados enviados pelo formulário
    dados = request.form

    cidade = dados.get(
        "cidade",
        "Sao Paulo"
    ).strip()

    artista = dados.get(
        "artista",
        ""
    ).strip()

    humor = dados.get(
        "humor",
        "Feliz"
    )

    # ========================================================
    # CLIMA
    # ========================================================

    clima = obter_clima(cidade)

    humor_limpo = remover_acentos(humor)

    clima_limpo = remover_acentos(
        clima["tag"]
    )

    # ========================================================
    # BUSCA DAS MÚSICAS
    # ========================================================

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

    print("===================================")
    print("Termo pesquisado:", termo_busca)
    print("===================================")

    tracks_uris = []

    # Primeira tentativa
    try:

        resultados = sp.search(
            q=termo_busca,
            type="track",
            limit=10
        )

        tracks_uris = [
            item["uri"]
            for item in resultados["tracks"]["items"]
        ]

        print(
            "Músicas encontradas:",
            len(tracks_uris)
        )

    except Exception as e:

        print(
            "Erro ao buscar músicas:",
            e
        )

    # Segunda tentativa caso a primeira não encontre nada
    if not tracks_uris:

        try:

            resultados = sp.search(
                q=humor_limpo,
                type="track",
                limit=10
            )

            tracks_uris = [
                item["uri"]
                for item in resultados["tracks"]["items"]
            ]

            print(
                "Músicas encontradas na segunda busca:",
                len(tracks_uris)
            )

        except Exception as e:

            print(
                "Erro na segunda busca:",
                e
            )

    # ========================================================
    # NOME DA PLAYLIST
    # ========================================================

    nome_playlist = (
        f"Vibe {humor} | {clima['tag']}"
    )

    if artista:

        nome_playlist += f" ({artista})"

    print(
        "Criando playlist:",
        nome_playlist
    )

    # ========================================================
    # CRIAR PLAYLIST
    # ========================================================

    try:

        playlist = sp.current_user_playlist_create(
            name=nome_playlist,
            public=True,
            description=(
                f"Playlist criada via Mood Player "
                f"para {cidade} "
                f"({clima['desc']}, "
                f"{clima['temp']}°C)."
            )
        )

    except Exception as e:

        print(
            "ERRO AO CRIAR PLAYLIST:",
            e
        )

        return (
            "Erro ao criar a playlist no Spotify: "
            f"{e}"
        )

    # ========================================================
    # ADICIONAR MÚSICAS
    # ========================================================

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

        except Exception as e:

            print(
                "Erro ao adicionar músicas:",
                e
            )

    else:

        print(
            "Nenhuma música foi encontrada."
        )

    # ========================================================
    # ABRIR PLAYLIST NO SPOTIFY
    # ========================================================

    url_spotify = (
        playlist["external_urls"]["spotify"]
    )

    return redirect(url_spotify)


# ------------------------------------------------------------
# LOGOUT
# ------------------------------------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    print(
        "🚀 App rodando em "
        "http://127.0.0.1:8888"
    )

    app.run(
        debug=True,
        port=8888
    )