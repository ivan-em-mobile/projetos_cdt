'''
criando arquivos por flask
'''

from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
# A secret_key é necessária para usar sessões (criptografia básica dos cookies)
app.secret_key = 'chave_secreta_para_o_salao'

# ----------------- BANCO DE DADOS EM MEMÓRIA (DADOS FIXOS) -----------------
# Usuários cadastrados (Simulando um banco de dados)
usuarios_db = {}

# Dados do Salão solicitados
CABELEIREIROS = ["Carlos", "Mariana", "Roberto"]

SERVICOS = {
    "Corte Masculino": 45.00,
    "Corte Feminino": 70.00,
    "Escova / Penteado": 60.00,
    "Coloração": 120.00,
    "Barba Completa": 35.00
}

DIAS_SEMANA = ["Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]

# ----------------- ROTAS DA APLICAÇÃO -----------------

# 1. Rota Inicial / Login e Cadastro
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verifica se o clique foi no botão de cadastrar ou logar
        acao = request.form.get('acao')
        usuario = request.form.get('usuario').strip()
        senha = request.form.get('senha').strip()

        if not usuario or not senha:
            flash("Por favor, preencha todos os campos.", "erro")
            return redirect(url_for('index'))

        if acao == 'cadastrar':
            if usuario in usuarios_db:
                flash("Este usuário já existe! Tente outro nome.", "erro")
            else:
                usuarios_db[usuario] = senha
                flash("Cadastro realizado com sucesso! Faça o login.", "sucesso")
            return redirect(url_for('login'))

        elif acao == 'index':
            if usuario in usuarios_db and usuarios_db[usuario] == senha:
                session['usuario_logado'] = usuario  # Salva o usuário na sessão
                return redirect(url_for('agenda'))
            else:
                flash("Usuário ou senha incorretos.", "erro")
                return redirect(url_for('index'))

    return render_template('index.html')


# 2. Rota do Painel de Agendamento (Área Protegida)
@app.route('/agenda', methods=['GET', 'POST'])
def agenda():
    # Proteção de rota: se não estiver logado, volta para o login
    if 'usuario_logado' not in session:
        flash("Você precisa estar logado para acessar a agenda.", "erro")
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Captura os dados selecionados no formulário
        cabeleireiro = request.form.get('cabeleireiro')
        servico = request.form.get('servico')
        dia = request.form.get('dia')
        
        # Como o serviço vem como texto, buscamos o preço no nosso dicionário
        preco = SERVICOS.get(servico, 0.0)

        # Guarda os dados do agendamento na sessão para exibir na tela de confirmação
        session['agendamento'] = {
            'cabeleireiro': cabeleireiro,
            'servico': servico,
            'preco': preco,
            'dia': dia
        }
        return redirect(url_for('confirmacao'))

    # Se for GET, renderiza a página passando as listas fixas para o HTML
    return render_template('agenda.html', 
                           usuario=session['usuario_logado'],
                           cabeleireiros=CABELEIREIROS, 
                           servicos=SERVICOS, 
                           dias=DIAS_SEMANA)


# 3. Rota de Confirmação
@app.route('/confirmacao')
def confirmacao():
    if 'usuario_logado' not in session or 'agendamento' not in session:
        return redirect(url_for('index'))
    
    dados = session['agendamento']
    return render_template('confirmacao.html', agendamento=dados)


# 4. Rota de Logout
@app.route('/logout')
def logout():
    session.clear() # Limpa a sessão do usuário
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)