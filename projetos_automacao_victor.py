import os
import time
import json
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ==========================================
# 1. ARQUIVOS HTML DAS PÁGINAS DO SITE
# ==========================================

INDEX_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>GymFit - Sua Academia de Alta Performance</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #121212; color: #ffffff; line-height: 1.6; }
        header { background-color: #1e1e1e; padding: 20px 50px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #ff4500; }
        .logo { font-size: 28px; font-weight: bold; color: #ff4500; text-transform: uppercase; }
        nav a { color: #ffffff; text-decoration: none; margin-left: 20px; font-weight: 500; transition: 0.3s; }
        nav a:hover, nav a.active { color: #ff4500; }
        .hero { height: 70vh; background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1200') center/cover; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 0 20px; }
        .hero h1 { font-size: 48px; margin-bottom: 15px; text-transform: uppercase; }
        .hero p { font-size: 20px; color: #ccc; margin-bottom: 25px; }
        .btn-principal { background-color: #ff4500; color: #ffffff; padding: 12px 30px; border: none; border-radius: 5px; font-size: 18px; font-weight: bold; text-decoration: none; cursor: pointer; }
        .btn-principal:hover { background-color: #e03e00; }
        footer { background-color: #0a0a0a; text-align: center; padding: 20px; color: #777; border-top: 1px solid #222; margin-top: 40px; }
    </style>
</head>
<body>
    <header>
        <div class="logo">GymFit</div>
        <nav>
            <a href="index.html" class="active">Início</a>
            <a href="planos.html">Planos</a>
            <a href="aulas.html">Agendar Aulas</a>
            <a href="login.html">Área do Aluno</a>
        </nav>
    </header>

    <section class="hero">
        <h1>Transforme Seu Corpo e Mente</h1>
        <p>A melhor estrutura e os melhores profissionais à sua disposição.</p>
        <a href="planos.html" class="btn-principal" id="btn-conhecer-planos">Conheça Nossos Planos</a>
    </section>

    <!-- CHATBOT FLUTUANTE INTEGRADO -->
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
                msgDiv.className = 'user-msg';
            } else {
                msgDiv.style.background = '#2a2a2a';
                msgDiv.style.color = '#fff';
                msgDiv.style.alignSelf = 'flex-start';
                msgDiv.className = 'bot-msg';
            }

            msgDiv.innerText = texto;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function responderBot(msg) {
            let resposta = "Desculpe, não entendi. Você pode perguntar sobre 'horário', 'planos', 'preço' ou 'modalidades'.";
            const texto = msg.toLowerCase();

            if (texto.includes('olá') || texto.includes('oi') || texto.includes('bom dia')) {
                resposta = "Olá! Seja bem-vindo à GymFit. Em que posso ajudar?";
            } else if (texto.includes('horário') || texto.includes('funciona')) {
                resposta = "Funcionamos de segunda a sexta das 06:00 às 23:00, e sábados das 08:00 às 16:00.";
            } else if (texto.includes('plano') || texto.includes('preço') || texto.includes('valor')) {
                resposta = "Temos o Plano Mensal (R$ 99/mês) e o Plano VIP (R$ 149/mês). Veja na página de Planos!";
            } else if (texto.includes('aula') || texto.includes('agendar')) {
                resposta = "Você pode agendar aulas de Crossfit, Spinning e Pilates na aba 'Agendar Aulas'.";
            }

            setTimeout(() => {
                adicionarMensagem(resposta, 'bot');
            }, 600);
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

    <footer>
        <p>&copy; 2026 GymFit. Todos os direitos reservados.</p>
    </footer>
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
        .card:hover { border-color: #ff4500; transform: translateY(-5px); transition: 0.3s; }
        .preco { font-size: 32px; color: #ff4500; font-weight: bold; margin: 15px 0; }
        ul { list-style: none; margin-bottom: 20px; text-align: left; }
        ul li { margin-bottom: 8px; color: #ccc; }
        .btn-assinar { background-color: #ff4500; color: #fff; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%; }
        .btn-assinar:hover { background-color: #e03e00; }
        .mensagem-sucesso { display: none; background: #28a745; color: #fff; padding: 15px; margin-top: 20px; border-radius: 5px; font-weight: bold; }
    </style>
</head>
<body>
    <header>
        <div class="logo">GymFit</div>
        <nav>
            <a href="index.html">Início</a>
            <a href="planos.html" class="active">Planos</a>
            <a href="aulas.html">Agendar Aulas</a>
            <a href="login.html">Área do Aluno</a>
        </nav>
    </header>

    <div class="container">
        <h1>Escolha o Plano Ideal para Você</h1>
        <div class="cards">
            <div class="card" id="card-mensal">
                <h3>Plano Mensal</h3>
                <div class="preco">R$ 99/mês</div>
                <ul>
                    <li>✓ Acesso à musculação</li>
                    <li>✓ Horário livre</li>
                    <li>✓ Sem fidelidade</li>
                </ul>
                <button class="btn-assinar" id="btn-assinar-mensal" onclick="assinar('Mensal')">Assinar Mensal</button>
            </div>
            <div class="card" id="card-vip">
                <h3>Plano VIP</h3>
                <div class="preco">R$ 149/mês</div>
                <ul>
                    <li>✓ Musculação + Aulas Especiais</li>
                    <li>✓ Acesso VIP em qualquer unidade</li>
                    <li>✓ Leve 1 acompanhante por mês</li>
                </ul>
                <button class="btn-assinar" id="btn-assinar-vip" onclick="assinar('VIP')">Assinar VIP</button>
            </div>
        </div>
        <div id="status-assinatura" class="mensagem-sucesso"></div>
    </div>

    <script>
        function assinar(plano) {
            const divStatus = document.getElementById('status-assinatura');
            divStatus.style.display = 'block';
            divStatus.innerText = '✅ Plano ' + plano + ' selecionado com sucesso! Redirecionando para área do aluno...';
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
        nav a:hover, nav a.active { color: #ff4500; }
        .container { max-width: 800px; margin: 40px auto; padding: 20px; background: #1e1e1e; border-radius: 8px; }
        h1 { color: #ff4500; text-align: center; margin-bottom: 20px; }
        .grid-aulas { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; }
        .aula-box { background: #121212; padding: 20px; border-radius: 8px; border: 1px solid #333; text-align: center; }
        .aula-box h3 { color: #ff4500; margin-bottom: 10px; }
        .btn-reservar { background: #28a745; color: #fff; border: none; padding: 10px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 10px; }
        .btn-reservar:hover { background: #218838; }
        #reserva-confirmada { display: none; background: #ff4500; color: #fff; padding: 15px; text-align: center; margin-top: 20px; border-radius: 5px; font-weight: bold; }
    </style>
</head>
<body>
    <header>
        <div class="logo">GymFit</div>
        <nav>
            <a href="index.html">Início</a>
            <a href="planos.html">Planos</a>
            <a href="aulas.html" class="active">Agendar Aulas</a>
            <a href="login.html">Área do Aluno</a>
        </nav>
    </header>

    <div class="container">
        <h1>Grade de Aulas Coletivas</h1>
        <div class="grid-aulas">
            <div class="aula-box">
                <h3>Crossfit</h3>
                <p>🕒 Seg / Quat - 07:00</p>
                <p>Vagas: 5 restantes</p>
                <button class="btn-reservar" id="btn-reservar-crossfit" onclick="reservar('Crossfit 07:00')">Reservar Vaga</button>
            </div>
            <div class="aula-box">
                <h3>Spinning</h3>
                <p>🕒 Ter / Quinta - 18:00</p>
                <p>Vagas: 2 restantes</p>
                <button class="btn-reservar" id="btn-reservar-spinning" onclick="reservar('Spinning 18:00')">Reservar Vaga</button>
            </div>
            <div class="aula-box">
                <h3>Pilates</h3>
                <p>🕒 Seg / Sex - 19:30</p>
                <p>Vagas: 3 restantes</p>
                <button class="btn-reservar" id="btn-reservar-pilates" onclick="reservar('Pilates 19:30')">Reservar Vaga</button>
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
        nav a:hover, nav a.active { color: #ff4500; }
        .form-container { max-width: 400px; margin: 60px auto; background-color: #1e1e1e; padding: 30px; border-radius: 8px; text-align: center; }
        .form-container h2 { margin-bottom: 20px; color: #ff4500; }
        .input-group { margin-bottom: 15px; text-align: left; }
        .input-group label { display: block; margin-bottom: 5px; font-size: 14px; }
        .input-group input { width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #333; background-color: #121212; color: #fff; }
        .btn-submit { width: 100%; background-color: #ff4500; color: #fff; padding: 10px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; }
        .btn-submit:hover { background-color: #e03e00; }
        #mensagem-login { display: none; margin-top: 15px; padding: 10px; border-radius: 4px; font-weight: bold; }
    </style>
</head>
<body>
    <header>
        <div class="logo">GymFit</div>
        <nav>
            <a href="index.html">Início</a>
            <a href="planos.html">Planos</a>
            <a href="aulas.html">Agendar Aulas</a>
            <a href="login.html" class="active">Área do Aluno</a>
        </nav>
    </header>

    <div class="form-container">
        <h2>Área do Aluno</h2>
        <form id="form-login" onsubmit="realizarLogin(event)">
            <div class="input-group">
                <label for="username">Usuário ou CPF</label>
                <input type="text" id="username" name="username" placeholder="Digite seu usuário" required>
            </div>
            <div class="input-group">
                <label for="password">Senha</label>
                <input type="password" id="password" name="password" placeholder="Digite sua senha" required>
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
            msg.style.background = '#28a745';
            msg.style.color = '#fff';
            msg.innerText = 'Bem-vindo(a), ' + user + '! Login autenticado com sucesso.';
        }
    </script>
</body>
</html>
"""

def criar_arquivos_site():
    caminho = os.path.dirname(os.path.abspath(__file__))
    paginas = {
        "index.html": INDEX_HTML,
        "planos.html": PLANOS_HTML,
        "aulas.html": AULAS_HTML,
        "login.html": LOGIN_HTML
    }
    for nome_arq, conteudo in paginas.items():
        with open(os.path.join(caminho, nome_arq), "w", encoding="utf-8") as f:
            f.write(conteudo)

# ==========================================
# 2. MOTOR DE AUTOMAÇÕES SELENIUM
# ==========================================

class AutomacaoGymFit:
    def __init__(self):
        self.caminho_base = os.path.dirname(os.path.abspath(__file__))

    def iniciar_driver(self):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        return driver, WebDriverWait(driver, 10)

    def automacao_login(self, usuario, senha):
        driver, wait = self.iniciar_driver()
        try:
            url = f"file:///{os.path.join(self.caminho_base, 'login.html')}"
            driver.get(url)
            
            campo_user = wait.until(EC.presence_of_element_located((By.ID, "username")))
            campo_user.send_keys(usuario)
            
            campo_pwd = driver.find_element(By.ID, "password")
            campo_pwd.send_keys(senha)
            
            btn = driver.find_element(By.ID, "btn-entrar")
            btn.click()
            time.sleep(4)
        finally:
            driver.quit()

    def automacao_assinar_plano(self, tipo_plano):
        driver, wait = self.iniciar_driver()
        try:
            url = f"file:///{os.path.join(self.caminho_base, 'planos.html')}"
            driver.get(url)
            
            btn_id = "btn-assinar-vip" if tipo_plano.lower() == "vip" else "btn-assinar-mensal"
            btn = wait.until(EC.element_to_be_clickable((By.ID, btn_id)))
            btn.click()
            time.sleep(4)
        finally:
            driver.quit()

    def automacao_agendar_aula(self, modalidade):
        driver, wait = self.iniciar_driver()
        try:
            url = f"file:///{os.path.join(self.caminho_base, 'aulas.html')}"
            driver.get(url)
            
            modalidade_lower = modalidade.lower()
            if "crossfit" in modalidade_lower:
                btn_id = "btn-reservar-crossfit"
            elif "spinning" in modalidade_lower:
                btn_id = "btn-reservar-spinning"
            else:
                btn_id = "btn-reservar-pilates"
                
            btn = wait.until(EC.element_to_be_clickable((By.ID, btn_id)))
            btn.click()
            time.sleep(4)
        finally:
            driver.quit()

    def automacao_chatbot(self, mensagem_usuario):
        driver, wait = self.iniciar_driver()
        try:
            url = f"file:///{os.path.join(self.caminho_base, 'index.html')}"
            driver.get(url)
            
            input_chat = wait.until(EC.presence_of_element_located((By.ID, "chat-input")))
            input_chat.send_keys(mensagem_usuario)
            
            btn_enviar = driver.find_element(By.ID, "btn-chat-enviar")
            btn_enviar.click()
            time.sleep(4)
        finally:
            driver.quit()

# ==========================================
# 3. INTERFACE GRAPHICA TKINTER COMPLETA
# ==========================================

def rodar_em_thread(funcao, *args):
    t = threading.Thread(target=funcao, args=args)
    t.daemon = True
    t.start()

def iniciar_interface():
    criar_arquivos_site()
    bot_engine = AutomacaoGymFit()

    janela = tk.Tk()
    janela.title("Painel de Controle GymFit - Automações")
    janela.geometry("450x520")
    janela.configure(bg="#121212")

    title_label = tk.Label(janela, text="⚙️ Automações GymFit", font=("Segoe UI", 16, "bold"), bg="#121212", fg="#ff4500")
    title_label.pack(pady=15)

    notebook = ttk.Notebook(janela)
    notebook.pack(fill="both", expand=True, padx=15, pady=10)

    # ESTILIZAÇÃO DAS ABAS DA INTERFACE
    style = ttk.Style()
    style.theme_use('default')
    style.configure('TNotebook', background='#121212', borderwidth=0)
    style.configure('TNotebook.Tab', background='#1e1e1e', foreground='#ffffff', padding=[10, 5])
    style.map('TNotebook.Tab', background=[('selected', '#ff4500')], foreground=[('selected', '#ffffff')])

    # TAB 1: LOGIN
    tab_login = tk.Frame(notebook, bg="#1e1e1e")
    notebook.add(tab_login, text="🔑 Login")

    tk.Label(tab_login, text="Usuário:", bg="#1e1e1e", fg="#ffffff").pack(anchor="w", padx=20, pady=(15,0))
    ent_user = tk.Entry(tab_login, width=35)
    ent_user.insert(0, "aluno_testador")
    ent_user.pack(padx=20, pady=5)

    tk.Label(tab_login, text="Senha:", bg="#1e1e1e", fg="#ffffff").pack(anchor="w", padx=20, pady=(10,0))
    ent_pass = tk.Entry(tab_login, show="*", width=35)
    ent_pass.insert(0, "senha12345")
    ent_pass.pack(padx=20, pady=5)

    btn_login = tk.Button(
        tab_login, text="Testar Automação de Login", 
        command=lambda: rodar_em_thread(bot_engine.automacao_login, ent_user.get(), ent_pass.get()),
        bg="#ff4500", fg="#ffffff", font=("Arial", 10, "bold"), padx=10, pady=5
    )
    btn_login.pack(pady=20)

    # TAB 2: PLANOS
    tab_planos = tk.Frame(notebook, bg="#1e1e1e")
    notebook.add(tab_planos, text="💳 Planos")

    tk.Label(tab_planos, text="Escolha o Plano para Testar:", bg="#1e1e1e", fg="#ffffff").pack(pady=15)
    var_plano = tk.StringVar(value="VIP")
    
    rb_mensal = tk.Radiobutton(tab_planos, text="Plano Mensal (R$ 99)", variable=var_plano, value="Mensal", bg="#1e1e1e", fg="#ffffff", selectcolor="#121212")
    rb_mensal.pack(anchor="w", padx=40, pady=5)
    
    rb_vip = tk.Radiobutton(tab_planos, text="Plano VIP (R$ 149)", variable=var_plano, value="VIP", bg="#1e1e1e", fg="#ffffff", selectcolor="#121212")
    rb_vip.pack(anchor="w", padx=40, pady=5)

    btn_plano = tk.Button(
        tab_planos, text="Testar Assinatura", 
        command=lambda: rodar_em_thread(bot_engine.automacao_assinar_plano, var_plano.get()),
        bg="#ff4500", fg="#ffffff", font=("Arial", 10, "bold"), padx=10, pady=5
    )
    btn_plano.pack(pady=20)

    # TAB 3: AULAS
    tab_aulas = tk.Frame(notebook, bg="#1e1e1e")
    notebook.add(tab_aulas, text="🏋️ Aulas")

    tk.Label(tab_aulas, text="Selecione a Aula Coletiva:", bg="#1e1e1e", fg="#ffffff").pack(pady=15)
    var_aula = tk.StringVar(value="Spinning")
    
    cb_aula = ttk.Combobox(tab_aulas, textvariable=var_aula, values=["Crossfit", "Spinning", "Pilates"], state="readonly")
    cb_aula.pack(pady=10)

    btn_aula = tk.Button(
        tab_aulas, text="Testar Reserva de Aula", 
        command=lambda: rodar_em_thread(bot_engine.automacao_agendar_aula, var_aula.get()),
        bg="#ff4500", fg="#ffffff", font=("Arial", 10, "bold"), padx=10, pady=5
    )
    btn_aula.pack(pady=20)

    # TAB 4: CHATBOT
    tab_chat = tk.Frame(notebook, bg="#1e1e1e")
    notebook.add(tab_chat, text="💬 Chatbot")

    tk.Label(tab_chat, text="Enviar Mensagem ao Chatbot:", bg="#1e1e1e", fg="#ffffff").pack(pady=15)
    ent_chat = tk.Entry(tab_chat, width=35)
    ent_chat.insert(0, "Qual o horário de funcionamento?")
    ent_chat.pack(padx=20, pady=5)

    btn_chat = tk.Button(
        tab_chat, text="Testar Interação do Chatbot", 
        command=lambda: rodar_em_thread(bot_engine.automacao_chatbot, ent_chat.get()),
        bg="#ff4500", fg="#ffffff", font=("Arial", 10, "bold"), padx=10, pady=5
    )
    btn_chat.pack(pady=20)

    janela.mainloop()

if __name__ == "__main__":
    iniciar_interface()
