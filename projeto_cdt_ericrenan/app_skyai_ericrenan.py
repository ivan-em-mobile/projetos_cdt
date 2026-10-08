"""
===============================================================================
IA "SKY" - Versão Automação Total (Controle Local + Navegação Web + Google Calendar)
Agora com DOIS MODOS: 💬 CHAT BOT  e  🤖 ASSISTENTE
===============================================================================
"""

import hashlib
import json
import os
import re
import sqlite3
import sys
import subprocess
import threading
import traceback
import urllib.parse
import webbrowser
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog

print("[INFO] Iniciando verificação de dependências...")

# 1. Verificação do Ollama
try:
    import ollama
except ImportError:
    print("[ERRO] Biblioteca 'ollama' não instalada. Execute: pip install ollama")
    sys.exit(1)

# 2. Verificação das bibliotecas do Google Calendar API
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("[ERRO] Dependências do Google ausentes. Execute: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    sys.exit(1)

# 3. Automação Visual (Opcional)
try:
    import pyautogui
    PYAUTOGUI_DISPONIVEL = True
except ImportError:
    PYAUTOGUI_DISPONIVEL = False


MODELO_AVANCADO_OLLAMA = "llama3.1:8b"
NOME_BANCO_DADOS = "historico_sky.db"
ARQUIVO_CONFIG_JSON = "config.json"
LIMITE_MENSAGENS_RECENTES = 4
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Perfil administrativo local: qualquer conta com este nome ganha acesso ao botão
# de exportação do banco de dados na interface. A senha em si (definida no login
# normal, como qualquer outra conta) deve ser 'Root'. Isso não é uma trava de
# segurança real - é só um atalho de conveniência para um app local de um usuário só.
NOME_USUARIO_ROOT = "Root Master"

# Limite de segurança do loop de ferramentas do modo Assistente
MAX_TOOL_ITERATIONS = 5

# Callback thread-safe de confirmação, definido pela GUI (AppSky) na inicialização.
# Assinatura esperada: (titulo: str, mensagem: str) -> bool
CONFIRMACAO_CALLBACK = None

# Padrões (case-insensitive) que identificam comandos de terminal potencialmente
# destrutivos e que, portanto, exigem confirmação explícita do usuário antes de rodar.
PADROES_COMANDO_DESTRUTIVO = [
    r"\bdel\b", r"\berase\b", r"\brd\b", r"\brmdir\b", r"\brm\s+-rf\b", r"\brm\s+-r\b",
    r"\bformat\b", r"\bdiskpart\b", r"\bshutdown\b", r"\breboot\b",
    r"\breg\s+delete\b", r"\bnet\s+user\b", r"\btaskkill\b", r"\bdrop\s+table\b",
    r"\bmkfs\b", r"\bchmod\s+-r\b", r"\bdd\s+if=", r"\buninstall\b", r"\bmsiexec\b.*\/x",
]


# =============================================================================
# MÓDULO DE AUTOMAÇÃO LOCAL E NAVEGAÇÃO WEB
# =============================================================================

# Catálogo configurável de aplicativos locais conhecidos (Windows).
CATALOGO_APLICATIVOS = {
    "bloco de notas": "notepad.exe",
    "notepad": "notepad.exe",
    "calculadora": "calc.exe",
    "edge": "msedge.exe",
    "cmd": "cmd.exe",
    "terminal": "wt.exe",
    "paint": "mspaint.exe",
    "vscode": "code",
    "vs code": "code",
    "code": "code",
    "spotify": "spotify.exe",
    "explorador": "explorer.exe",
    "explorer": "explorer.exe",
}

# Canais conhecidos do YouTube. NUNCA inventar URLs de canais que não estejam aqui:
# se o canal não estiver mapeado, cai para a busca normal do YouTube.
CANAIS_YOUTUBE_CONHECIDOS = {
    "edukof": "https://www.youtube.com/@edukof",
    "amenic": "https://www.youtube.com/@edukof",
}


def _texto_parece_url(texto: str) -> bool:
    """Heurística simples para saber se uma string já parece uma URL/domínio."""
    texto = texto.strip()
    if not texto:
        return False
    if texto.startswith("http://") or texto.startswith("https://"):
        return True
    # algo do tipo "exemplo.com" ou "exemplo.com/pagina"
    return bool(re.match(r"^[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+(/\S*)?$", texto))


def abrir_site(url: str) -> str:
    """Abre uma URL/site no navegador padrão, normalizando o esquema (https://) quando necessário.

    Args:
        url: endereço do site a abrir, com ou sem "https://".
    """
    if not url or not url.strip():
        return "Nenhuma URL foi fornecida."

    alvo = url.strip()
    if not alvo.startswith("http://") and not alvo.startswith("https://"):
        alvo = f"https://{alvo}"

    if not _texto_parece_url(url.strip()):
        return f"'{url}' não parece ser uma URL válida."

    try:
        webbrowser.open(alvo)
        return f"Site '{alvo}' aberto no navegador."
    except Exception as e:
        return f"Falha ao abrir o site '{url}': {str(e)}"


def pesquisar_google(termo: str) -> str:
    """Pesquisa um termo no Google, abrindo o resultado no navegador padrão.

    Args:
        termo: o que deve ser pesquisado no Google.
    """
    if not termo or not termo.strip():
        return "Nenhum termo de pesquisa foi fornecido."
    termo_encoded = urllib.parse.quote(termo.strip())
    try:
        webbrowser.open(f"https://www.google.com/search?q={termo_encoded}")
        return f"Pesquisando '{termo}' no Google!"
    except Exception as e:
        return f"Falha ao pesquisar '{termo}' no Google: {str(e)}"


def abrir_youtube(alvo: str = "") -> str:
    """Abre o YouTube: sem alvo abre a home, com um canal conhecido abre o canal,
    e com um termo de busca pesquisa vídeos.

    Args:
        alvo: pode ser vazio (abrir YouTube), o nome de um canal conhecido
              (ex: 'edukof') ou um termo de busca (ex: 'músicas de Hollow Knight').
    """
    alvo_limpo = (alvo or "").lower().strip()

    if not alvo_limpo:
        webbrowser.open("https://www.youtube.com")
        return "YouTube aberto com sucesso no navegador!"

    # 1. Canal conhecido (mapeamento explícito, nunca inventado)
    for chave, link in CANAIS_YOUTUBE_CONHECIDOS.items():
        if chave in alvo_limpo:
            webbrowser.open(link)
            return f"Canal '{chave}' aberto com sucesso no YouTube!"

    # 2. Pedido explícito de canal não mapeado -> cai para busca de canais
    termo_limpo = alvo_limpo
    for palavra in ["canal do", "canal de", "canal", "pesquise", "pesquisar", "procure", "procurar",
                     "abra", "abrir", "vídeos de", "videos de", "músicas de", "musicas de", "no youtube", "youtube"]:
        termo_limpo = termo_limpo.replace(palavra, "")
    termo_limpo = termo_limpo.strip(" :-")

    if not termo_limpo:
        webbrowser.open("https://www.youtube.com")
        return "YouTube aberto com sucesso no navegador!"

    termo_encoded = urllib.parse.quote(termo_limpo)
    webbrowser.open(f"https://www.youtube.com/results?search_query={termo_encoded}")
    return f"Pesquisando '{termo_limpo}' no YouTube!"


def abrir_aplicativo(nome_app: str) -> str:
    """Abre aplicativos locais conhecidos, ou cai para pesquisa no navegador se não reconhecer.

    Para sites, Google e YouTube, prefira as ferramentas abrir_site, pesquisar_google
    e abrir_youtube, que são mais específicas.

    Args:
        nome_app: nome do aplicativo a abrir (ex: 'bloco de notas', 'spotify', 'vscode').
    """
    nome_clean = nome_app.lower().strip()
    sistema = sys.platform

    # Redirecionamentos de conveniência para os casos mais comuns de web,
    # mantendo compatibilidade com quem ainda chamar esta função para isso.
    if "youtube" in nome_clean:
        return abrir_youtube(nome_clean.replace("youtube", "").replace("abrir", "").strip())

    if any(k in nome_clean for k in ["google", "chrome", "navegador", "internet"]):
        if any(k in nome_clean for k in ["calendario", "calendar", "agenda"]):
            webbrowser.open("https://calendar.google.com")
            return "Google Calendário aberto no seu navegador."
        termo_busca = nome_clean
        for palavra in ["google", "chrome", "abra", "abrir", "pesquisar", "pesquise", "para mim", "no navegador"]:
            termo_busca = termo_busca.replace(palavra, "")
        termo_busca = termo_busca.strip()
        if termo_busca:
            return pesquisar_google(termo_busca)
        webbrowser.open("https://www.google.com")
        return "Navegador Google Chrome aberto com sucesso."

    # Catálogo de aplicativos locais (correspondência exata ou por substring)
    alvo_app = None
    if nome_clean in CATALOGO_APLICATIVOS:
        alvo_app = CATALOGO_APLICATIVOS[nome_clean]
    else:
        for chave, executavel in CATALOGO_APLICATIVOS.items():
            if chave in nome_clean or nome_clean in chave:
                alvo_app = executavel
                break

    user_profile = os.environ.get("USERPROFILE", "")
    caminhos_chrome = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.join(user_profile, r"AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    chrome_encontrado = next((p for p in caminhos_chrome if os.path.exists(p)), None)

    try:
        if sistema.startswith("win"):
            if alvo_app:
                subprocess.Popen(alvo_app)
                return f"Aplicativo '{nome_app}' aberto com sucesso."
            elif chrome_encontrado and ("chrome" in nome_clean or "google" in nome_clean):
                subprocess.Popen(chrome_encontrado)
                return "Google Chrome aberto com sucesso."
            elif _texto_parece_url(nome_clean):
                return abrir_site(nome_clean)
            else:
                return pesquisar_google(nome_app)
        elif sistema == "darwin":  # macOS
            subprocess.Popen(["open", "-a", nome_app])
            return f"Aplicativo '{nome_app}' aberto no macOS."
        else:  # Linux
            subprocess.Popen([nome_clean])
            return f"Aplicativo '{nome_app}' iniciado no Linux."
    except FileNotFoundError:
        return f"Não encontrei o aplicativo '{nome_app}' instalado neste computador."
    except Exception as e:
        return f"Falha ao processar solicitação para '{nome_app}': {str(e)}"


def _comando_e_destrutivo(comando: str) -> bool:
    comando_lc = comando.lower()
    return any(re.search(padrao, comando_lc) for padrao in PADROES_COMANDO_DESTRUTIVO)


def executar_comando_terminal(comando: str) -> str:
    """Executa um comando de terminal (CMD/Bash) e retorna o resultado.

    Comandos potencialmente destrutivos (apagar arquivos, formatar, desligar o PC,
    etc.) exigem confirmação explícita do usuário antes de serem executados.

    Args:
        comando: o comando de terminal a executar.
    """
    if not comando or not comando.strip():
        return "Nenhum comando foi fornecido."

    if _comando_e_destrutivo(comando):
        if CONFIRMACAO_CALLBACK is None:
            return (f"Comando '{comando}' parece potencialmente destrutivo e não foi executado "
                     f"(nenhum canal de confirmação disponível).")
        confirmado = CONFIRMACAO_CALLBACK(
            "Confirmação necessária",
            f"A SKY quer executar o seguinte comando potencialmente destrutivo:\n\n{comando}\n\nDeseja autorizar?",
        )
        if not confirmado:
            return f"Comando '{comando}' cancelado: o usuário não autorizou a execução."

    try:
        resultado = subprocess.run(
            comando, shell=True, capture_output=True, text=True, timeout=15
        )
        saida = resultado.stdout.strip() or resultado.stderr.strip()
        return f"Resultado:\n{saida}" if saida else "Comando executado sem retorno textual."
    except subprocess.TimeoutExpired:
        return "O comando demorou demais e foi interrompido (timeout)."
    except Exception as e:
        return f"Erro ao executar comando: {str(e)}"


def digitar_texto_tela(texto: str) -> str:
    """Digita um texto simulando o teclado usando PyAutoGUI.

    Args:
        texto: o texto a ser digitado na posição atual do cursor.
    """
    if not PYAUTOGUI_DISPONIVEL:
        return "PyAutoGUI não está instalado no sistema."
    try:
        pyautogui.write(texto, interval=0.03)
        return f"Texto '{texto}' digitado na tela com sucesso."
    except Exception as e:
        return f"Erro ao digitar na tela: {str(e)}"


def pressionar_tecla(tecla: str) -> str:
    """Pressiona uma única tecla do teclado (ex: 'enter', 'esc', 'tab').

    Args:
        tecla: nome da tecla, no formato aceito pelo PyAutoGUI.
    """
    if not PYAUTOGUI_DISPONIVEL:
        return "PyAutoGUI não está instalado no sistema."
    try:
        pyautogui.press(tecla)
        return f"Tecla '{tecla}' pressionada com sucesso."
    except Exception as e:
        return f"Erro ao pressionar a tecla '{tecla}': {str(e)}"


def pressionar_teclas(combinacao: str) -> str:
    """Pressiona uma combinação de teclas, separadas por '+' (ex: 'ctrl+c', 'alt+tab').

    Args:
        combinacao: teclas separadas por '+'.
    """
    if not PYAUTOGUI_DISPONIVEL:
        return "PyAutoGUI não está instalado no sistema."
    try:
        teclas = [t.strip() for t in combinacao.split("+") if t.strip()]
        pyautogui.hotkey(*teclas)
        return f"Combinação '{combinacao}' executada com sucesso."
    except Exception as e:
        return f"Erro ao executar a combinação '{combinacao}': {str(e)}"


def mover_mouse(x: int, y: int) -> str:
    """Move o cursor do mouse para uma posição específica da tela.

    Args:
        x: posição horizontal em pixels.
        y: posição vertical em pixels.
    """
    if not PYAUTOGUI_DISPONIVEL:
        return "PyAutoGUI não está instalado no sistema."
    try:
        pyautogui.moveTo(int(x), int(y), duration=0.2)
        return f"Mouse movido para ({x}, {y})."
    except Exception as e:
        return f"Erro ao mover o mouse: {str(e)}"


def clicar_tela(x: int = None, y: int = None) -> str:
    """Clica na posição atual do mouse, ou em uma posição específica se informada.

    Args:
        x: posição horizontal em pixels (opcional).
        y: posição vertical em pixels (opcional).
    """
    if not PYAUTOGUI_DISPONIVEL:
        return "PyAutoGUI não está instalado no sistema."
    try:
        if x is not None and y is not None:
            pyautogui.click(int(x), int(y))
            return f"Clique realizado em ({x}, {y})."
        pyautogui.click()
        return "Clique realizado na posição atual do mouse."
    except Exception as e:
        return f"Erro ao clicar na tela: {str(e)}"


# =============================================================================
# MÓDULO GOOGLE CALENDAR (API)
# =============================================================================

def obter_servico_google_calendar():
    """Autentica o usuário via OAuth2 e retorna o serviço da API do Calendar."""
    creds = None
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except Exception as e:
            print(f"[AVISO] token.json inválido: {e}")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"[AVISO] Falha ao renovar token: {e}")
                creds = None

        if not creds:
            if not os.path.exists('credentials.json'):
                return None, "O arquivo 'credentials.json' não foi encontrado na pasta do script."

            try:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0, prompt='consent')
            except Exception as err_auth:
                return None, f"Falha na autenticação OAuth: {str(err_auth)}"

        try:
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        except Exception as err_token:
            print(f"[AVISO] Não foi possível salvar token.json: {err_token}")

    try:
        service = build('calendar', 'v3', credentials=creds)
        return service, "Sucesso"
    except Exception as err_service:
        return None, f"Erro ao conectar com serviço Google Calendar: {str(err_service)}"


