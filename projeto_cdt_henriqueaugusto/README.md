# -🌎☁projetos_cdt
🚀 IA SKY: Assistente Pessoal, Automação Local e Google Calendar
Bem-vindo ao repositório da IA SKY! Este projeto é uma assistente virtual unificada desenvolvida em Python que une o processamento de linguagem natural local (Ollama / Llama 3.1) com automação do sistema operacional, pesquisas na web e gestão da agenda do Google.
O sistema possui interface gráfica (Tkinter) com suporte a abas de conversa, múltiplos usuários com autenticação criptografada, memória de longo prazo e Function Calling nativo.

📅 Estrutura e Módulos do Sistema
O projeto é dividido em blocos bem definidos de funcionalidade e integração:

⚙️ Bloco 1: Automação e Ferramentas Locais
A assistente consegue interagir diretamente com o sistema operacional para executar tarefas e buscar informações externas:
- Abertura de Aplicativos: Suporte a Windows, macOS e Linux para abrir softwares nativos ou instalados.
- Comandos de Terminal: Execução remota via cmd/shell com timeout de segurança de 15 segundos.
- Pesquisa Web: Módulo de busca dinâmica utilizando a biblioteca googlesearch-python.

## 📦 Dependências do Projeto

| Biblioteca | Finalidade |
| :--- | :--- |
| `ollama` | Interface com modelos locais de LLM (ex: Llama 3.1) |
| `google-api-python-client` | Integração com as APIs do Google |
| `google-auth-httplib2` | Autenticação HTTP para serviços do Google |
| `google-auth-oauthlib` | Fluxo de autenticação OAuth 2.0 do Google |
| `googlesearch-python` | Realização de pesquisas na web via Python *(Opcional)* |
| `tkinter` | Interface gráfica nativa e gerenciamento da GUI |
| `sqlite3` | Banco de dados relacional embutido para histórico e dados |

---

## ⚡ Guia de Instalação e Execução

1. **Instale as dependências:**
```bash
pip install ollama google-api-python-client google-auth-httplib2 google-auth-oauthlib googlesearch-python
```

* Garanta que o Ollama esteja rodando com o modelo configurado:
```bash
ollama run llama3.1:8b
```

* Execute o aplicativo:
```bash
python main.py
```

⚙️ Módulos e Funcionalidades Principais
1. Persistência de Dados & Banco SQLite

```python
# Inicialização e criação das tabelas do banco de dados relacional
def inicializar_banco_dados():
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

    conexao.commit()
    conexao.close()
```

2. Automações Locais e Execução de Ferramentas
Abertura de aplicativos do sistema operacional

def abrir_aplicativo(nome_app: str) -> str:
    nome_clean = nome_app.lower().strip()
    sistema = sys.platform

    apps_comuns_win = {
        "bloco de notas": "notepad.exe",
        "calculadora": "calc.exe",
        "chrome": "chrome.exe",
        "cmd": "cmd.exe",
        "vscode": "code",
    }

    try:
        if sistema.startswith("win"):
            if nome_clean in apps_comuns_win:
                subprocess.Popen(apps_comuns_win[nome_clean])
                return f"Aplicativo '{nome_app}' aberto com sucesso."
            else:
                subprocess.Popen(f"start {nome_app}", shell=True)
                return f"Tentando abrir o programa/comando '{nome_app}'."
        elif sistema == "darwin":
            subprocess.Popen(["open", "-a", nome_app])
            return f"Aplicativo '{nome_app}' aberto no macOS."
        else:
            subprocess.Popen([nome_clean])
            return f"Aplicativo '{nome_app}' iniciado no Linux."
    except Exception as e:
        return f"Falha ao abrir o aplicativo '{nome_app}': {str(e)}"

3. Integração com Google Calendar API
# Agendamento automático de compromissos no Google Agenda
def agendar_compromisso_google(titulo: str, data_inicio_iso: str, duracao_minutos: int = 60) -> str:
    try:
        service, msg = obter_servico_google_calendar()
        if not service:
            return f"Erro de autenticação no Google Calendar: {msg}"

        data_inicio_iso = data_inicio_iso.split('+')[0].replace('Z', '')
        inicio_dt = datetime.fromisoformat(data_inicio_iso)
        fim_dt = inicio_dt + timedelta(minutes=duracao_minutos)

        evento = {
            'summary': titulo,
            'start': {'dateTime': inicio_dt.isoformat(), 'timeZone': 'America/Sao_Paulo'},
            'end': {'dateTime': fim_dt.isoformat(), 'timeZone': 'America/Sao_Paulo'},
        }

        evento_criado = service.events().insert(calendarId='primary', body=evento).execute()
        return f"Evento '{titulo}' agendado com sucesso! Link: {evento_criado.get('htmlLink')}"
    except Exception as e:
        return f"Erro ao criar evento no Google Calendar: {str(e)}"

4. Agente IA com Chamada de Funções (Function Calling)
# Processamento de mensagens do usuário e invocação de ferramentas via Ollama
class AgenteSky:
    def __init__(self, modelo: str = MODELO_AVANCADO_OLLAMA):
        self.modelo = modelo

    def responder(self, usuario_id: int, nome_usuario: str, mensagem_usuario: str, historico_sessao: list) -> str:
        self._extrair_e_guardar_fatos(usuario_id, mensagem_usuario)
        momento_atual = self._obter_contexto_temporal()
        resumo_fatos = obter_resumo_memoria(usuario_id)

        instrucao_sistema = {
            "role": "system",
            "content": f"Você é a SKY... Usuário: {nome_usuario} | Data/Hora Atual: {momento_atual}\nFATOS: {resumo_fatos}"
        }

        lista_mensagens = [instrucao_sistema] + historico_sessao[-LIMITE_MENSAGENS_RECENTES:] + [{"role": "user", "content": mensagem_usuario}]
        ferramentas = [abrir_aplicativo, agendar_compromisso_google, pesquisar_na_web, executar_comando_cmd]

        resposta = ollama.chat(model=self.modelo, messages=lista_mensagens, tools=ferramentas, options={"temperature": 0.3})

        if resposta.get('message', {}).get('tool_calls'):
            for tool in resposta['message']['tool_calls']:
                funcao_nome = tool['function']['name']
                argumentos = tool['function']['arguments']
                # Execução dinâmica da ferramenta invocada
                return f"⚡ [Ação Executada]: {executar_ferramenta(funcao_nome, argumentos)}"

        return resposta["message"]["content"]
