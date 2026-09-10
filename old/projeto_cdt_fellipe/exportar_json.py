import json
from app import app, db, Conteudo

with app.app_context():
    todos_os_conteudos = Conteudo.query.all()
    
    lista_para_json = []
    
    for item in todos_os_conteudos:
        dados_item = {
            "id": item.id,
            "categoria_id": item.categoria_id,
            "ordem": item.id,
            "titulo": item.titulo,
            "texto": item.texto
        }
        lista_para_json.append(dados_item)
    
    with open('dados_igreja.json', 'w', encoding='utf-8') as arquivo:
        json.dump(lista_para_json, arquivo, ensure_ascii=False, indent=4)

print("✨ Sucesso! Os dados foram exportados para o arquivo 'dados_igreja.json'.")