from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

locais_disponiveis = {'meet', 'Presencial'}
ARQUIVO_DADOS = 'agenda.json'

def carregar_agenda():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_agenda():
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(agenda, f, ensure_ascii=False, indent=2)

agenda = carregar_agenda()

def proximo_id():
    if not agenda:
        return 1
    return max(r['id'] for r in agenda) + 1

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/agendar', methods=['POST'])
def agendar():
    dados = request.json
    reuniao = {
        "id": proximo_id(),
        "nome": dados['nome'],
        "telefone": dados['telefone'],
        "data": dados['data'],
        "horario": dados['horario'],
        "local": dados['local'],
        "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    if reuniao['local'] in locais_disponiveis:
        agenda.append(reuniao)
        salvar_agenda()
        return jsonify({"sucesso": True, "mensagem": f"Reunião agendada! ID: {reuniao['id']}"})
    else:
        return jsonify({"sucesso": False, "mensagem": "Local inválido!"})

@app.route('/listar', methods=['GET'])
def listar():
    agenda_ordenada = sorted(agenda, key=lambda x: (x['data'], x['horario']))
    return jsonify(agenda_ordenada)

@app.route('/buscar/<int:id>', methods=['GET'])
def buscar(id):
    for reuniao in agenda:
        if reuniao['id'] == id:
            return jsonify({"sucesso": True, "reuniao": reuniao})
    return jsonify({"sucesso": False, "mensagem": "Reunião não encontrada!"})

@app.route('/mudar/<int:id>', methods=['PUT'])
def mudar(id):
    dados = request.json
    for reuniao in agenda:
        if reuniao['id'] == id:
            reuniao['nome'] = dados.get('nome', reuniao['nome'])
            reuniao['telefone'] = dados.get('telefone', reuniao['telefone'])
            reuniao['data'] = dados.get('data', reuniao['data'])
            reuniao['horario'] = dados.get('horario', reuniao['horario'])
            reuniao['local'] = dados.get('local', reuniao['local'])
            salvar_agenda()
            return jsonify({"sucesso": True, "mensagem": f"Reunião {id} atualizada!"})
    return jsonify({"sucesso": False, "mensagem": "Reunião não encontrada!"})

@app.route('/cancelar/<int:id>', methods=['DELETE'])
def cancelar(id):
    global agenda
    for i, reuniao in enumerate(agenda):
        if reuniao['id'] == id:
            agenda.pop(i)
            salvar_agenda()
            return jsonify({"sucesso": True, "mensagem": f"Reunião {id} cancelada!"})
    return jsonify({"sucesso": False, "mensagem": "Reunião não encontrada!"})

if __name__ == "__main__":
    app.run(debug=True)