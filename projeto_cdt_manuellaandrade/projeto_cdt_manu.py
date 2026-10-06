from flask import Flask, render_template_string, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///impulsework.db'
app.config['SECRET_KEY'] = 'impulsework_chave_secreta'
db = SQLAlchemy(app)

# ==========================================
# MODELOS DO BANCO DE DADOS
# ==========================================

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    cargo = db.Column(db.String(100))
    resumo = db.Column(db.Text)
    formacoes = db.relationship('Formacao', backref='usuario', lazy=True)
    candidaturas = db.relationship('Candidatura', backref='usuario', lazy=True)

class Formacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    instituicao = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(100), nullable=False)
    ano_conclusao = db.Column(db.String(10))

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    site = db.Column(db.String(100))
    candidaturas = db.relationship('Candidatura', backref='empresa', lazy=True)

class Candidatura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Enviado")

# ==========================================
# TEMPLATE HTML (COM MODO CLARO E SOBRE COMPLETO)
# ==========================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ImpulseWork - Aceleração de Carreiras</title>
    <style>
        :root {
            /* Modo Escuro (Azul Dark) */
            --bg-base: #0F172A;
            --bg-card: #1E293B;
            --accent: #38BDF8;
            --accent-hover: #0284C7;
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
            --border: #334155;
            --input-bg: #0F172A;
            --card-sub: #172554;
        }

        body.light-theme {
            /* Modo Claro (Tons Azuis Suaves) */
            --bg-base: #F0F9FF;
            --bg-card: #FFFFFF;
            --accent: #0284C7;
            --accent-hover: #0369A1;
            --text-primary: #0F172A;
            --text-secondary: #475569;
            --border: #BAE6FD;
            --input-bg: #F8FAFC;
            --card-sub: #E0F2FE;
        }

        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--bg-base); color: var(--text-primary); margin: 0; padding: 20px; transition: all 0.3s ease; }
        header { display: flex; justify-content: space-between; align-items: center; max-width: 950px; margin: 0 auto 20px; border-bottom: 1px solid var(--border); padding-bottom: 15px; }
        h1 { color: var(--accent); margin: 0; font-size: 24px; }
        nav { display: flex; align-items: center; gap: 15px; }
        nav a { color: var(--text-primary); text-decoration: none; font-weight: 600; }
        nav a:hover { color: var(--accent); }
        
        .theme-toggle { background: var(--card-sub); border: 1px solid var(--border); color: var(--text-primary); padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 13px; font-weight: bold; }
        
        .container { max-width: 950px; margin: 0 auto; background: var(--bg-card); padding: 30px; border-radius: 10px; border: 1px solid var(--border); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
        
        .btn { background: var(--accent); color: #FFF; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn:hover { background: var(--accent-hover); }
        
        form label { display: block; margin-top: 15px; color: var(--text-secondary); font-weight: 500; }
        form input, form textarea, form select { width: 100%; padding: 10px; margin-top: 5px; background: var(--input-bg); border: 1px solid var(--border); color: var(--text-primary); border-radius: 6px; box-sizing: border-box; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid var(--border); }
        th { color: var(--accent); }
        .badge { background: #0284C7; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }

        .info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 15px; margin: 20px 0; }
        .info-card { background: var(--card-sub); padding: 18px; border-radius: 8px; border: 1px solid var(--border); }
        .info-card h4 { margin: 0 0 8px 0; color: var(--accent); }
        .info-card p { margin: 0; font-size: 14px; color: var(--text-secondary); }
    </style>
</head>
<body>
    <header>
        <h1>⚡ ImpulseWork</h1>
        <nav>
            <a href="/">Início / Criar Perfil</a>
            <a href="/minhas-candidaturas">Minhas Candidaturas</a>
            <a href="/cadastrar-empresa">Área da Empresa</a>
            <a href="/sobre">Sobre o App</a>
            <button class="theme-toggle" onclick="toggleTheme()">☀️ / 🌙 Tema</button>
        </nav>
    </header>

    <div class="container">
        {% if pagina == 'home' %}
            <h2>Impulsione o seu futuro profissional 🚀</h2>
            <p style="color: var(--text-secondary);">Preencha as suas informações para gerar o seu currículo e candidatar-se às empresas parceiras.</p>
            
            <form action="/salvar-curriculo" method="POST">
                <h3>1. Dados Pessoais e Profissionais</h3>
                <label>Nome Completo:</label>
                <input type="text" name="nome" required>
                
                <label>E-mail:</label>
                <input type="email" name="email" required>
                
                <label>Telefone / WhatsApp:</label>
                <input type="text" name="telefone" required>
                
                <label>Cargo Pretendido:</label>
                <input type="text" name="cargo" required>

                <h3>2. Formação Académica (Escolas e Cursos)</h3>
                <label>Nome da Escola / Instituição:</label>
                <input type="text" name="instituicao" placeholder="Ex: Universidade / Instituto Técnico" required>
                
                <label>Nome do Curso / Formação:</label>
                <input type="text" name="curso" placeholder="Ex: Engenharia de Software / Gestão" required>
                
                <label>Ano de Conclusão:</label>
                <input type="text" name="ano_conclusao" placeholder="Ex: 2024" required>

                <h3>3. Resumo Profissional</h3>
                <label>Breve Resumo:</label>
                <textarea name="resumo" rows="4" required></textarea>

                <h3>4. Onde Deseja Salvar / Enviar?</h3>
                <label>Selecione a ação:</label>
                <select name="opcao_salvar">
                    <option value="empresas">Candidatar-me a Todas as Empresas Parceiras</option>
                    <option value="download">Descarregar Ficheiro do Currículo (.txt)</option>
                </select>

                <br><br>
                <button type="submit" class="btn">Finalizar e Processar ➔</button>
            </form>

        {% elif pagina == 'candidaturas' %}
            <h2>📋 As Minhas Candidaturas</h2>
            <p style="color: var(--text-secondary);">Acompanhe abaixo as empresas onde o seu currículo foi registado:</p>
            {% if candidaturas %}
                <table>
                    <thead>
                        <tr>
                            <th>Empresa</th>
                            <th>Área de Atuação</th>
                            <th>Data do Envio</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for c in candidaturas %}
                        <tr>
                            <td><strong>{{ c.empresa.nome }}</strong></td>
                            <td>{{ c.empresa.area }}</td>
                            <td>{{ c.data_envio.strftime('%d/%m/%Y %H:%M') }}</td>
                            <td><span class="badge">{{ c.status }}</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% else %}
                <p style="color: var(--text-secondary);">Ainda não submeteu candidaturas para as empresas parceiras.</p>
            {% endif %}

        {% elif pagina == 'empresa' %}
            <h2>🏢 Cadastro de Empresas Parceiras</h2>
            <p style="color: var(--text-secondary);">Cadastre a sua empresa para receber os currículos dos candidatos da plataforma.</p>
            <form action="/salvar-empresa" method="POST">
                <label>Nome da Empresa:</label>
                <input type="text" name="nome" required>
                
                <label>Área de Atuação:</label>
                <input type="text" name="area" placeholder="Ex: Tecnologia, Finanças, Saúde" required>
                
                <label>Website / Link:</label>
                <input type="text" name="site" placeholder="https://exemplo.com">
                
                <br><br>
                <button type="submit" class="btn">Cadastrar Empresa</button>
            </form>

        {% elif pagina == 'sobre' %}
            <h2>ℹ️ Sobre a Plataforma ImpulseWork</h2>
            <p style="color: var(--text-secondary); line-height: 1.6;">
                O <strong>ImpulseWork</strong> é uma solução desenvolvida para conectar rapidamente profissionais qualificados às empresas contratantes. Centralizamos a criação do seu currículo e facilitamos a distribuição direta para vagas ativas.
            </p>

            <div class="info-grid">
                <div class="info-card">
                    <h4>🎯 Nossa Missão</h4>
                    <p>Facilitar a entrada de novos talentos no mercado de trabalho através de uma plataforma simples, eficiente e direta.</p>
                </div>
                <div class="info-card">
                    <h4>🚀 Como Funciona?</h4>
                    <p>Você cadastra seus dados e formação acadêmica uma única vez e pode enviar para várias empresas parceiras simultaneamente.</p>
                </div>
                <div class="info-card">
                    <h4>💡 Para as Empresas</h4>
                    <p>Centralização do banco de talentos, permitindo encontrar profissionais com o perfil ideal para cada setor.</p>
                </div>
            </div>

            <hr style="border-color: var(--border); margin: 25px 0;">

            <h3>🏢 Empresas Parceiras Cadastradas na Plataforma</h3>
            {% if empresas %}
                <table>
                    <thead>
                        <tr>
                            <th>Empresa</th>
                            <th>Área de Atuação</th>
                            <th>Website</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for emp in empresas %}
                        <tr>
                            <td><strong>{{ emp.nome }}</strong></td>
                            <td>{{ emp.area }}</td>
                            <td><a href="{{ emp.site }}" target="_blank" style="color: var(--accent);">Aceder ao site</a></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% else %}
                <p style="color: var(--text-secondary);">Nenhuma empresa cadastrada no momento. Você pode cadastrar novas empresas na aba "Área da Empresa".</p>
            {% endif %}
        {% endif %}
    </div>

    <script>
        function toggleTheme() {
            document.body.classList.toggle('light-theme');
            const isLight = document.body.classList.contains('light-theme');
            localStorage.setItem('theme', isLight ? 'light' : 'dark');
        }

        if (localStorage.getItem('theme') === 'light') {
            document.body.classList.add('light-theme');
        }
    </script>
