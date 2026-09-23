import os
import time
import threading
from flask import Flask, render_template_string, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# ==========================================
# 1. PÁGINAS HTML DA APLICAÇÃO
# ==========================================

INDEX_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>GymFit - Sua Academia de Alta Performance</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #0800a2; color: #ffffff; line-height: 1.6; }
        header { background-color: #0003b3; padding: 20px 50px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #003cff; }
        .logo { font-size: 28px; font-weight: bold; color: #1e52ed; text-transform: uppercase; }
        nav a { color: #ffffff; text-decoration: none; margin-left: 20px; font-weight: 500; }
        nav a:hover, nav a.active { color: #00bbff; }
        .hero { padding: 40px; text-align: center; }
        .hero h1 { color: #ffffff; margin-bottom: 10px; }
    </style>
</head>
<body>
    <header>
        <div class="logo">GymFit</div>
        <nav>
            <a href="/" class="active">Início</a>
            <a href="/planos">Planos</a>
            <a href="/aulas">Agendar Aulas</a>
            <a href="/login">Área do Aluno</a>
            <a href="/painel" style="color: #00e5ff; font-weight: bold;">[ Painel de Testes ]</a>
        </nav>
    </header>

    <section class="hero">
        <h1>Transforme Seu Corpo e Mente</h1>
        <p>A melhor estrutura e os melhores profissionais à sua disposição.</p>
        <br>
        <a href="/planos" style="color: #00e5ff; font-size: 18px;">Conheça Nossos Planos</a>
    </section>

    <!-- CHATBOT FLUTUANTE -->
    <div id="chatbot-container" style="position: fixed; bottom: 20px; right: 20px; width: 320px; background: #1e1e1e; border: 2px solid #ff4500; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); z-index: 9999;">
        <div id="chat-header" style="background: #ff4500; color: #fff; padding: 10px 15px; font-weight: bold; display: flex; justify-content: space-between; align-items: center;">
            <span>🤖 Assistente GymFit</span>
            <span id="chat-status" style="font-size: 11px; background: #28a745; padding: 2px 6px; border-radius: 4px;">Online</span>
        </div>
        <div id="chat-box" style="height: 220px; padding: 10px; overflow-y: auto; background: #141414; display: flex; flex-direction: column; gap: 8px;">
            <div class="bot-msg" style="background: #2a2a2a; color: #fff; padding: 8px 12px; border-radius: 8px; max-width: 85%; align-self: flex-start; font-size: 13px;">
                Olá! Sou o assistente virtual da GymFit. Como posso te ajudar hoje?
            </div>
        </div>
        <div style="display: flex; border-top: 1px solid #333;">
            <input type="text" id="chat-input" placeholder="Digite sua mensagem..." style="flex: 1; padding: 10px; background: #1e1e1e; border: none; color: #fff; font-size: 13px; outline: none;">
            <button id="btn-chat-enviar" style="background: #ff4500; border: none; color: #fff; padding: 10px 15px; cursor: pointer; font-weight: bold;">Enviar</button>
        </div>
    </div>

    <script>
        const chatInput = document.getElementById('chat-input');
        const btnEnviar = document.getElementById('btn-chat-enviar');
        const chatBox = document.getElementById('chat-box');

        function adicionarMensagem(texto, sender) {
            const msgDiv = document.createElement('div');
            msgDiv.style.padding = '8px 12px';
            msgDiv.style.borderRadius = '8px';
            msgDiv.style.maxWidth = '85%';
            msgDiv.style.fontSize = '13px';
            msgDiv.style.marginBottom = '5px';

            if(sender === 'user') {
                msgDiv.style.background = '#ff4500';
                msgDiv.style.color = '#fff';
                msgDiv.style.alignSelf = 'flex-end';
            } else {
                msgDiv.style.background = '#2a2a2a';
                msgDiv.style.color = '#fff';
                msgDiv.style.alignSelf = 'flex-start';
            }

            msgDiv.innerText = texto;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function responderBot(msg) {
            let resposta = "Desculpe, não entendi. Você pode perguntar sobre 'horário', 'planos' ou 'aulas'.";
            const texto = msg.toLowerCase();

            if (texto.includes('olá') || texto.includes('oi')) {
                resposta = "Olá! Seja bem-vindo à GymFit. Em que posso ajudar?";
            } else if (texto.includes('horário') || texto.includes('funciona')) {
                resposta = "Funcionamos de segunda a sexta das 06:00 às 23:00.";
            } else if (texto.includes('plano') || texto.includes('preço')) {
                resposta = "Temos o Plano Mensal (R$ 99/mês) e o Plano VIP (R$ 149/mês).";
            }

            setTimeout(() => { adicionarMensagem(resposta, 'bot'); }, 600);
        }

        btnEnviar.addEventListener('click', () => {
            const texto = chatInput.value.trim();
            if (texto) {
                adicionarMensagem(texto, 'user');
                chatInput.value = '';
                responderBot(texto);
            }
        });

        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') btnEnviar.click();
        });
    </script>
</body>
</html>
"""

PLANOS_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>GymFit - Nossos Planos</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #121212; color: #ffffff; line-height: 1.6; }
        header { background-color: #1e1e1e; padding: 20px 50px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #ff4500; }
        .logo { font-size: 28px; font-weight: bold; color: #ff4500; text-transform: uppercase; }
        nav a { color: #ffffff; text-decoration: none; margin-left: 20px; font-weight: 500; }
        nav a:hover, nav a.active { color: #ff4500; }
        .container { padding: 50px 20px; text-align: center; }
        h1 { color: #ff4500; margin-bottom: 30px; }
        .cards { display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; }
        .card { background-color: #1e1e1e; padding: 30px; border-radius: 8px; width: 300px; border: 1px solid #333; }
        .preco { font-size: 32px; color: #ff4500; font-weight: bold; margin: 15px 0; }
        .btn-assinar { background-color: #ff4500; color: #fff; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%; }
        .mensagem-sucesso { display: none; background: #28a745; color: #fff; padding: 15px; margin-top: 20px; border-radius: 5px; font-weight: bold; }
    </style>
</head>
<body>
    <header>
        <div class="logo">GymFit</div>
        <nav>
            <a href="/">Início</a>
            <a href="/planos" class="active">Planos</a>
            <a href="/aulas">Agendar Aulas</a>
            <a href="/login">Área do Aluno</a>
            <a href="/painel" style="color: #ff4500; font-weight: bold;">[ Painel de Testes ]</a>
        </nav>
    </header>

    <div class="container">
        <h1>Escolha o Plano Ideal para Você</h1>
        <div class="cards">
            <div class="card">
                <h3>Plano Mensal</h3>
                <div class="preco">R$ 99/mês</div>
                <button class="btn-assinar" id="btn-assinar-mensal" onclick="assinar('Mensal')">Assinar Mensal</button>
            </div>
            <div class="card">
                <h3>Plano VIP</h3>
                <div class="preco">R$ 149/mês</div>
                <button class="btn-assinar" id="btn-assinar-vip" onclick="assinar('VIP')">Assinar VIP</button>
            </div>
        </div>
        <div id="status-assinatura" class="mensagem-sucesso"></div>
    </div>

    <script>
        function assinar(plano) {
            const divStatus = document.getElementById('status-assinatura');
            divStatus.style.display = 'block';
            divStatus.innerText = '✅ Plano ' + plano + ' selecionado com sucesso!';
        }
    </script>
</body>
</html>
"""

AULAS_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>GymFit - Agendamento de Aulas</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #121212; color: #ffffff; line-height: 1.6; }
        header { background-color: #1e1e1e; padding: 20px 50px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #ff4500; }
        .logo { font-size: 28px; font-weight: bold; color: #ff4500; text-transform: uppercase; }
        nav a { color: #ffffff; text-decoration: none; margin-left: 20px; font-weight: 500; }
        .container { max-width: 800px; margin: 40px auto; padding: 20px; background: #1e1e1e; border-radius: 8px; }
        h1 { color: #ff4500; text-align: center; margin-bottom: 20px; }
        .grid-aulas { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; }
        .aula-box { background: #121212; padding: 20px; border-radius: 8px; border: 1px solid #333; text-align: center; }
        .btn-reservar { background: #28a745; color: #fff; border: none; padding: 10px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 10px; }
        #reserva-confirmada { display: none; background: #ff4500; color: #fff; padding: 15px; text-align: center; margin-top: 20px; border-radius: 5px; font-weight: bold; }
    </style>
</head>
<body>
    <header>
        <div class="logo">GymFit</div>
        <nav>
            <a href="/">Início</a>
            <a href="/planos">Planos</a>
            <a href="/aulas" class="active">Agendar Aulas</a>
            <a href="/login">Área do Aluno</a>
            <a href="/painel" style="color: #ff4500; font-weight: bold;">[ Painel de Testes ]</a>
        </nav>
    </header>

    <div class="container">
        <h1>Grade de Aulas Coletivas</h1>
        <div class="grid-aulas">
            <div class="aula-box">
                <h3>Crossfit</h3>
                <button class="btn-reservar" id="btn-reservar-crossfit" onclick="reservar('Crossfit')">Reservar Vaga</button>
            </div>
            <div class="aula-box">
                <h3>Spinning</h3>
                <button class="btn-reservar" id="btn-reservar-spinning" onclick="reservar('Spinning')">Reservar Vaga</button>
            </div>
            <div class="aula-box">
                <h3>Pilates</h3>
                <button class="btn-reservar" id="btn-reservar-pilates" onclick="reservar('Pilates')">Reservar Vaga</button>
            </div>
        </div>
        <div id="reserva-confirmada"></div>
    </div>

    <script>
        function reservar(aula) {
            const caixa = document.getElementById('reserva-confirmada');
            caixa.style.display = 'block';
            caixa.innerText = '🎉 Reserva realizada com sucesso para: ' + aula;
        }
    </script>
</body>
</html>
"""

LOGIN_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>GymFit - Área do Aluno</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #121212; color: #ffffff; line-height: 1.6; }
        header { background-color: #1e1e1e; padding: 20px 50px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #ff4500; }
        .logo { font-size: 28px; font-weight: bold; color: #ff4500; text-transform: uppercase; }
        nav a { color: #ffffff; text-decoration: none; margin-left: 20px; font-weight: 500; }
        .form-container { max-width: 400px; margin: 60px auto; background-color: #1e1e1e; padding: 30px; border-radius: 8px; text-align: center; }
        .input-group { margin-bottom: 15px; text-align: left; }
        .input-group label { display: block; margin-bottom: 5px; }
        .input-group input { width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #333; background-color: #121212; color: #fff; }
        .btn-submit { width: 100%; background-color: #ff4500; color: #fff; padding: 10px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; }
        #mensagem-login { display: none; margin-top: 15px; padding: 10px; border-radius: 4px; font-weight: bold; background: #28a745; color: #fff; }
    </style>
</head>
<body>
    <header>
        <div class="logo">GymFit</div>
        <nav>
            <a href="/">Início</a>
            <a href="/planos">Planos</a>
            <a href="/aulas">Agendar Aulas</a>
            <a href="/login" class="active">Área do Aluno</a>
            <a href="/painel" style="color: #ff4500; font-weight: bold;">[ Painel de Testes ]</a>
        </nav>
    </header>

    <div class="form-container">
        <h2>Área do Aluno</h2>
        <form id="form-login" onsubmit="realizarLogin(event)">
            <div class="input-group">
                <label for="username">Usuário</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="input-group">
                <label for="password">Senha</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" id="btn-entrar" class="btn-submit">Entrar</button>
        </form>
        <div id="mensagem-login"></div>
    </div>

    <script>
        function realizarLogin(event) {
            event.preventDefault();
            const user = document.getElementById('username').value;
            const msg = document.getElementById('mensagem-login');
            msg.style.display = 'block';
            msg.innerText = 'Bem-vindo(a), ' + user + '! Login autenticado.';
        }
    </script>
</body>
</html>
"""

PAINEL_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Painel de Controle - Automações</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #121212; color: #ffffff; padding: 40px; }
        .container { max-width: 600px; margin: 0 auto; background: #1e1e1e; padding: 30px; border-radius: 8px; border: 1px solid #ff4500; }
        h1 { color: #ff4500; margin-bottom: 20px; text-align: center; }
        .section { margin-bottom: 25px; padding-bottom: 15px; border-bottom: 1px solid #333; }
        label { display: block; margin-bottom: 8px; font-weight: bold; }
        input, select { width: 100%; padding: 10px; background: #121212; border: 1px solid #ff4500; color: #fff; border-radius: 4px; margin-bottom: 10px; }
        button { background: #ff4500; color: #fff; border: none; padding: 10px 20px; width: 100%; font-weight: bold; border-radius: 4px; cursor: pointer; }
        button:hover { background: #e03e00; }
        nav { margin-bottom: 20px; text-align: center; }
        nav a { color: #fff; text-decoration: none; margin: 0 10px; }
    </style>
</head>
<body>
    <nav>
        <a href="/">← Voltar ao Site GymFit</a>
    </nav>
    <div class="container">
        <h1>⚙️ Painel de Automações</h1>

        <div class="section">
            <h3>🔑 Testar Login</h3>
            <input type="text" id="user" value="aluno_testador" placeholder="Usuário">
            <input type="password" id="pass" value="senha12345" placeholder="Senha">
            <button onclick="executar('/executar-login', {usuario: document.getElementById('user').value, senha: document.getElementById('pass').value})">Disparar Login</button>
        </div>

        <div class="section">
            <h3>💳 Testar Assinatura de Plano</h3>
            <select id="plano">
                <option value="Mensal">Plano Mensal</option>
                <option value="VIP">Plano VIP</option>
            </select>
            <button onclick="executar('/executar-plano', {plano: document.getElementById('plano').value})">Disparar Plano</button>
        </div>

        <div class="section">
            <h3>🏋️ Testar Agendamento de Aula</h3>
            <select id="aula">
                <option value="Crossfit">Crossfit</option>
                <option value="Spinning">Spinning</option>
                <option value="Pilates">Pilates</option>
            </select>
            <button onclick="executar('/executar-aula', {aula: document.getElementById('aula').value})">Disparar Reserva</button>
        </div>

        <div class="section">
            <h3>💬 Testar Chatbot</h3>
            <input type="text" id="msg" value="Qual o horário de funcionamento?" placeholder="Mensagem">
            <button onclick="executar('/executar-chat', {mensagem: document.getElementById('msg').value})">Enviar ao Chatbot</button>
        </div>
    </div>

    <script>
        function executar(url, payload) {
            fetch(url, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            }).then(r => r.json()).then(d => alert(d.status));
        }
    </script>
</body>
</html>
"""

# ==========================================
# 2. MOTOR DE AUTOMAÇÕES SELENIUM
# ==========================================

class AutomacaoGymFit:
    def __init__(self, host_url="http://127.0.0.1:5000"):
        self.host_url = host_url

    def iniciar_driver(self):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        return driver, WebDriverWait(driver, 10)

    def automacao_login(self, usuario, senha):
        driver, wait = self.iniciar_driver()
        try:
            driver.get(f"{self.host_url}/login")
            campo_user = wait.until(EC.presence_of_element_located((By.ID, "username")))
            campo_user.send_keys(usuario)
            driver.find_element(By.ID, "password").send_keys(senha)
            driver.find_element(By.ID, "btn-entrar").click()
            time.sleep(4)
        finally:
            driver.quit()

    def automacao_assinar_plano(self, tipo_plano):
        driver, wait = self.iniciar_driver()
        try:
            driver.get(f"{self.host_url}/planos")
            btn_id = "btn-assinar-vip" if tipo_plano.lower() == "vip" else "btn-assinar-mensal"
            btn = wait.until(EC.element_to_be_clickable((By.ID, btn_id)))
            btn.click()
            time.sleep(4)
        finally:
            driver.quit()

    def automacao_agendar_aula(self, modalidade):
        driver, wait = self.iniciar_driver()
        try:
            driver.get(f"{self.host_url}/aulas")
            btn_id = f"btn-reservar-{modalidade.lower()}"
            btn = wait.until(EC.element_to_be_clickable((By.ID, btn_id)))
            btn.click()
            time.sleep(4)
        finally:
            driver.quit()

    def automacao_chatbot(self, mensagem_usuario):
        driver, wait = self.iniciar_driver()
        try:
            driver.get(f"{self.host_url}/")
            input_chat = wait.until(EC.presence_of_element_located((By.ID, "chat-input")))
            input_chat.send_keys(mensagem_usuario)
            driver.find_element(By.ID, "btn-chat-enviar").click()
            time.sleep(4)
        finally:
            driver.quit()

bot_engine = AutomacaoGymFit()

# ==========================================
# 3. ROTAS DO FLASK
# ==========================================

@app.route("/")
def home():
    return render_template_string(INDEX_HTML)

@app.route("/planos")
def planos():
    return render_template_string(PLANOS_HTML)

@app.route("/aulas")
def aulas():
    return render_template_string(AULAS_HTML)

@app.route("/login")
def login():
    return render_template_string(LOGIN_HTML)

@app.route("/painel")
def painel():
    return render_template_string(PAINEL_HTML)

# ROTAS PARA DISPARO DE AUTOMAÇÃO
@app.route("/executar-login", methods=["POST"])
def api_login():
    dados = request.get_json()
    threading.Thread(
        target=bot_engine.automacao_login, 
        args=(dados.get("usuario"), dados.get("senha"))
    ).start()
    return jsonify({"status": "Automação de Login iniciada no navegador!"})

@app.route("/executar-plano", methods=["POST"])
def api_plano():
    dados = request.get_json()
    threading.Thread(
        target=bot_engine.automacao_assinar_plano, 
        args=(dados.get("plano"),)
    ).start()
    return jsonify({"status": "Automação de Assinatura iniciada no navegador!"})

@app.route("/executar-aula", methods=["POST"])
def api_aula():
    dados = request.get_json()
    threading.Thread(
        target=bot_engine.automacao_agendar_aula, 
        args=(dados.get("aula"),)
    ).start()
    return jsonify({"status": "Automação de Agendamento iniciada no navegador!"})

@app.route("/executar-chat", methods=["POST"])
def api_chat():
    dados = request.get_json()
    threading.Thread(
        target=bot_engine.automacao_chatbot, 
        args=(dados.get("mensagem"),)
    ).start()
    return jsonify({"status": "Automação de Chatbot iniciada no navegador!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)