def agendar_compromisso_google(titulo: str, data_inicio_iso: str, duracao_minutos: int = 60) -> str:
    """Cria um evento no Google Calendar via API.

    Args:
        titulo: título do evento.
        data_inicio_iso: data/hora de início no formato 'YYYY-MM-DDTHH:MM:SS'.
        duracao_minutos: duração do evento em minutos (padrão 60).
    """
    try:
        service, msg = obter_servico_google_calendar()
        if not service:
            return f"Erro de autenticação no Google Calendar: {msg}"

        from datetime import datetime, timedelta

        data_clean = data_inicio_iso.strip()
        if " " in data_clean and "T" not in data_clean:
            data_clean = data_clean.replace(" ", "T")
        if data_clean.endswith("Z"):
            data_clean = data_clean[:-1]
        if "+" in data_clean:
            data_clean = data_clean.split("+")[0]

        try:
            inicio_dt = datetime.fromisoformat(data_clean)
        except ValueError:
            inicio_dt = datetime.strptime(data_clean[:19], "%Y-%m-%dT%H:%M:%S")

        fim_dt = inicio_dt + timedelta(minutes=duracao_minutos)

        evento = {
            'summary': titulo,
            'start': {
                'dateTime': inicio_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': fim_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'America/Sao_Paulo',
            },
        }

        evento_criado = service.events().insert(calendarId='primary', body=evento).execute()
        link = evento_criado.get('htmlLink', '')
        return f"Evento '{titulo}' agendado para {inicio_dt.strftime('%d/%m/%Y às %H:%M')}! Link: {link}"

    except Exception as e:
        return f"Erro ao criar evento no Google Calendar: {str(e)}"