</body>
</html>
"""

# ==========================================
# ROTAS DO SISTEMA
# ==========================================

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, pagina='home')

@app.route('/salvar-curriculo', methods=['POST'])
def salvar_curriculo():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    cargo = request.form.get('cargo')
    resumo = request.form.get('resumo')
    
    instituicao = request.form.get('instituicao')
    curso = request.form.get('curso')
    ano_conclusao = request.form.get('ano_conclusao')
    
    opcao = request.form.get('opcao_salvar')

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        usuario = Usuario(nome=nome, email=email, telefone=telefone, cargo=cargo, resumo=resumo)
        db.session.add(usuario)
        db.session.commit()

    formacao = Formacao(usuario_id=usuario.id, instituicao=instituicao, curso=curso, ano_conclusao=ano_conclusao)
    db.session.add(formacao)
    db.session.commit()

    if opcao == 'empresas':
        empresas = Empresa.query.all()
        for emp in empresas:
            existe = Candidatura.query.filter_by(usuario_id=usuario.id, empresa_id=emp.id).first()
            if not existe:
                candidatura = Candidatura(usuario_id=usuario.id, empresa_id=emp.id)
                db.session.add(candidatura)
        db.session.commit()
        return redirect(url_for('minhas_candidaturas'))

    elif opcao == 'download':
        conteudo = f"""==================================================
