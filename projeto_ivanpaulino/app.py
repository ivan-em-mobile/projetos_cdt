from flask import Flask, render_template, request, jsonify, g
import sqlite3
import os

# Inicialização padrão do Flask (já que as pastas templates e static estão no mesmo nível)
app = Flask(__name__)

# --- AJUSTE INTELIGENTE DO BANCO DE DADOS ---
# Se o projeto estiver a rodar na Vercel, usa a pasta '/tmp'
if os.environ.get('VERCEL'):
    DATABASE = '/tmp/salao.db'
else:
    # Se estiver no teu PC local, cria o banco na mesma pasta raiz do app.py
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE = os.path.join(BASE_DIR, 'salao.db')
# --------------------------------------------

# Função para conectar ao Banco de Dados
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Inicializar o Banco de Dados com os dados do Salão
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # 1. Tabela de Clientes
        cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            telefone TEXT)''')
        
        # 2. Tabela de Funcionários
        cursor.execute('''CREATE TABLE IF NOT EXISTS funcionarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            cargo TEXT NOT NULL)''')
        
        # 3. Tabela de Serviços
        cursor.execute('''CREATE TABLE IF NOT EXISTS servicos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            preco REAL NOT NULL)''')
        
        # 4. Tabela de Produtos
        cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            preco REAL NOT NULL)''')
        
        # 5. Tabela de Agendamentos
        cursor.execute('''CREATE TABLE IF NOT EXISTS agendamentos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            cliente_id INTEGER,
                            funcionario_id INTEGER,
                            servico_id INTEGER,
                            dia_semana TEXT,
                            hora TEXT,
                            agendado_por TEXT,
                            FOREIGN KEY(cliente_id) REFERENCES clientes(id),
                            FOREIGN KEY(funcionario_id) REFERENCES funcionarios(id),
                            FOREIGN KEY(servico_id) REFERENCES servicos(id))''')

        # Evita duplicar os dados fixos ao reiniciar o servidor
        cursor.execute("SELECT COUNT(*) FROM funcionarios")
        if cursor.fetchone()[0] == 0:
            funcionarios_iniciais = [
                ('Andre', 'Cabeleireiro'),
                ('Andreia', 'Cabeleireira'),
                ('Antonio', 'Cabeleireiro'),
                ('Andressa', 'Podóloga'),
                ('Andrei', 'Recepcionista')
            ]
            cursor.executemany('INSERT INTO funcionarios (nome, cargo) VALUES (?, ?)', funcionarios_iniciais)

            servicos_iniciais = [('Corte', 25.0), ('Pintura', 40.0), ('Tratamento Químico', 60.0)]
            cursor.executemany('INSERT INTO servicos (nome, preco) VALUES (?, ?)', servicos_iniciais)

            produtos_iniciais = [('Shampoo', 15.0), ('Creme', 18.0), ('Máscara Capilar', 22.0)]
            cursor.executemany('INSERT INTO produtos (nome, preco) VALUES (?, ?)', produtos_iniciais)

        db.commit()

# --- ROTAS ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dados-iniciais', methods=['GET'])
def dados_iniciais():
    db = get_db()
    cursor = db.cursor()
    
    funcionarios = cursor.execute('SELECT * FROM funcionarios').fetchall()
    servicos = cursor.execute('SELECT * FROM servicos').fetchall()
    produtos = cursor.execute('SELECT * FROM produtos').fetchall()
    clientes = cursor.execute('SELECT * FROM clientes').fetchall()
    
    return jsonify({
        "funcionarios": [dict(f) for f in funcionarios],
        "servicos": [dict(s) for s in servicos],
        "produtos": [dict(p) for p in produtos],
        "clientes": [dict(c) for c in clientes]
    })

@app.route('/api/clientes', methods=['POST'])
def cadastrar_cliente():
    dados = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO clientes (nome, telefone) VALUES (?, ?)', (dados['nome'], dados['telefone']))
    db.commit()
    return jsonify({"status": "sucesso", "mensagem": "Cliente cadastrado com sucesso!"})

@app.route('/api/editar-preco', methods=['POST'])
def editar_preco():
    dados = request.json
    tabela = dados['tabela']
    item_id = dados['id']
    novo_preco = dados['preco']
    
    if tabela not in ['servicos', 'produtos']:
        return jsonify({"status": "erro", "mensagem": "Tabela inválida"}), 400
        
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f'UPDATE {tabela} SET preco = ? WHERE id = ?', (novo_preco, item_id))
    db.commit()
    return jsonify({"status": "sucesso", "mensagem": "Preço atualizado com sucesso!"})

@app.route('/api/agendamentos', methods=['POST'])
def criar_agendamento():
    dados = request.json
    dia = dados['dia_semana']
    agendado_por = dados['agendado_por']
    
    dias_permitidos = ['Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    if dia not in dias_permitidos:
        return jsonify({"status": "erro", "mensagem": "Agendamentos só são permitidos de Quarta a Domingo!"}), 400
        
    if agendado_por != "Recepcionista-Andrei":
        return jsonify({"status": "erro", "mensagem": "Apenas o Recepcionista-Andrei pode efetuar agendamentos!"}), 403

    db = get_db()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO agendamentos (cliente_id, funcionario_id, servico_id, dia_semana, hora, agendado_por) 
                      VALUES (?, ?, ?, ?, ?, ?)''', 
                   (dados['cliente_id'], dados['funcionario_id'], dados['servico_id'], dia, dados['hora'], agendado_por))
    db.commit()
    return jsonify({"status": "sucesso", "mensagem": "Agendamento realizado com sucesso!"})

@app.route('/api/exportar-json', methods=['GET'])
def exportar_json():
    db = get_db()
    cursor = db.cursor()
    
    clientes = [dict(row) for row in cursor.execute('SELECT * FROM clientes').fetchall()]
    funcionarios = [dict(row) for row in cursor.execute('SELECT * FROM funcionarios').fetchall()]
    servicos = [dict(row) for row in cursor.execute('SELECT * FROM servicos').fetchall()]
    produtos = [dict(row) for row in cursor.execute('SELECT * FROM produtos').fetchall()]
    agendamentos = [dict(row) for row in cursor.execute('SELECT * FROM agendamentos').fetchall()]
    
    banco_completo = {
        "clientes": clientes,
        "funcionarios": funcionarios,
        "servicos": servicos,
        "produtos": produtos,
        "agendamentos": agendamentos
    }
    
    return jsonify(banco_completo)

init_db()

if __name__ == '__main__':
    app.run(debug=True)