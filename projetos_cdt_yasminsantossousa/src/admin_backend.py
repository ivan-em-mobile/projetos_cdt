import sqlite3
import json
import os

DB_NAME = 'acaiteria.db'

def obter_todos_pedidos():
    """Busca todos os pedidos registados na base de dados para o painel do administrador."""
    if not os.path.exists(DB_NAME):
        return []
    
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    pedidos = []
    
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pedidos';")
        if cursor.fetchone():
            cursor.execute("SELECT * FROM pedidos;")
            pedidos = cursor.fetchall()
    except Exception as e:
        print(f"[ERRO BD] Falha ao buscar pedidos: {e}")
    finally:
        conexao.close()
        
    return pedidos

def exportar_banco_para_json(caminho_destino="backup_acaiteria.json"):
    """Exporta todas as tabelas da base de dados SQLite para um ficheiro JSON."""
    if not os.path.exists(DB_NAME):
        return False, "Base de dados não encontrada."
        
    conexao = sqlite3.connect(DB_NAME)
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    
    dados_completos = {}
    
    try:
        # Obtém todas as tabelas do banco
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = cursor.fetchall()
        
        for tabela in tabelas:
            nome_tabela = tabela['name']
            cursor.execute(f"SELECT * FROM {nome_tabela};")
            linhas = cursor.fetchall()
            dados_completos[nome_tabela] = [dict(linha) for linha in linhas]
            
        with open(caminho_destino, 'w', encoding='utf-8') as f:
            json.dump(dados_completos, f, ensure_ascii=False, indent=4)
            
        return True, caminho_destino
    except Exception as e:
        return False, str(e)
    finally:
        conexao.close()