CURRÍCULO - {nome.upper()}
==================================================
Cargo: {cargo}
Email: {email} | Telefone: {telefone}

FORMAÇÃO ACADÉMICA:
- {curso} ({instituicao}) - Conclusão: {ano_conclusao}

RESUMO PROFISSIONAL:
{resumo}
=================================================="""
        return Response(
            conteudo,
            mimetype="text/plain",
            headers={"Content-disposition": f"attachment; filename=curriculo_{nome.replace(' ', '_')}.txt"}
        )

@app.route('/minhas-candidaturas')
def minhas_candidaturas():
    ultimo_usuario = Usuario.query.order_by(Usuario.id.desc()).first()
    candidaturas = ultimo_usuario.candidaturas if ultimo_usuario else []
    return render_template_string(HTML_TEMPLATE, pagina='candidaturas', candidaturas=candidaturas)

@app.route('/cadastrar-empresa')
def cadastrar_empresa():
    return render_template_string(HTML_TEMPLATE, pagina='empresa')

@app.route('/salvar-empresa', methods=['POST'])
def salvar_empresa():
    nome = request.form.get('nome')
    area = request.form.get('area')
    site = request.form.get('site')

    nova_empresa = Empresa(nome=nome, area=area, site=site)
    db.session.add(nova_empresa)
    db.session.commit()

    return redirect(url_for('sobre'))

@app.route('/sobre')
def sobre():
    empresas = Empresa.query.all()
    return render_template_string(HTML_TEMPLATE, pagina='sobre', empresas=empresas)

# ==========================================
# EXECUÇÃO DIRETA NO VS CODE
# ==========================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)