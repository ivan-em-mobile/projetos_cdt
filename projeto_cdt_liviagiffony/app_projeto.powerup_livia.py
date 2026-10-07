import sqlite3
from flask import Flask, request, redirect, url_for, render_template_string, session, Response
import hashlib
import os
import json

app = Flask(__name__)
app.secret_key = "power_up_sophia_2026"


# ============================================================
# CONEXÃO COM O BANCO DE DADOS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "power_up.db")


def conectar_banco():
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_hash_senha(senha):
    return hashlib.sha256(
        senha.encode("utf-8")
    ).hexdigest()


# ============================================================
# CARREGAR EXERCÍCIOS DO BANCO DE DADOS
# ============================================================

def carregar_exercicios():

    conexao = conectar_banco()

    try:

        registros = conexao.execute(
            """
            SELECT
                id,
                nome,
                grupo_muscular,
                musculos,
                execucao
            FROM exercicios
            ORDER BY id
            """
        ).fetchall()

    finally:

        conexao.close()

    exercicios = {}

    for registro in registros:

        grupo = registro["grupo_muscular"]

        if grupo not in exercicios:
            exercicios[grupo] = []

        exercicios[grupo].append({
            "id": registro["id"],
            "nome": registro["nome"],
            "musculos": registro["musculos"],
            "execucao": registro["execucao"]
        })

    return exercicios


# ============================================================
# GRUPOS RELACIONADOS
# ============================================================

GRUPOS_RELACIONADOS = {
    "gluteos": ["posteriores", "quadriceps"],
    "quadriceps": ["gluteos", "posteriores"],
    "posteriores": ["gluteos", "quadriceps"],
    "costas": ["biceps"],
    "peito": ["triceps"],
    "ombros": ["triceps"],
    "biceps": ["costas"],
    "triceps": ["peito"],
    "panturrilhas": ["quadriceps"],
    "abdomen": []
}


# ============================================================
# ESTILO
# ============================================================

ESTILO = """
<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: linear-gradient(135deg, #f5efff, #eee5ff);
    color: #302442;
}

a {
    text-decoration: none;
}

button,
input {
    font-family: inherit;
}

.logo {
    font-size: 27px;
    font-weight: 900;
    letter-spacing: 2px;
    color: #6f3fb5;
}

.botao {
    display: inline-block;
    border: none;
    background: linear-gradient(135deg, #8e5bd5, #6f3fb5);
    color: white;
    padding: 13px 22px;
    border-radius: 13px;
    font-size: 15px;
    font-weight: bold;
    cursor: pointer;
    transition: 0.2s;
}

.botao:hover {
    transform: translateY(-2px);
}

.voltar {
    display: inline-block;
    color: #6f3fb5;
    font-weight: bold;
    margin-bottom: 18px;
}

input {
    width: 100%;
    padding: 13px;
    border: 1px solid #d9cbed;
    border-radius: 12px;
    outline: none;
    background: white;
}

input:focus {
    border-color: #8e5bd5;
}

.container {
    width: 92%;
    max-width: 1100px;
    margin: auto;
}

.admin-card {
    width: 92%;
    max-width: 1000px;
    margin: 25px auto;
    background: white;
    padding: 25px;
    border-radius: 22px;
    box-shadow: 0 10px 30px rgba(70, 40, 100, 0.10);
    text-align: center;
}

.admin-card h2 {
    color: #6f3fb5;
}

</style>
"""


# ============================================================
# LOGIN
# ============================================================

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="pt-br">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Power Up - Login</title>

""" + ESTILO + """

<style>

.login-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 25px;
}

.login-box {
    width: 100%;
    max-width: 950px;
    min-height: 570px;
    background: white;
    border-radius: 25px;
    overflow: hidden;
    display: grid;
    grid-template-columns: 1fr 1fr;
    box-shadow: 0 15px 45px rgba(80, 45, 120, 0.15);
}