# =============================================================================
# DESPACHO DE FERRAMENTAS (usado pelo loop de agente do modo Assistente)
# =============================================================================

MAPA_FERRAMENTAS = {
    "abrir_aplicativo": abrir_aplicativo,
    "abrir_site": abrir_site,
    "pesquisar_google": pesquisar_google,
    "abrir_youtube": abrir_youtube,
    "executar_comando_terminal": executar_comando_terminal,
    "digitar_texto_tela": digitar_texto_tela,
    "pressionar_tecla": pressionar_tecla,
    "pressionar_teclas": pressionar_teclas,
    "mover_mouse": mover_mouse,
    "clicar_tela": clicar_tela,
    "agendar_compromisso_google": agendar_compromisso_google,
}

FERRAMENTAS_ASSISTENTE = [
    abrir_aplicativo,
    abrir_site,
    pesquisar_google,
    abrir_youtube,
    executar_comando_terminal,
    digitar_texto_tela,
    pressionar_tecla,
    mover_mouse,
    clicar_tela,
    agendar_compromisso_google,
]


def executar_ferramenta_por_nome(nome: str, argumentos: dict) -> str:
    """Executa, de forma segura, a ferramenta 'nome' com os argumentos fornecidos pelo modelo."""
    funcao = MAPA_FERRAMENTAS.get(nome)
    if not funcao:
        return f"Ferramenta '{nome}' desconhecida."
    try:
        argumentos = dict(argumentos or {})
        return funcao(**argumentos)
    except TypeError as e:
        return f"Argumentos inválidos para '{nome}': {str(e)}"
    except Exception as e:
        return f"Erro ao executar '{nome}': {str(e)}"


# =============================================================================
# BANCO DE DADOS & CONFIGURAÇÃO
# =============================================================================

def obter_conexao_db():
    return sqlite3.connect(NOME_BANCO_DADOS, timeout=20.0, check_same_thread=False)

CONFIG_PADRAO = {
    "tema": "escuro",
    "modelo": MODELO_AVANCADO_OLLAMA,
    "limite_historico": LIMITE_MENSAGENS_RECENTES,
}

def carregar_configuracao() -> dict:
    if not os.path.exists(ARQUIVO_CONFIG_JSON):
        salvar_configuracao(CONFIG_PADRAO)
        return CONFIG_PADRAO.copy()
    try:
        with open(ARQUIVO_CONFIG_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "modelo" not in data or not data["modelo"]:
                data["modelo"] = MODELO_AVANCADO_OLLAMA
            return data
    except Exception:
        return CONFIG_PADRAO.copy()

def salvar_configuracao(config: dict):
    try:
        with open(ARQUIVO_CONFIG_JSON, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[ERRO] Erro ao salvar JSON: {e}")

def encriptar_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()

def inicializar_banco_dados():
    """Cria as tabelas se não existirem e migra o schema de forma segura
    (nunca apaga dados existentes)."""
    print("[INFO] Verificando e inicializando banco de dados...")
    conexao = obter_conexao_db()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            sessao_id TEXT NOT NULL,
            data_hora TEXT NOT NULL,
            usuario_msg TEXT NOT NULL,
            resposta_sky TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memoria_resumida (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER UNIQUE NOT NULL,
            resumo TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        );
    """)

    # Migração segura: adiciona a coluna 'modo' em bancos já existentes,
    # sem apagar nenhum dado.
    cursor.execute("PRAGMA table_info(conversas);")
    colunas_existentes = [linha[1] for linha in cursor.fetchall()]
    if "modo" not in colunas_existentes:
        print("[INFO] Migrando banco de dados: adicionando coluna 'modo' em 'conversas'...")
        cursor.execute("ALTER TABLE conversas ADD COLUMN modo TEXT DEFAULT 'chat';")

    conexao.commit()
    conexao.close()

def autenticar_ou_cadastrar_usuario(nome_usuario: str, senha_digitada: str) -> tuple:
    nome_limpo = nome_usuario.strip().title()
    senha_hash = encriptar_senha(senha_digitada.strip())

    if not nome_limpo or not senha_digitada.strip():
        return False, None, "Preencha o nome de usuário e a senha."

    conexao = obter_conexao_db()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, senha_hash FROM usuarios WHERE nome = ?;", (nome_limpo,))
    usuario = cursor.fetchone()

    if usuario:
        usuario_id, hash_salvo = usuario
        if hash_salvo == senha_hash:
            conexao.close()
            return True, usuario_id, f"Bem-vindo(a) de volta, {nome_limpo}!"
        conexao.close()
        return False, None, "Senha incorreta! Acesso negado."

    cursor.execute("INSERT INTO usuarios (nome, senha_hash) VALUES (?, ?);", (nome_limpo, senha_hash))
    usuario_id = cursor.lastrowid
    cursor.execute("INSERT INTO memoria_resumida (usuario_id, resumo) VALUES (?, ?);", (usuario_id, "Nenhum fato registrado ainda."))
    conexao.commit()
    conexao.close()
    return True, usuario_id, f"Novo usuário '{nome_limpo}' cadastrado com sucesso!"

def salvar_conversa_sql(usuario_id: int, sessao_id: str, usuario_msg: str, resposta_sky: str, modo: str = "chat"):
    try:
        conexao = obter_conexao_db()
        cursor = conexao.cursor()
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO conversas (usuario_id, sessao_id, data_hora, usuario_msg, resposta_sky, modo)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (usuario_id, sessao_id, data_atual, usuario_msg, resposta_sky, modo))

        conexao.commit()
        conexao.close()
    except Exception as e:
        print(f"[ERRO] Erro ao salvar no banco: {e}")

def obter_resumo_memoria(usuario_id: int) -> str:
    conexao = obter_conexao_db()
    cursor = conexao.cursor()
    cursor.execute("SELECT resumo FROM memoria_resumida WHERE usuario_id = ?;", (usuario_id,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado[0] if resultado else "Nenhum fato registrado ainda."

def atualizar_resumo_memoria(usuario_id: int, novo_resumo: str):
    conexao = obter_conexao_db()
    cursor = conexao.cursor()
    cursor.execute("UPDATE memoria_resumida SET resumo = ? WHERE usuario_id = ?;", (novo_resumo, usuario_id))
    conexao.commit()
    conexao.close()

def obter_sessoes_usuario(usuario_id: int) -> list:
    conexao = obter_conexao_db()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT DISTINCT sessao_id FROM conversas 
        WHERE usuario_id = ? 
        ORDER BY id DESC;
    """, (usuario_id,))
    sessoes = [r[0] for r in cursor.fetchall()]
    conexao.close()
    return sessoes

def obter_conversas_da_sessao(usuario_id: int, sessao_id: str) -> list:
    """Retorna [(usuario_msg, resposta_sky, modo), ...] em ordem cronológica."""
    conexao = obter_conexao_db()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT usuario_msg, resposta_sky, COALESCE(modo, 'chat') FROM conversas 
        WHERE usuario_id = ? AND sessao_id = ?
        ORDER BY id ASC;
    """, (usuario_id, sessao_id))
    registros = cursor.fetchall()
    conexao.close()
    return registros


def exportar_banco_dados_json(caminho_arquivo: str = None) -> str:
    """Exporta todas as tabelas do banco de dados (usuarios, conversas e
    memoria_resumida) para um único arquivo JSON, para backup ou inspeção manual.

    Args:
        caminho_arquivo: caminho de destino do .json. Se não for informado, um
            nome com timestamp é gerado automaticamente na pasta atual do script.
    """
    if not caminho_arquivo or not caminho_arquivo.strip():
        caminho_arquivo = f"backup_sky_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    try:
        conexao = obter_conexao_db()
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()

        tabelas_exportadas = {}
        for nome_tabela in ["usuarios", "conversas", "memoria_resumida"]:
            cursor.execute(f"SELECT * FROM {nome_tabela};")
            tabelas_exportadas[nome_tabela] = [dict(linha) for linha in cursor.fetchall()]

        conexao.close()

        pacote_exportado = {
            "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "banco_origem": NOME_BANCO_DADOS,
            "tabelas": tabelas_exportadas,
        }

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(pacote_exportado, f, indent=4, ensure_ascii=False, default=str)

        return f"Banco de dados exportado com sucesso para '{os.path.abspath(caminho_arquivo)}'."
    except Exception as e:
        return f"Erro ao exportar banco de dados: {str(e)}"


# =============================================================================
# MÓDULO DA IA "SKY" COM FUNCTION CALLING (FERRAMENTAS) - DOIS MODOS
# =============================================================================

class AgenteSky:

    def __init__(self, modelo: str = MODELO_AVANCADO_OLLAMA):
        self.modelo = modelo

    def _obter_contexto_temporal(self) -> str:
        agora = datetime.now()
        dias_semana = {
            0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira",
            3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo"
        }
        return f"{dias_semana[agora.weekday()]}, {agora.strftime('%Y-%m-%d %H:%M:%S')}"

    def _extrair_e_guardar_fatos(self, usuario_id: int, mensagem_usuario: str):
        texto_lc = mensagem_usuario.lower()
        gatilhos = [
            "torço", "meu time", "clube", "santos", "flamengo", "palmeiras",
            "corinthians", "gosto de", "meu nome", "moro em", "tenho",
            "favorito", "prefiro", "sou de", "trabalho", "jogo", "filme"
        ]

        if any(g in texto_lc for g in gatilhos):
            resumo_atual = obter_resumo_memoria(usuario_id)
            novo_fato = f"- {mensagem_usuario.strip()}"

            if novo_fato not in resumo_atual:
                if resumo_atual == "Nenhum fato registrado ainda.":
                    atualizar_resumo_memoria(usuario_id, novo_fato)
                else:
                    atualizar_resumo_memoria(usuario_id, f"{resumo_atual}\n{novo_fato}")

    def _montar_cabecalho_sistema(self, nome_usuario: str) -> tuple:
        """Retorna (momento_atual, resumo_fatos) para reuso nos dois modos."""
        momento_atual = self._obter_contexto_temporal()
        return momento_atual

    # -------------------------------------------------------------------
    # PONTO DE ENTRADA ÚNICO - despacha para o modo correto
    # -------------------------------------------------------------------
    def responder(
        self,
        usuario_id: int,
        nome_usuario: str,
        mensagem_usuario: str,
        historico_sessao: list,
        modo: str = "chat",
    ) -> str:
        self._extrair_e_guardar_fatos(usuario_id, mensagem_usuario)

        if modo == "assistente":
            return self.responder_assistente(usuario_id, nome_usuario, mensagem_usuario, historico_sessao)
        return self.responder_chat(usuario_id, nome_usuario, mensagem_usuario, historico_sessao)

    # -------------------------------------------------------------------
    # 💬 MODO CHAT BOT - conversa normal, SEM ferramentas de automação
    # -------------------------------------------------------------------
    def responder_chat(self, usuario_id, nome_usuario, mensagem_usuario, historico_sessao) -> str:
        momento_atual = self._montar_cabecalho_sistema(nome_usuario)
        resumo_fatos = obter_resumo_memoria(usuario_id)

        instrucao_sistema = {
            "role": "system",
            "content": (
                f"Você é a SKY, um chatbot pessoal.\n"
                f"Usuário: {nome_usuario} | Data/Hora Atual: {momento_atual}\n\n"
                f"FATOS CONHECIDOS SOBRE O USUÁRIO:\n{resumo_fatos}\n\n"
                f"Sua função principal é conversar com o usuário e responder perguntas.\n\n"
                f"Você pode:\n"
                f"- responder dúvidas;\n- explicar assuntos;\n- informar a data atual;\n"
                f"- informar a hora atual;\n- fazer cálculos;\n- conversar normalmente;\n"
                f"- analisar textos;\n- ajudar nos estudos;\n- responder perguntas gerais;\n"
                f"- utilizar a memória disponível do usuário quando apropriado.\n\n"
                f"IMPORTANTE SOBRE OS FATOS CONHECIDOS ACIMA: use-os apenas quando forem "
                f"realmente relevantes para responder ao que o usuário perguntou. NÃO mencione "
                f"um fato espontaneamente só para mostrar que se lembra dele (ex: não comente "
                f"sobre o time de futebol do usuário numa saudação comum). Se a pergunta não tem "
                f"relação com um fato guardado, ignore-o e responda normalmente.\n\n"
                f"Neste modo você NÃO deve executar comandos no computador, não deve abrir "
                f"programas, não deve abrir sites, não deve executar terminal, não deve usar "
                f"PyAutoGUI e não deve criar eventos no Google Calendar.\n\n"
                f"Se o usuário pedir uma ação de automação enquanto estiver no Chat Bot, explique "
                f"de forma curta que essa função está disponível no modo Assistente e pergunte se "
                f"ele deseja trocar para esse modo.\n\n"
                f"Sempre utilize a Data/Hora Atual fornecida acima quando o usuário perguntar coisas "
                f"como 'que dia é hoje?', 'qual a data?', 'que horas são?', 'amanhã será que dia?' etc."
            ),
        }

        lista_mensagens = [instrucao_sistema]
        lista_mensagens.extend(historico_sessao[-LIMITE_MENSAGENS_RECENTES:])
        lista_mensagens.append({"role": "user", "content": mensagem_usuario})

        try:
            resposta = ollama.chat(
                model=self.modelo,
                messages=lista_mensagens,
                options={"temperature": 0.4},
            )
            return resposta["message"]["content"]
        except Exception as erro:
            return self._formatar_erro_ollama(erro)

    # -------------------------------------------------------------------
    # 🤖 MODO ASSISTENTE - agente de automação com ciclo real de ferramentas
    # -------------------------------------------------------------------
    def responder_assistente(self, usuario_id, nome_usuario, mensagem_usuario, historico_sessao) -> str:
        momento_atual = self._montar_cabecalho_sistema(nome_usuario)
        resumo_fatos = obter_resumo_memoria(usuario_id)

        instrucao_sistema = {
            "role": "system",
            "content": (
                f"Você é a SKY Assistente, um agente de automação local.\n"
                f"Usuário: {nome_usuario} | Data/Hora Atual: {momento_atual}\n\n"
                f"FATOS CONHECIDOS SOBRE O USUÁRIO:\n{resumo_fatos}\n\n"
                f"IMPORTANTE: use os fatos acima apenas quando forem realmente relevantes para "
                f"a solicitação atual. Não os mencione espontaneamente.\n\n"
                f"Sua função é ajudar o usuário a executar tarefas reais no computador. "
                f"Você possui acesso a ferramentas. Antes de responder, analise a intenção do "
                f"usuário e escolha a ferramenta adequada.\n\n"
                f"Você pode: abrir programas; abrir sites; pesquisar no Google; abrir páginas "
                f"específicas; abrir o YouTube; pesquisar vídeos no YouTube; abrir canais "
                f"específicos do YouTube; executar comandos de terminal quando necessário; "
                f"digitar texto pelo teclado; utilizar o Google Calendar; e realizar outras "
                f"automações disponíveis através das ferramentas.\n\n"
                f"Quando o usuário pedir uma ação concreta, tente executá-la através de uma "
                f"ferramenta em vez de apenas explicar como fazer. Depois de executar a ação, "
                f"informe de forma curta o que foi realizado. Nunca diga que uma ação foi "
                f"executada se a ferramenta realmente não tiver sido chamada ou tiver retornado "
                f"erro. Se uma ação falhar, informe o erro de maneira clara e tente uma "
                f"alternativa segura quando possível.\n\n"
                f"Converta datas relativas (ex: 'amanhã às 15h') em formato ISO "
                f"'YYYY-MM-DDTHH:MM:SS' usando a Data/Hora Atual acima como referência. Nunca "
                f"invente URLs de canais do YouTube que não sejam conhecidas."
            ),
        }

        mensagens = [instrucao_sistema]
        mensagens.extend(historico_sessao[-LIMITE_MENSAGENS_RECENTES:])
        mensagens.append({"role": "user", "content": mensagem_usuario})

        acoes_realizadas = []

        try:
            for _ in range(MAX_TOOL_ITERATIONS):
                resposta = ollama.chat(
                    model=self.modelo,
                    messages=mensagens,
                    tools=FERRAMENTAS_ASSISTENTE,
                    options={"temperature": 0.3},
                )
                mensagem_modelo = resposta.get("message", {})
                mensagens.append(mensagem_modelo)

                tool_calls = mensagem_modelo.get("tool_calls")
                if not tool_calls:
                    # O modelo terminou de raciocinar e respondeu normalmente.
                    conteudo_final = mensagem_modelo.get("content", "").strip()
                    if acoes_realizadas and not conteudo_final:
                        conteudo_final = "⚡ " + " | ".join(acoes_realizadas)
                    return conteudo_final or "Ação concluída."

                for chamada in tool_calls:
                    nome_funcao = chamada["function"]["name"]
                    argumentos = chamada["function"].get("arguments", {})
                    resultado_ferramenta = executar_ferramenta_por_nome(nome_funcao, argumentos)
                    acoes_realizadas.append(f"{nome_funcao}: {resultado_ferramenta}")

                    # Devolve o resultado da ferramenta ao Ollama para que ele continue
                    # raciocinando (ciclo real: usuário -> ollama -> tool -> ollama -> resposta).
                    mensagens.append({"role": "tool", "content": str(resultado_ferramenta)})

            # Limite de iterações atingido: devolve um resumo do que foi feito.
            resumo = "\n".join(f"- {a}" for a in acoes_realizadas) or "Nenhuma ação foi concluída."
            return f"⚡ Ações realizadas:\n{resumo}\n\n(Limite de {MAX_TOOL_ITERATIONS} iterações atingido.)"

        except Exception as erro:
            return self._formatar_erro_ollama(erro)

    def _formatar_erro_ollama(self, erro: Exception) -> str:
        err_str = str(erro)
        if "connection refused" in err_str.lower():
            return "❌ Erro: O serviço Ollama não está a rodar. Execute 'ollama serve' no terminal."
        elif "not found" in err_str.lower():
            return f"❌ Erro: O modelo '{self.modelo}' não foi baixado. Execute 'ollama run {self.modelo}' no terminal."
        return f"❌ Erro de execução: {err_str}"


# =============================================================================
# INTERFACE GRÁFICA TKINTER
# =============================================================================

PALETAS = {
    "escuro": {
        "COR_FUNDO_JANELA": "#1e1e2e", "COR_FUNDO_TOPO": "#181825",
        "COR_CAMPO_TEXTO": "#313244", "COR_TEXTO_PADRAO": "#cdd6f4",
        "COR_TEXTO_SUBTITULO": "#a6adc8", "COR_TITULO": "#ecb743",
        "COR_BOTAO_LOGIN": "#89b4fa", "COR_BOTAO_MEMORIA": "#fbff00",
        "COR_BOTAO_NOVO": "#a6e3a1", "COR_BOTAO_FECHAR": "#f38ba8",
        "COR_BOTAO_HIST": "#cba6f7", "COR_BOTAO_TEMA": "#89b4fa",
        "COR_BOTAO_ENVIAR": "#fff4f4", "COR_TEXTO_BOTAO": "#11111b",
        "COR_NOME_USUARIO": "#e2e2e2", "COR_NOME_SKY": "#00bcdd",
        "COR_MODO_ATIVO": "#f9e2af", "COR_MODO_INATIVO": "#313244",
        "COR_TEXTO_MODO_ATIVO": "#11111b", "COR_TEXTO_MODO_INATIVO": "#cdd6f4",
    },
    "claro": {
        "COR_FUNDO_JANELA": "#f4f4f9", "COR_FUNDO_TOPO": "#e2e2e9",
        "COR_CAMPO_TEXTO": "#ffffff", "COR_TEXTO_PADRAO": "#11111b",
        "COR_TEXTO_SUBTITULO": "#555566", "COR_TITULO": "#b57c00",
        "COR_BOTAO_LOGIN": "#2b6cb0", "COR_BOTAO_MEMORIA": "#d69e2e",
        "COR_BOTAO_NOVO": "#38a169", "COR_BOTAO_FECHAR": "#e53e3e",
        "COR_BOTAO_HIST": "#805ad5", "COR_BOTAO_TEMA": "#4a5568",
        "COR_BOTAO_ENVIAR": "#2b6cb0", "COR_TEXTO_BOTAO": "#ffffff",
        "COR_NOME_USUARIO": "#2d3748", "COR_NOME_SKY": "#00838f",
        "COR_MODO_ATIVO": "#d69e2e", "COR_MODO_INATIVO": "#e2e2e9",
        "COR_TEXTO_MODO_ATIVO": "#ffffff", "COR_TEXTO_MODO_INATIVO": "#2d3748",
    },
}

DESCRICOES_MODO = {
    "chat": "💬 CHAT BOT — Conversa e respostas gerais",
    "assistente": "🤖 ASSISTENTE — Automação e controle do computador",
}


def solicitar_confirmacao_gui(root: tk.Tk, titulo: str, mensagem: str) -> bool:
    """Pede confirmação (sim/não) ao usuário de forma thread-safe.

    Pode ser chamada a partir de qualquer thread (ex: de dentro de uma
    ferramenta executada pelo agente em background); a caixa de diálogo em si
    sempre roda na thread principal do Tkinter.
    """
    resultado = {"ok": False}
    evento = threading.Event()

    def perguntar():
        try:
            resultado["ok"] = messagebox.askyesno(titulo, mensagem)
        finally:
            evento.set()

    root.after(0, perguntar)
    evento.wait(timeout=60)
    return resultado["ok"]


class AppSky:

    def __init__(self, root):
        self.root = root
        self.root.title("IA SKY - Assistente Pessoal")
        self.root.geometry("700x780")

        self.config = carregar_configuracao()
        self.modo_tema = self.config.get("tema", "escuro")
        self.carregar_paleta()

        self.agente = AgenteSky(self.config.get("modelo", MODELO_AVANCADO_OLLAMA))
        self.usuario_id = None
        self.nome_usuario = ""
        self.abas_chat = {}

        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Registra o callback de confirmação thread-safe usado pelas ferramentas
        # (ex: executar_comando_terminal) para pedir autorização de ações destrutivas.
        global CONFIRMACAO_CALLBACK
        CONFIRMACAO_CALLBACK = lambda titulo, msg: solicitar_confirmacao_gui(self.root, titulo, msg)

        self.criar_tela_login()

    def carregar_paleta(self):
        p = PALETAS[self.modo_tema]
        self.COR_FUNDO_JANELA = p["COR_FUNDO_JANELA"]
        self.COR_FUNDO_TOPO = p["COR_FUNDO_TOPO"]
        self.COR_CAMPO_TEXTO = p["COR_CAMPO_TEXTO"]
        self.COR_TEXTO_PADRAO = p["COR_TEXTO_PADRAO"]
        self.COR_TEXTO_SUBTITULO = p["COR_TEXTO_SUBTITULO"]
        self.COR_TITULO = p["COR_TITULO"]
        self.COR_BOTAO_LOGIN = p["COR_BOTAO_LOGIN"]
        self.COR_BOTAO_MEMORIA = p["COR_BOTAO_MEMORIA"]
        self.COR_BOTAO_NOVO = p.get("COR_BOTAO_NOVO", "#a6e3a1")
        self.COR_BOTAO_FECHAR = p.get("COR_BOTAO_FECHAR", "#f38ba8")
        self.COR_BOTAO_HIST = p.get("COR_BOTAO_HIST", "#cba6f7")
        self.COR_BOTAO_TEMA = p["COR_BOTAO_TEMA"]
        self.COR_BOTAO_ENVIAR = p["COR_BOTAO_ENVIAR"]
        self.COR_TEXTO_BOTAO = p["COR_TEXTO_BOTAO"]
        self.COR_NOME_USUARIO = p["COR_NOME_USUARIO"]
        self.COR_NOME_SKY = p["COR_NOME_SKY"]
        self.COR_MODO_ATIVO = p["COR_MODO_ATIVO"]
        self.COR_MODO_INATIVO = p["COR_MODO_INATIVO"]
        self.COR_TEXTO_MODO_ATIVO = p["COR_TEXTO_MODO_ATIVO"]
        self.COR_TEXTO_MODO_INATIVO = p["COR_TEXTO_MODO_INATIVO"]

        self.root.configure(bg=self.COR_FUNDO_JANELA)

    def alternar_tema(self):
        self.modo_tema = "claro" if self.modo_tema == "escuro" else "escuro"
        self.config["tema"] = self.modo_tema
        salvar_configuracao(self.config)
        self.carregar_paleta()

        if hasattr(self, "frame_login") and self.frame_login.winfo_exists():
            self.frame_login.destroy()
            self.criar_tela_login()
        elif hasattr(self, "notebook"):
            # Antes de reconstruir a tela (necessário para repintar as cores),
            # guardamos quais abas estavam abertas para reabri-las depois.
            # Sem isso, a troca de tema descartava as conversas que estavam
            # abertas nas abas (elas continuavam salvas no banco, mas ninguém
            # as reabria automaticamente).
            sessoes_abertas = []
            indice_selecionado = 0

            if self.notebook.tabs():
                try:
                    indice_selecionado = self.notebook.index(self.notebook.select())
                except tk.TclError:
                    indice_selecionado = 0

                for aba_id in self.notebook.tabs():
                    frame_widget = self.notebook.nametowidget(aba_id)
                    titulo_texto = self.notebook.tab(aba_id, "text")
                    if titulo_texto.startswith("💬 "):
                        titulo_texto = titulo_texto[2:].strip()
                    for s_id, d_aba in self.abas_chat.items():
                        if d_aba["frame"] == frame_widget:
                            sessoes_abertas.append((s_id, titulo_texto, d_aba.get("modo", "chat")))
                            break

            for widget in self.root.winfo_children():
                widget.destroy()
            self.abas_chat = {}

            self.criar_tela_chat(sessoes_para_restaurar=sessoes_abertas, indice_selecionado=indice_selecionado)

    # -------------------------------------------------------------------
    # TELA DE LOGIN
    # -------------------------------------------------------------------
    def criar_tela_login(self):
        self.frame_login = tk.Frame(self.root, bg=self.COR_FUNDO_JANELA)
        self.frame_login.pack(expand=True)

        btn_tema = tk.Button(
            self.frame_login,
            text=f"Modo {'Claro' if self.modo_tema == 'escuro' else 'Escuro'}",
            font=("Helvetica", 9, "bold"),
            bg=self.COR_BOTAO_TEMA,
            fg=self.COR_TEXTO_BOTAO,
            relief="flat",
            command=self.alternar_tema,
            cursor="hand2",
        )
        btn_tema.pack(anchor="ne", pady=(0, 10))

        tk.Label(
            self.frame_login,
            text="✨ IA SKY",
            font=("Helvetica", 24, "bold"),
            fg=self.COR_TITULO,
            bg=self.COR_FUNDO_JANELA,
        ).pack(pady=20)

        tk.Label(
            self.frame_login,
            text="Autenticação do Utilizador",
            font=("Helvetica", 12),
            fg=self.COR_TEXTO_SUBTITULO,
            bg=self.COR_FUNDO_JANELA,
        ).pack(pady=5)

        tk.Label(
            self.frame_login, text="Utilizador:", fg=self.COR_TEXTO_PADRAO,
            bg=self.COR_FUNDO_JANELA, font=("Helvetica", 10, "bold")
        ).pack(anchor="w", pady=(10, 2))

        self.ent_usuario = tk.Entry(
            self.frame_login, font=("Helvetica", 12), width=30,
            bg=self.COR_CAMPO_TEXTO, fg=self.COR_TEXTO_PADRAO,
            insertbackground=self.COR_TEXTO_PADRAO, relief="flat"
        )
        self.ent_usuario.pack(pady=5, ipady=5)

        tk.Label(
            self.frame_login, text="Palavra-passe:", fg=self.COR_TEXTO_PADRAO,
            bg=self.COR_FUNDO_JANELA, font=("Helvetica", 10, "bold")
        ).pack(anchor="w", pady=(10, 2))

        self.ent_senha = tk.Entry(
            self.frame_login, show="*", font=("Helvetica", 12), width=30,
            bg=self.COR_CAMPO_TEXTO, fg=self.COR_TEXTO_PADRAO,
            insertbackground=self.COR_TEXTO_PADRAO, relief="flat"
        )
        self.ent_senha.pack(pady=5, ipady=5)

        btn_entrar = tk.Button(
            self.frame_login, text="Entrar / Registar",
            font=("Helvetica", 11, "bold"), bg=self.COR_BOTAO_LOGIN,
            fg=self.COR_TEXTO_BOTAO, relief="flat", command=self.acao_login,
            cursor="hand2"
        )
        btn_entrar.pack(pady=20, fill="x", ipady=5)

    def acao_login(self):
        nome = self.ent_usuario.get()
        senha = self.ent_senha.get()

        sucesso, user_id, msg = autenticar_ou_cadastrar_usuario(nome, senha)

        if sucesso:
            self.usuario_id = user_id
            self.nome_usuario = nome.strip().title()
            messagebox.showinfo("Sucesso", msg)
            self.frame_login.destroy()
            self.criar_tela_chat()
        else:
            messagebox.showerror("Acesso Negado", msg)

    def eh_usuario_root(self) -> bool:
        """True se o usuário logado for o perfil administrativo (Root Master)."""
        return self.nome_usuario.strip().lower() == NOME_USUARIO_ROOT.lower()

    def exportar_banco_dados_gui(self):
        """Pede um destino ao usuário e exporta o banco de dados inteiro em JSON."""
        caminho = filedialog.asksaveasfilename(
            title="Exportar banco de dados como JSON",
            defaultextension=".json",
            filetypes=[("Arquivo JSON", "*.json"), ("Todos os arquivos", "*.*")],
            initialfile=f"backup_sky_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        )
        if not caminho:
            return

        resultado = exportar_banco_dados_json(caminho)
        if resultado.startswith("Erro"):
            messagebox.showerror("Exportação falhou", resultado)
        else:
            messagebox.showinfo("Exportação concluída", resultado)

    # -------------------------------------------------------------------
    # TELA PRINCIPAL DE CHAT
    # -------------------------------------------------------------------
    def criar_tela_chat(self, sessoes_para_restaurar: list = None, indice_selecionado: int = 0):
        frame_topo = tk.Frame(self.root, bg=self.COR_FUNDO_TOPO)
        frame_topo.pack(fill="x")

        linha_superior = tk.Frame(frame_topo, bg=self.COR_FUNDO_TOPO)
        linha_superior.pack(fill="x")

        lbl_titulo = tk.Label(
            linha_superior, text=f"✨ SKY [{self.nome_usuario}]",
            font=("Helvetica", 11, "bold"), fg=self.COR_TITULO, bg=self.COR_FUNDO_TOPO
        )
        lbl_titulo.pack(side="left", padx=10, pady=10)

        btn_tema = tk.Button(
            linha_superior, text="🎨 Tema", bg=self.COR_BOTAO_TEMA,
            fg=self.COR_TEXTO_BOTAO, font=("Helvetica", 9, "bold"),
            relief="flat", command=self.alternar_tema, cursor="hand2"
        )
        btn_tema.pack(side="right", padx=(2, 10))

        btn_fechar_aba = tk.Button(
            linha_superior, text="❌ Fechar Aba", bg=self.COR_BOTAO_FECHAR,
            fg=self.COR_TEXTO_BOTAO, font=("Helvetica", 9, "bold"),
            relief="flat", command=self.fechar_aba_atual, cursor="hand2"
        )
        btn_fechar_aba.pack(side="right", padx=2)

        btn_hist = tk.Button(
            linha_superior, text="📜 Histórico", bg=self.COR_BOTAO_HIST,
            fg=self.COR_TEXTO_BOTAO, font=("Helvetica", 9, "bold"),
            relief="flat", command=self.abrir_menu_historico, cursor="hand2"
        )
        btn_hist.pack(side="right", padx=2)

        btn_memoria = tk.Button(
            linha_superior, text="🧠 Memória", bg=self.COR_BOTAO_MEMORIA,
            fg=self.COR_TEXTO_BOTAO, font=("Helvetica", 9, "bold"),
            relief="flat", command=self.exibir_memoria_box, cursor="hand2"
        )
        btn_memoria.pack(side="right", padx=2)

        btn_novo = tk.Button(
            linha_superior, text="➕ Nova", bg=self.COR_BOTAO_NOVO,
            fg=self.COR_TEXTO_BOTAO, font=("Helvetica", 9, "bold"),
            relief="flat", command=self.criar_nova_aba_chat, cursor="hand2"
        )
        btn_novo.pack(side="right", padx=2)

        if self.eh_usuario_root():
            btn_exportar = tk.Button(
                linha_superior, text="📦 Exportar JSON", bg=self.COR_BOTAO_HIST,
                fg=self.COR_TEXTO_BOTAO, font=("Helvetica", 9, "bold"),
                relief="flat", command=self.exportar_banco_dados_gui, cursor="hand2"
            )
            btn_exportar.pack(side="right", padx=2)

        # ------------------- Seletor de modo (💬 Chat Bot / 🤖 Assistente) -------------------
        linha_modo = tk.Frame(frame_topo, bg=self.COR_FUNDO_TOPO)
        linha_modo.pack(fill="x", padx=10, pady=(0, 8))

        self.btn_modo_chat = tk.Button(
            linha_modo, text="💬 CHAT BOT", font=("Helvetica", 10, "bold"),
            relief="flat", cursor="hand2", command=lambda: self.alternar_modo("chat")
        )
        self.btn_modo_chat.pack(side="left", ipadx=10, ipady=4, padx=(0, 4))

        self.btn_modo_assistente = tk.Button(
            linha_modo, text="🤖 ASSISTENTE", font=("Helvetica", 10, "bold"),
            relief="flat", cursor="hand2", command=lambda: self.alternar_modo("assistente")
        )
        self.btn_modo_assistente.pack(side="left", ipadx=10, ipady=4, padx=(0, 10))

        self.lbl_descricao_modo = tk.Label(
            linha_modo, text=DESCRICOES_MODO["chat"], font=("Helvetica", 9, "italic"),
            fg=self.COR_TEXTO_SUBTITULO, bg=self.COR_FUNDO_TOPO
        )
        self.lbl_descricao_modo.pack(side="left")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.atualizar_indicador_modo())

        if sessoes_para_restaurar:
            # Reabre exatamente as abas que estavam abertas antes (ex: antes de
            # trocar o tema), em vez de começar do zero com uma aba em branco.
            for sessao_id, titulo_aba, modo in sessoes_para_restaurar:
                self.criar_nova_aba_chat(sessao_id=sessao_id, titulo_aba=titulo_aba, modo_inicial=modo)
            try:
                self.notebook.select(indice_selecionado)
            except tk.TclError:
                pass
        else:
            self.criar_nova_aba_chat()

    def criar_nova_aba_chat(self, sessao_id: str = None, titulo_aba: str = None, modo_inicial: str = "chat"):
        if not sessao_id:
            sessao_id = f"Sessão {datetime.now().strftime('%H:%M:%S')}"

        if not titulo_aba:
            titulo_aba = sessao_id

        if sessao_id in self.abas_chat:
            self.notebook.select(self.abas_chat[sessao_id]["frame"])
            return

        frame_aba = tk.Frame(self.notebook, bg=self.COR_FUNDO_JANELA)

        area_chat = scrolledtext.ScrolledText(
            frame_aba, wrap=tk.WORD, font=("Helvetica", 11),
            bg=self.COR_FUNDO_JANELA, fg=self.COR_TEXTO_PADRAO, relief="flat"
        )
        area_chat.pack(padx=10, pady=10, fill="both", expand=True)
        area_chat.config(state="disabled")

        area_chat.tag_config("user", foreground=self.COR_NOME_USUARIO, font=("Helvetica", 11, "bold"))
        area_chat.tag_config("sky", foreground=self.COR_NOME_SKY, font=("Helvetica", 11))
        area_chat.tag_config("pensando", foreground=self.COR_NOME_SKY, font=("Helvetica", 11, "italic"))

        frame_input = tk.Frame(frame_aba, bg=self.COR_FUNDO_JANELA)
        frame_input.pack(fill="x", padx=10, pady=(0, 10))

        ent_msg = tk.Entry(
            frame_input, font=("Helvetica", 11), bg=self.COR_CAMPO_TEXTO,
            fg=self.COR_TEXTO_PADRAO, insertbackground=self.COR_TEXTO_PADRAO, relief="flat"
        )
        ent_msg.pack(side="left", fill="both", expand=True, ipady=8, padx=(0, 10))

        btn_enviar = tk.Button(
            frame_input, text="Enviar 🚀", font=("Helvetica", 10, "bold"),
            bg=self.COR_BOTAO_ENVIAR, fg=self.COR_TEXTO_BOTAO, relief="flat", cursor="hand2"
        )
        btn_enviar.pack(side="right", ipady=6, ipadx=10)

        dados_aba = {
            "frame": frame_aba, "area_chat": area_chat, "ent_msg": ent_msg,
            "btn_enviar": btn_enviar, "sessao_id": sessao_id, "historico": [],
            "modo": modo_inicial,
        }

        btn_enviar.config(command=lambda d=dados_aba: self.enviar_mensagem(d))
        ent_msg.bind("<Return>", lambda event, d=dados_aba: self.enviar_mensagem(d))

        self.abas_chat[sessao_id] = dados_aba
        self.notebook.add(frame_aba, text=f"💬 {titulo_aba}")
        self.notebook.select(frame_aba)

        conversas_salvas = obter_conversas_da_sessao(self.usuario_id, sessao_id)
        if conversas_salvas:
            ultimo_modo = "chat"
            for u_msg, s_msg, modo_msg in conversas_salvas:
                self.adicionar_texto_chat(area_chat, f"👤 {self.nome_usuario}: ", "user")
                self.adicionar_texto_chat(area_chat, f"{u_msg}\n\n", "normal")
                self.adicionar_texto_chat(area_chat, "✨ SKY: ", "sky")
                self.adicionar_texto_chat(area_chat, f"{s_msg}\n\n", "normal")
                dados_aba["historico"].append({"role": "user", "content": u_msg})
                dados_aba["historico"].append({"role": "assistant", "content": s_msg})
                ultimo_modo = modo_msg or "chat"
            dados_aba["modo"] = ultimo_modo
        else:
            self.adicionar_texto_chat(
                area_chat,
                f"✨ SKY: Olá, {self.nome_usuario}! Estou no modo 💬 Chat Bot. Troque para "
                f"🤖 Assistente quando precisar que eu execute ações no computador. Como posso ajudar?\n\n",
                "sky",
            )

        self.atualizar_indicador_modo()

    def fechar_aba_atual(self):
        if not self.notebook.tabs():
            return

        index_atual = self.notebook.index(self.notebook.select())
        frame_atual = self.notebook.nametowidget(self.notebook.tabs()[index_atual])

        sessao_para_remover = None
        for s_id, d_aba in self.abas_chat.items():
            if d_aba["frame"] == frame_atual:
                sessao_para_remover = s_id
                break

        if sessao_para_remover:
            del self.abas_chat[sessao_para_remover]

        self.notebook.forget(frame_atual)

        if not self.notebook.tabs():
            self.criar_nova_aba_chat()

    # -------------------------------------------------------------------
    # SELETOR DE MODO (Chat Bot / Assistente)
    # -------------------------------------------------------------------
    def _aba_atual(self):
        """Retorna o dicionário de dados da aba atualmente selecionada, ou None."""
        if not hasattr(self, "notebook") or not self.notebook.tabs():
            return None
        try:
            frame_atual = self.notebook.nametowidget(self.notebook.select())
        except tk.TclError:
            return None
        for dados_aba in self.abas_chat.values():
            if dados_aba["frame"] == frame_atual:
                return dados_aba
        return None

    def alternar_modo(self, novo_modo: str):
        dados_aba = self._aba_atual()
        if dados_aba is None:
            return
        dados_aba["modo"] = novo_modo
        self.atualizar_indicador_modo()

    def atualizar_indicador_modo(self):
        """Atualiza os botões de modo e a descrição para refletir a aba atual."""
        if not hasattr(self, "btn_modo_chat"):
            return

        dados_aba = self._aba_atual()
        modo_atual = dados_aba["modo"] if dados_aba else "chat"

        if modo_atual == "assistente":
            self.btn_modo_assistente.config(bg=self.COR_MODO_ATIVO, fg=self.COR_TEXTO_MODO_ATIVO)
            self.btn_modo_chat.config(bg=self.COR_MODO_INATIVO, fg=self.COR_TEXTO_MODO_INATIVO)
        else:
            self.btn_modo_chat.config(bg=self.COR_MODO_ATIVO, fg=self.COR_TEXTO_MODO_ATIVO)
            self.btn_modo_assistente.config(bg=self.COR_MODO_INATIVO, fg=self.COR_TEXTO_MODO_INATIVO)

        self.lbl_descricao_modo.config(text=DESCRICOES_MODO.get(modo_atual, ""))

    # -------------------------------------------------------------------
    # ENVIO DE MENSAGENS
    # -------------------------------------------------------------------
    def enviar_mensagem(self, dados_aba: dict):
        texto = dados_aba["ent_msg"].get().strip()
        if not texto:
            return

        dados_aba["ent_msg"].delete(0, tk.END)
        self.adicionar_texto_chat(dados_aba["area_chat"], f"👤 {self.nome_usuario}: ", "user")
        self.adicionar_texto_chat(dados_aba["area_chat"], f"{texto}\n\n", "normal")

        dados_aba["btn_enviar"].config(state="disabled")
        modo_atual = dados_aba.get("modo", "chat")
        texto_pensando = "✨ SKY: Processando solicitação..." if modo_atual == "chat" else "✨ SKY: Analisando e executando ação..."
        self.adicionar_texto_chat(dados_aba["area_chat"], f"{texto_pensando}\n", "pensando")

        threading.Thread(
            target=self._processar_resposta_thread,
            args=(texto, dados_aba),
            daemon=True,
        ).start()

    def _processar_resposta_thread(self, texto: str, dados_aba: dict):
        modo_atual = dados_aba.get("modo", "chat")
        try:
            resposta = self.agente.responder(
                self.usuario_id, self.nome_usuario, texto, dados_aba["historico"], modo=modo_atual
            )

            if not resposta.startswith("❌"):
                salvar_conversa_sql(self.usuario_id, dados_aba["sessao_id"], texto, resposta, modo=modo_atual)
                dados_aba["historico"].append({"role": "user", "content": texto})
                dados_aba["historico"].append({"role": "assistant", "content": resposta})

            self.root.after(0, self._atualizar_chat_pos_resposta, resposta, dados_aba)
        except Exception as e:
            err_msg = f"❌ Erro inesperado: {str(e)}"
            traceback.print_exc()
            self.root.after(0, self._atualizar_chat_pos_resposta, err_msg, dados_aba)

    def _atualizar_chat_pos_resposta(self, resposta: str, dados_aba: dict):
        area = dados_aba["area_chat"]
        area.config(state="normal")

        ranges = area.tag_ranges("pensando")
        if ranges:
            area.delete(ranges[0], ranges[1])

        area.config(state="disabled")

        self.adicionar_texto_chat(area, "✨ SKY: ", "sky")
        self.adicionar_texto_chat(area, f"{resposta}\n\n", "normal")
        dados_aba["btn_enviar"].config(state="normal")

    def adicionar_texto_chat(self, area_chat, texto: str, tag: str):
        area_chat.config(state="normal")
        area_chat.insert(tk.END, texto, tag)
        area_chat.config(state="disabled")
        area_chat.yview(tk.END)

    def abrir_menu_historico(self):
        sessoes = obter_sessoes_usuario(self.usuario_id)
        if not sessoes:
            messagebox.showinfo("Histórico", "Nenhuma conversa gravada no banco de dados.")
            return

        top = tk.Toplevel(self.root)
        top.title("Reabrir Conversa Antiga")
        top.geometry("350x300")
        top.configure(bg=self.COR_FUNDO_JANELA)

        tk.Label(
            top, text="Selecione uma sessão antiga:", fg=self.COR_TEXTO_PADRAO,
            bg=self.COR_FUNDO_JANELA, font=("Helvetica", 10, "bold")
        ).pack(pady=10)

        listbox = tk.Listbox(
            top, bg=self.COR_CAMPO_TEXTO, fg=self.COR_TEXTO_PADRAO,
            font=("Helvetica", 10), relief="flat"
        )
        listbox.pack(fill="both", expand=True, padx=15, pady=5)

        for s in sessoes:
            listbox.insert(tk.END, s)

        def carregar_sessao():
            selecionado = listbox.curselection()
            if selecionado:
                sessao_id = listbox.get(selecionado[0])
                self.criar_nova_aba_chat(sessao_id=sessao_id, titulo_aba=sessao_id)
                top.destroy()

        btn_abrir = tk.Button(
            top, text="Abrir Conversa", bg=self.COR_BOTAO_LOGIN,
            fg=self.COR_TEXTO_BOTAO, font=("Helvetica", 10, "bold"),
            relief="flat", command=carregar_sessao, cursor="hand2"
        )
        btn_abrir.pack(pady=10, ipady=5)

    def exibir_memoria_box(self):
        fatos = obter_resumo_memoria(self.usuario_id)
        messagebox.showinfo(f"Memória Viva de {self.nome_usuario}", fatos)


# =============================================================================
# INICIALIZAÇÃO SEGURA
# =============================================================================

if __name__ == "__main__":
    try:
        inicializar_banco_dados()
        print("[INFO] Iniciando Interface Gráfica...")
        root = tk.Tk()
        app = AppSky(root)
        root.mainloop()
    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha ao iniciar a aplicação: {e}")
        traceback.print_exc()