import os
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

if os.environ.get('RENDER'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/igreja_catolica.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///igreja_catolica.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False) 

class Conteudo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, nullable=False) 
    opcao_id = db.Column(db.Integer, nullable=False)     
    titulo = db.Column(db.String(150), nullable=False)
    texto = db.Column(db.Text, nullable=False)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    dados = request.get_json()
    nome_usuario = dados.get('usuario')
    senha_pura = dados.get('senha')

    if not nome_usuario or not senha_pura:
        return jsonify({"erro": "Usuário e senha são obrigatórios"}), 400

    usuario_existente = Usuario.query.filter_by(usuario=nome_usuario).first()
    if usuario_existente:
        return jsonify({"erro": "Este nome de usuário já está em uso"}), 400

    senha_criptografada = generate_password_hash(senha_pura)
    
    novo_usuario = Usuario(usuario=nome_usuario, senha=senha_criptografada)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201


@app.route('/api/login', methods=['POST'])
def login():
    dados = request.get_json()
    nome_usuario = dados.get('usuario')
    senha_pura = dados.get('senha')

    usuario_banco = Usuario.query.filter_by(usuario=nome_usuario).first()

    if usuario_banco and check_password_hash(usuario_banco.senha, senha_pura):
        return jsonify({
            "mensagem": "Login realizado com sucesso!",
            "usuario": usuario_banco.usuario
        }), 200

    return jsonify({"erro": "Usuário ou senha incorretos"}), 401


@app.route('/api/conteudo/<int:cat_id>/<int:op_id>', methods=['GET'])
def obter_conteudo(cat_id, op_id):
    resultado = Conteudo.query.filter_by(categoria_id=cat_id, opcao_id=op_id).first()
    
    if resultado:
        return jsonify({
            "titulo": resultado.titulo,
            "texto": resultado.texto
        })
    
    return jsonify({"erro": "Conteúdo não encontrado no banco de dados."}), 404


if __name__ == '__main__':
    app.run(debug=True)