.login-left {
    background: linear-gradient(145deg, #8e5bd5, #61349f);
    color: white;
    padding: 55px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.login-left h1 {
    font-size: 45px;
    margin-bottom: 10px;
}

.login-left p {
    line-height: 1.7;
}

.login-right {
    padding: 55px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.campo {
    margin: 15px 0;
}

.campo label {
    display: block;
    margin-bottom: 7px;
    font-weight: bold;
}

.cadastro-link {
    text-align: center;
    margin-top: 20px;
}

.mensagem-erro {
    background: #ffeaea;
    border: 1px solid #f0b5b5;
    color: #a32d2d;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 15px;
}

@media(max-width: 750px) {

    .login-box {
        grid-template-columns: 1fr;
    }

    .login-left {
        display: none;
    }

    .login-right {
        padding: 35px 25px;
    }

}

</style>

</head>

<body>

<div class="login-page">

<div class="login-box">

<div class="login-left">

<h1>POWER UP</h1>

<p>
Seu espaço para conhecer exercícios,
montar treinos e receber auxílio da
assistente virtual Wendy.
</p>

</div>

<div class="login-right">

<div class="logo">POWER UP</div>

<h2>Entrar</h2>

<p>Entre para acessar sua conta.</p>

{% if erro %}

<div class="mensagem-erro">
{{ erro }}
</div>

{% endif %}

<form method="POST">

<div class="campo">

<label>E-mail ou usuário</label>

<input
    type="text"
    name="email"
    placeholder="Digite seu e-mail ou root"
    required
>

</div>

<div class="campo">

<label>Senha</label>

<input
    type="password"
    name="senha"
    placeholder="Digite sua senha"
    required
>

</div>

<button class="botao" type="submit">
Entrar
</button>

</form>

<div class="cadastro-link">

Ainda não possui cadastro?

<br><br>

<a href="{{ url_for('cadastro') }}" class="botao">
Criar conta
</a>

</div>

</div>

</div>

</div>

</body>
</html>
"""


# ============================================================
# CADASTRO
# ============================================================

CADASTRO_HTML = """
<!DOCTYPE html>
<html lang="pt-br">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Cadastro - Power Up</title>

""" + ESTILO + """

<style>

.cadastro-page {
    min-height: 100vh;
    padding: 35px 15px;
}

.cadastro-box {
    background: white;
    width: 100%;
    max-width: 800px;
    margin: auto;
    padding: 40px;
    border-radius: 25px;
    box-shadow: 0 15px 45px rgba(80, 45, 120, 0.12);
}

.cadastro-box h1 {
    text-align: center;
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.campo {
    margin-bottom: 5px;
}

.campo label {
    display: block;
    margin-bottom: 7px;
    font-weight: bold;
}

.botao-area {
    text-align: center;
    margin-top: 25px;
}

.mensagem-erro {
    background: #ffeaea;
    border: 1px solid #f0b5b5;
    color: #a32d2d;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 20px;
    text-align: center;
}

@media(max-width: 600px) {

    .cadastro-box {
        padding: 25px 20px;
    }

    .form-grid {
        grid-template-columns: 1fr;
    }

}

</style>

</head>

<body>

<div class="cadastro-page">

<div class="cadastro-box">

<a class="voltar" href="{{ url_for('login') }}">
← Voltar
</a>

<h1>Crie sua conta</h1>

<p style="text-align:center;">
Cadastre seus dados para acessar o Power Up.
</p>

{% if erro %}

<div class="mensagem-erro">
{{ erro }}
</div>

{% endif %}

<form method="POST">

<div class="form-grid">

<div class="campo">
<label>Nome</label>
<input type="text" name="nome" value="{{ dados.nome }}" required>
</div>

<div class="campo">
<label>E-mail</label>
<input type="email" name="email" value="{{ dados.email }}" required>
</div>

<div class="campo">
<label>Telefone</label>
<input type="text" name="telefone" value="{{ dados.telefone }}" required>
</div>

<div class="campo">
<label>CEP</label>
<input type="text" name="cep" value="{{ dados.cep }}" required>
</div>

<div class="campo">
<label>Data de nascimento</label>
<input type="date" name="data_nascimento" value="{{ dados.data_nascimento }}" required>
</div>

<div class="campo">
<label>Academia</label>
<input type="text" name="academia" value="{{ dados.academia }}" required>
</div>

<div class="campo">
<label>Senha</label>
<input type="password" name="senha" required>
</div>

<div class="campo">
<label>Confirmar senha</label>
<input type="password" name="confirmar_senha" required>
</div>

</div>

<div class="botao-area">

<button class="botao" type="submit">
Cadastrar
</button>

</div>

</form>

</div>

</div>

</body>
</html>
"""


# ============================================================
# HOME
# ============================================================

HOME_HTML = """
<!DOCTYPE html>
<html lang="pt-br">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Power Up</title>

""" + ESTILO + """

<style>

.home {
    min-height: 100vh;
}

.header {
    background: white;
    padding: 18px 5%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 15px rgba(70, 40, 100, 0.08);
}

.hero {
    text-align: center;
    padding: 65px 20px 35px;
}

.hero h1 {
    font-size: 42px;
    margin: 0;
}

.hero p {
    font-size: 18px;
    color: #665a75;
}

.cards {
    width: 92%;
    max-width: 1000px;
    margin: 25px auto;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 25px;
}

.card {
    background: white;
    padding: 30px;
    border-radius: 22px;
    box-shadow: 0 10px 30px rgba(70, 40, 100, 0.10);
}

.card h2 {
    color: #6f3fb5;
}

.wendy-float {
    position: fixed;
    right: 22px;
    bottom: 22px;
    background: #6f3fb5;
    color: white;
    padding: 15px 20px;
    border-radius: 30px;
    font-weight: bold;
}

@media(max-width: 700px) {

    .cards {
        grid-template-columns: 1fr;
    }

}

</style>

</head>

<body>

<div class="home">

<div class="header">

<div class="logo">POWER UP</div>

<a href="{{ url_for('sair') }}" class="voltar">
Sair
</a>

</div>

<div class="hero">

<h1>Olá, {{ nome }}! 💜</h1>

<p>Bem-vinda ao Power Up.</p>

</div>

<div class="cards">

<div class="card">

<h2>🏋️ Montar treino</h2>

<p>
Escolha seus objetivos, grupos musculares,
tempo disponível e os dias da semana.
</p>

<a href="{{ url_for('treino') }}" class="botao">
Montar meu treino
</a>

</div>

<div class="card">

<h2>💬 Wendy</h2>

<p>
Converse com a assistente virtual do Power Up
e tire dúvidas sobre exercícios.
</p>

<a href="{{ url_for('wendy') }}" class="botao">
Conversar com Wendy
</a>

</div>

</div>

{% if session.get("root") %}

<div class="admin-card">

<h2>👑 Área do administrador</h2>

<p>
Você está conectado como usuário root.
</p>

<a href="{{ url_for('exportar_json') }}" class="botao">
📄 Exportar usuários em JSON
</a>

</div>

{% endif %}

<a href="{{ url_for('wendy') }}" class="wendy-float">
💬 Wendy
</a>

</div>

</body>
</html>
"""


# ============================================================
# WENDY
# ============================================================

WENDY_HTML = """
<!DOCTYPE html>
<html lang="pt-br">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Wendy - Power Up</title>

""" + ESTILO + """

<style>

.wendy-page {
    min-height: 100vh;
    padding: 25px 15px;
}

.chat {
    width: 100%;
    max-width: 650px;
    margin: auto;
    background: white;
    border-radius: 25px;
    overflow: hidden;
    box-shadow: 0 15px 40px rgba(70, 40, 100, 0.15);
}

.chat-top {
    background: linear-gradient(135deg, #8e5bd5, #6f3fb5);
    padding: 22px;
    color: white;
    text-align: center;
}

.chat-top h1 {
    margin: 0;
}

.chat-body {
    padding: 30px;
}

.mensagem {
    background: #f0e8fb;
    padding: 17px;
    border-radius: 17px;
    line-height: 1.6;
    margin-bottom: 20px;
}

.perguntas {
    display: grid;
    gap: 12px;
}

.pergunta {
    background: white;
    border: 1px solid #d9cbed;
    border-radius: 14px;
    padding: 14px;
    color: #5b348c;
    font-weight: bold;
}

</style>

</head>

<body>

<div class="wendy-page">

<a href="{{ url_for('home') }}" class="voltar">
← Início
</a>

<div class="chat">

<div class="chat-top">

<div style="font-size:45px;">👩🏻‍💻</div>

<h1>Wendy</h1>

<p>Sua assistente virtual</p>

</div>

<div class="chat-body">

<div class="mensagem">

Oi! Eu sou a Wendy 💜<br><br>

Posso ajudar você a conhecer os exercícios
e entender melhor como funciona o Power Up.

</div>

<div class="perguntas">

<a href="{{ url_for('treino') }}" class="pergunta">
🏋️ Quero montar meu treino
</a>

<a href="{{ url_for('duvidas_exercicios') }}" class="pergunta">
❓ Quero saber sobre exercícios
</a>

<a href="{{ url_for('home') }}" class="pergunta">
🏠 Voltar para o início
</a>

</div>

</div>

</div>

</div>

</body>
</html>
"""


# ============================================================
# DÚVIDAS SOBRE EXERCÍCIOS
# ============================================================

DUVIDAS_HTML = """
<!DOCTYPE html>
<html lang="pt-br">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Dúvidas sobre exercícios - Power Up</title>

""" + ESTILO + """

<style>

.duvidas-page {
    min-height: 100vh;
    padding: 25px 15px 50px;
}

.duvidas-box {
    width: 100%;
    max-width: 850px;
    margin: auto;
    background: white;
    padding: 35px;
    border-radius: 25px;
    box-shadow: 0 15px 40px rgba(70, 40, 100, 0.12);
}

.duvidas-box h1 {
    text-align: center;
}

.introducao {
    text-align: center;
    color: #665a75;
    margin-bottom: 30px;
}

.exercicio-duvida {
    border: 1px solid #dfd4ed;
    border-radius: 15px;
    margin-bottom: 12px;
    overflow: hidden;
}

.exercicio-duvida summary {
    list-style: none;
    cursor: pointer;
    padding: 18px 20px;
    font-weight: bold;
    color: #5b348c;
    display: flex;
    justify-content: space-between;
}

.exercicio-duvida summary::-webkit-details-marker {
    display: none;
}

.exercicio-duvida summary::after {
    content: "⌄";
    font-size: 22px;
}

.exercicio-conteudo {
    padding: 15px 20px 20px;
    background: #faf8ff;
    border-top: 1px solid #eee5f7;
    line-height: 1.6;
}

</style>

</head>

<body>

<div class="duvidas-page">

<a href="{{ url_for('wendy') }}" class="voltar">
← Voltar para Wendy
</a>

<div class="duvidas-box">

<h1>❓ Dúvidas sobre exercícios</h1>

<p class="introducao">
Clique em um exercício para ver os músculos trabalhados
e entender como realizar o movimento.
</p>

{% for exercicio in exercicios %}

<details class="exercicio-duvida">

<summary>
{{ exercicio.nome }}
</summary>

<div class="exercicio-conteudo">

<p>
<strong>Músculos trabalhados:</strong>
{{ exercicio.musculos }}
</p>

<p>
<strong>Como executar:</strong><br>
{{ exercicio.execucao }}
</p>

</div>

</details>

{% endfor %}

<br>

<div style="text-align:center;">

<a href="{{ url_for('treino') }}" class="botao">
🏋️ Montar meu treino
</a>

</div>

</div>

</div>

</body>
</html>
"""


# ============================================================
# MONTAR TREINO
# ============================================================

TREINO_HTML = """
<!DOCTYPE html>
<html lang="pt-br">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Montar treino - Power Up</title>

""" + ESTILO + """

<style>

.treino-page {
    min-height: 100vh;
    padding: 25px 15px 50px;
}

.treino-box {
    background: white;
    width: 100%;
    max-width: 1000px;
    margin: auto;
    padding: 35px;
    border-radius: 25px;
    box-shadow: 0 15px 40px rgba(70, 40, 100, 0.12);
}

.treino-box h1 {
    text-align: center;
}

.secao {
    margin: 30px 0;
}

.secao h2 {
    color: #6f3fb5;
    font-size: 20px;
}

.opcoes {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.opcao input {
    display: none;
}

.opcao label {
    display: block;
    padding: 12px 16px;
    border: 1px solid #d9cbed;
    border-radius: 13px;
    cursor: pointer;
    background: #faf8ff;
}

.opcao input:checked + label {
    background: #e7d9fa;
    border-color: #8e5bd5;
    color: #5b348c;
    font-weight: bold;
}

.gerar-area {
    text-align: center;
    margin-top: 35px;
}

</style>

</head>

<body>

<div class="treino-page">

<div style="max-width:1100px;margin:0 auto 25px;display:flex;justify-content:space-between;align-items:center;">

<div class="logo">
POWER UP
</div>

<a href="{{ url_for('home') }}" class="botao">
← Início
</a>

</div>

<div class="treino-box">

<h1>Monte seu treino 💜</h1>

<p style="text-align:center;">
Escolha as opções abaixo para que o sistema gere automaticamente uma sugestão.
</p>

<form method="POST">

<div class="secao">

<h2>🎯 Escolha até 2 objetivos</h2>

<div class="opcoes">

<div class="opcao">
<input type="checkbox" id="obj1" name="objetivos" value="Ganhar massa muscular">
<label for="obj1">Ganhar massa muscular</label>
</div>

<div class="opcao">
<input type="checkbox" id="obj2" name="objetivos" value="Melhorar condicionamento">
<label for="obj2">Melhorar condicionamento</label>
</div>

<div class="opcao">
<input type="checkbox" id="obj3" name="objetivos" value="Fortalecer o corpo">
<label for="obj3">Fortalecer o corpo</label>
</div>

<div class="opcao">
<input type="checkbox" id="obj4" name="objetivos" value="Melhorar resistência">
<label for="obj4">Melhorar resistência</label>
</div>

</div>

</div>

<div class="secao">

<h2>💪 Escolha até 3 grupos musculares</h2>

<div class="opcoes">

{% for chave, nome in grupos %}

<div class="opcao">

<input
    type="checkbox"
    id="{{ chave }}"
    name="grupos"
    value="{{ chave }}"
>

<label for="{{ chave }}">
{{ nome }}
</label>

</div>

{% endfor %}

</div>

</div>

<div class="secao">

<h2>📅 Escolha os dias da semana</h2>

<div class="opcoes">

{% for dia in dias %}

<div class="opcao">

<input
    type="checkbox"
    id="{{ dia }}"
    name="dias"
    value="{{ dia }}"
>

<label for="{{ dia }}">
{{ dia }}
</label>

</div>

{% endfor %}

</div>

</div>

<div class="secao">

<h2>⏱️ Tempo disponível por treino</h2>

<div class="opcoes">

<div class="opcao">
<input type="radio" id="tempo30" name="tempo" value="30" required>
<label for="tempo30">30 minutos</label>
</div>

<div class="opcao">
<input type="radio" id="tempo45" name="tempo" value="45">
<label for="tempo45">45 minutos</label>
</div>

<div class="opcao">
<input type="radio" id="tempo60" name="tempo" value="60">
<label for="tempo60">60 minutos</label>
</div>

<div class="opcao">
<input type="radio" id="tempo90" name="tempo" value="90">
<label for="tempo90">90 minutos</label>
</div>

</div>

</div>

<div class="secao">

<h2>📈 Nível de experiência</h2>

<div class="opcoes">

<div class="opcao">
<input type="radio" id="iniciante" name="experiencia" value="Iniciante" required>
<label for="iniciante">Iniciante</label>
</div>

<div class="opcao">
<input type="radio" id="intermediario" name="experiencia" value="Intermediário">
<label for="intermediario">Intermediário</label>
</div>

<div class="opcao">
<input type="radio" id="avancado" name="experiencia" value="Avançado">
<label for="avancado">Avançado</label>
</div>

</div>

</div>

<div class="gerar-area">

<button class="botao" type="submit">
✨ Gerar meu treino
</button>

</div>

</form>

</div>

</div>

</body>
</html>
"""


# ============================================================
# RESULTADO
# ============================================================

RESULTADO_HTML = """
<!DOCTYPE html>
<html lang="pt-br">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Seu treino - Power Up</title>

""" + ESTILO + """

<style>

.resultado-page {
    min-height: 100vh;
    padding: 25px 15px 50px;
}

.resultado-box {
    background: white;
    width: 100%;
    max-width: 950px;
    margin: auto;
    padding: 35px;
    border-radius: 25px;
    box-shadow: 0 15px 40px rgba(70, 40, 100, 0.12);
}

.resumo {
    background: #f3ecfc;
    padding: 20px;
    border-radius: 17px;
    margin: 25px 0;
    line-height: 1.8;
}

.dia {
    margin-top: 35px;
}

.dia h2 {
    color: #6f3fb5;
}

.exercicio {
    border: 1px solid #dfd4ed;
    border-radius: 17px;
    margin: 15px 0;
    padding: 20px;
    background: #fff;
}

.exercicio h3 {
    color: #5b348c;
}

.exercicio p {
    line-height: 1.65;
}

.aviso {
    background: #fff8e8;
    border: 1px solid #ead7a5;
    padding: 18px;
    border-radius: 15px;
    margin-top: 30px;
    line-height: 1.6;
}

</style>

</head>

<body>

<div class="resultado-page">

<div style="width:100%;max-width:1100px;margin:0 auto 25px;display:flex;justify-content:space-between;align-items:center;">

<div class="logo">
POWER UP
</div>

<a href="{{ url_for('home') }}" class="botao">
← Início
</a>

</div>

<div class="resultado-box">

<h1>Seu treino foi montado! 💜</h1>

<div class="resumo">

<strong>Objetivos:</strong>
{{ objetivos|join(", ") }}

<br>

<strong>Grupos musculares:</strong>
{{ grupos_nomes|join(", ") }}

<br>

<strong>Tempo:</strong>
{{ tempo }} minutos

<br>

<strong>Nível:</strong>
{{ experiencia }}

</div>

{% for dia, exercicios in semana.items() %}

<div class="dia">

<h2>📅 {{ dia }}</h2>

{% for exercicio in exercicios %}

<div class="exercicio">

<h3>{{ exercicio.nome }}</h3>

<p>
<strong>Músculos trabalhados:</strong>
{{ exercicio.musculos }}
</p>

<p>
<strong>Como executar:</strong><br>
{{ exercicio.execucao }}
</p>

</div>

{% endfor %}

</div>

{% endfor %}

<div class="aviso">

<strong>⚠️ Aviso:</strong><br>

Este treino é uma sugestão gerada automaticamente
para fins educativos e demonstrativos. Ele não substitui
a orientação de um profissional de Educação Física.

</div>

<br>

<div style="text-align:center;">

<a href="{{ url_for('treino') }}" class="botao">
Montar outro treino
</a>

</div>

</div>

</div>

</body>
</html>
"""


# ============================================================
# FUNÇÕES DO SISTEMA
# ============================================================

def escolher_quantidade_exercicios(tempo, experiencia):

    if tempo <= 30:
        quantidade = 3

    elif tempo <= 45:
        quantidade = 4

    elif tempo <= 60:
        quantidade = 6

    else:
        quantidade = 8

    if experiencia == "Iniciante":
        quantidade = max(2, quantidade - 1)

    return quantidade


def montar_semana(dias, grupos, tempo, experiencia):

    exercicios_banco = carregar_exercicios()

    semana = {}

    if not grupos:
        grupos = ["gluteos"]

    quantidade = escolher_quantidade_exercicios(
        tempo,
        experiencia
    )

    grupos_finais = list(grupos)

    for grupo in grupos:

        for relacionado in GRUPOS_RELACIONADOS.get(grupo, []):

            if relacionado not in grupos_finais:
                grupos_finais.append(relacionado)

    todos_exercicios = []

    for grupo in grupos_finais:

        for exercicio in exercicios_banco.get(grupo, []):

            if exercicio not in todos_exercicios:
                todos_exercicios.append(exercicio)

    if not todos_exercicios:

        for exercicios in exercicios_banco.values():

            for exercicio in exercicios:

                if exercicio not in todos_exercicios:
                    todos_exercicios.append(exercicio)

    if not todos_exercicios:
        return {}

    if not dias:
        dias = ["Segunda-feira"]

    for indice, dia in enumerate(dias):

        inicio = (
            indice * quantidade
        ) % len(todos_exercicios)

        exercicios_dia = []

        for i in range(quantidade):

            posicao = (
                inicio + i
            ) % len(todos_exercicios)

            exercicio = todos_exercicios[posicao]

            if exercicio not in exercicios_dia:
                exercicios_dia.append(exercicio)

        semana[dia] = exercicios_dia

    return semana


# ============================================================
# LOGIN
# ============================================================

@app.route("/", methods=["GET", "POST"])
def login():

    erro = None

    if request.method == "POST":

        login = request.form.get(
            "email",
            ""
        ).strip().lower()

        senha = request.form.get(
            "senha",
            ""
        )

        # ROOT
        if login == "root" and senha == "root":

            session["usuario_id"] = 0
            session["nome"] = "Administrador"
            session["email"] = "root"
            session["root"] = True

            return redirect(url_for("home"))

        # USUÁRIO NORMAL

        senha_hash = criar_hash_senha(senha)

        conexao = conectar_banco()

        try:

            usuario = conexao.execute(
                """
                SELECT *
                FROM usuarios
                WHERE email = ?
                AND senha = ?
                """,
                (
                    login,
                    senha_hash
                )
            ).fetchone()

        except sqlite3.Error:

            usuario = None

        finally:

            conexao.close()

        if usuario:

            session["usuario_id"] = usuario["id"]
            session["nome"] = usuario["nome"]
            session["email"] = usuario["email"]
            session["root"] = False

            return redirect(url_for("home"))

        erro = "E-mail ou senha incorretos."

    return render_template_string(
        LOGIN_HTML,
        erro=erro
    )


# ============================================================
# CADASTRO
# ============================================================

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    erro = None

    dados = {
        "nome": "",
        "email": "",
        "telefone": "",
        "cep": "",
        "data_nascimento": "",
        "academia": ""
    }

    if request.method == "POST":

        nome = request.form.get(
            "nome",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        telefone = request.form.get(
            "telefone",
            ""
        ).strip()

        cep = request.form.get(
            "cep",
            ""
        ).strip()

        data_nascimento = request.form.get(
            "data_nascimento",
            ""
        ).strip()

        academia = request.form.get(
            "academia",
            ""
        ).strip()

        senha = request.form.get(
            "senha",
            ""
        )

        confirmar = request.form.get(
            "confirmar_senha",
            ""
        )

        dados = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "cep": cep,
            "data_nascimento": data_nascimento,
            "academia": academia
        }

        if senha != confirmar:

            erro = "As senhas não são iguais."

            return render_template_string(
                CADASTRO_HTML,
                erro=erro,
                dados=dados
            )

        senha_hash = criar_hash_senha(senha)

        conexao = conectar_banco()

        try:

            conexao.execute(
                """
                INSERT INTO usuarios (
                    nome,
                    email,
                    telefone,
                    cep,
                    data_nascimento,
                    academia,
                    senha
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    nome,
                    email,
                    telefone,
                    cep,
                    data_nascimento,
                    academia,
                    senha_hash
                )
            )

            conexao.commit()

            usuario = conexao.execute(
                """
                SELECT *
                FROM usuarios
                WHERE email = ?
                """,
                (email,)
            ).fetchone()

            session["usuario_id"] = usuario["id"]
            session["nome"] = usuario["nome"]
            session["email"] = usuario["email"]
            session["root"] = False

            return redirect(url_for("home"))

        except sqlite3.IntegrityError:

            erro = "Este e-mail já está cadastrado."

        except sqlite3.Error:

            erro = "Não foi possível acessar o banco de dados."

        finally:

            conexao.close()

    return render_template_string(
        CADASTRO_HTML,
        erro=erro,
        dados=dados
    )


# ============================================================
# HOME
# ============================================================

@app.route("/home")
def home():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    return render_template_string(
        HOME_HTML,
        nome=session.get(
            "nome",
            "Usuária"
        )
    )


# ============================================================
# WENDY
# ============================================================

@app.route("/wendy")
def wendy():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    return render_template_string(
        WENDY_HTML
    )


# ============================================================
# DÚVIDAS SOBRE EXERCÍCIOS
# ============================================================

@app.route("/duvidas-exercicios")
def duvidas_exercicios():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    exercicios_banco = carregar_exercicios()

    exercicios = []

    for grupo in exercicios_banco.values():

        for exercicio in grupo:

            if exercicio not in exercicios:
                exercicios.append(exercicio)

    return render_template_string(
        DUVIDAS_HTML,
        exercicios=exercicios
    )


# ============================================================
# MONTAR TREINO
# ============================================================

@app.route("/treino", methods=["GET", "POST"])
def treino():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    grupos = [
        ("gluteos", "Glúteos"),
        ("quadriceps", "Quadríceps"),
        ("posteriores", "Posteriores"),
        ("panturrilhas", "Panturrilhas"),
        ("costas", "Costas"),
        ("peito", "Peito"),
        ("ombros", "Ombros"),
        ("biceps", "Bíceps"),
        ("triceps", "Tríceps"),
        ("abdomen", "Abdômen")
    ]

    dias = [
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo"
    ]

    if request.method == "POST":

        objetivos = request.form.getlist(
            "objetivos"
        )[:2]

        grupos_selecionados = request.form.getlist(
            "grupos"
        )[:3]

        dias_selecionados = request.form.getlist(
            "dias"
        )

        try:

            tempo = int(
                request.form.get(
                    "tempo",
                    30
                )
            )

        except ValueError:

            tempo = 30

        experiencia = request.form.get(
            "experiencia",
            "Iniciante"
        )

        semana = montar_semana(
            dias_selecionados,
            grupos_selecionados,
            tempo,
            experiencia
        )

        nomes_grupos = dict(grupos)

        grupos_nomes = [
            nomes_grupos.get(
                grupo,
                grupo
            )
            for grupo in grupos_selecionados
        ]

        if not grupos_nomes:
            grupos_nomes = ["Glúteos"]

        if not objetivos:
            objetivos = ["Fortalecer o corpo"]

        return render_template_string(
            RESULTADO_HTML,
            objetivos=objetivos,
            grupos_nomes=grupos_nomes,
            tempo=tempo,
            experiencia=experiencia,
            semana=semana
        )

    return render_template_string(
        TREINO_HTML,
        grupos=grupos,
        dias=dias
    )


# ============================================================
# EXPORTAR USUÁRIOS EM JSON
# SOMENTE ROOT
# ============================================================

@app.route("/exportar-json")
def exportar_json():

    if not session.get("root"):
        return redirect(url_for("login"))

    conexao = conectar_banco()

    try:

        usuarios = conexao.execute(
            """
            SELECT
                id,
                nome,
                email,
                telefone,
                cep,
                data_nascimento,
                academia
            FROM usuarios
            """
        ).fetchall()

    finally:

        conexao.close()

    dados = []

    for usuario in usuarios:

        dados.append({
            "id": usuario["id"],
            "nome": usuario["nome"],
            "email": usuario["email"],
            "telefone": usuario["telefone"],
            "cep": usuario["cep"],
            "data_nascimento": usuario["data_nascimento"],
            "academia": usuario["academia"]
        })

    arquivo_json = json.dumps(
        dados,
        ensure_ascii=False,
        indent=4
    )

    return Response(
        arquivo_json,
        mimetype="application/json",
        headers={
            "Content-Disposition":
            "attachment; filename=usuarios_power_up.json"
        }
    )


# ============================================================
# SAIR
# ============================================================

@app.route("/sair")
def sair():

    session.clear()

    return redirect(url_for("login"))


# ============================================================
# INICIAR SERVIDOR
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )