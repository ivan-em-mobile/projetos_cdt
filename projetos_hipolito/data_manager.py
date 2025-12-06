import sqlite3
import json
import requests
import time 
import os 

DB_NAME = 'pokemons.db'
NUM_GERACOES_PARA_CACHE = 9 

def inicializar_db():
    """Cria as quatro tabelas necessárias (pokemons, moves_list, tipos_efetividades, abilities_list) se não existirem."""
    print("-> [DB] Inicializando/Verificando estrutura do banco de dados...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Tabela de Pokémons
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pokemons (
            id INTEGER PRIMARY KEY,
            nome TEXT UNIQUE NOT NULL,
            tipos TEXT,
            stats_base TEXT,
            hp_atual INTEGER,
            sprite_url TEXT,
            geracao INTEGER,
            descricao TEXT,
            moves_aprendiveis TEXT  
        )
    """)
    
    # 2. Tabela de Movimentos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moves_list (
            nome TEXT PRIMARY KEY,
            tipo TEXT,
            categoria TEXT, 
            power INTEGER, 
            accuracy INTEGER,
            chance_efeito INTEGER, 
            descricao_efeito TEXT 
        )
    """)
    
    # 3. Tabela de Efetividades entre Tipos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tipos_efetividades (
            tipo_atacante TEXT,
            tipo_defensor TEXT,
            multiplicador REAL, 
            PRIMARY KEY (tipo_atacante, tipo_defensor)
        )
    """)
    
    # 4. Tabela de Habilidades (Abilities)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS abilities_list (
            id INTEGER PRIMARY KEY,
            nome TEXT UNIQUE NOT NULL,
            efeito TEXT,  
            curta_descricao TEXT, 
            geracao TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print("-> [DB] Estrutura verificada com sucesso.")


def checar_e_atualizar_tipos_e_moves_e_abilities():
    """Busca e salva a matriz de efetividades, a lista de moves (ataques) e as abilities."""
    inicializar_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("\n[TIPOS] Buscando tipos e efetividades...")
    
    try:
        tipos_response = requests.get("https://pokeapi.co/api/v2/type?limit=100")
        tipos_response.raise_for_status() 
        tipos_data = tipos_response.json().get('results', [])
        
        regras_salvas = 0
        for tipo in tipos_data:
            nome_atacante = tipo['name']
            tipo_response = requests.get(tipo['url'])
            tipo_response.raise_for_status()
            dados_tipo = tipo_response.json()
            
            for dano_tipo, multiplicador in [('double_damage_to', 2.0), ('half_damage_to', 0.5), ('no_damage_to', 0.0)]:
                for defensor in dados_tipo['damage_relations'].get(dano_tipo, []):
                    cursor.execute("""
                        INSERT OR IGNORE INTO tipos_efetividades (tipo_atacante, tipo_defensor, multiplicador)
                        VALUES (?, ?, ?)
                    """, (nome_atacante, defensor['name'], multiplicador))
                    if cursor.rowcount > 0:
                        print(f"   -> [INSERIDO REGRA] {nome_atacante.capitalize()} -> {defensor['name'].capitalize()} (x{multiplicador})")
                        regras_salvas += 1
                        

            if regras_salvas > 0:
                conn.commit()
                regras_salvas = 0 
                
    except requests.exceptions.RequestException as e:
        print(f"❌ [TIPOS] Erro ao buscar lista de tipos ou detalhes: {e}")
        
    print("✅ [TIPOS] Tipos e efetividades salvas.")
    print("\n[MOVES] Buscando moves (ataques) relevantes e seus efeitos...")
    url_moves = "https://pokeapi.co/api/v2/move?limit=1000"
    
    try:
        moves_response = requests.get(url_moves)
        moves_response.raise_for_status()
        moves_data = moves_response.json().get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"❌ [MOVES] Erro ao buscar lista inicial de moves: {e}")
        conn.close()
        return

    moves_salvos = 0
    for move_info in moves_data:
        nome_move = move_info['name']
        
        try:
            move_response = requests.get(move_info['url'])
            move_response.raise_for_status()
            dados_move = move_response.json()
            
            power = dados_move.get('power', 0)
            categoria = dados_move.get('meta', {}).get('category', {}).get('name')
            chance_efeito = dados_move.get('effect_chance')
            
            descricao_efeito = "Nenhum efeito secundário salvo."
            for entry in dados_move.get('effect_entries', []):
                if entry['language']['name'] == 'en':
                    descricao_efeito = entry['effect'].replace('\n', ' ').replace('\u00ad', '')
                    break
            
            if power or categoria in ['heal', 'stat-changes', 'status']:
                cursor.execute("""
                    INSERT OR IGNORE INTO moves_list (nome, tipo, categoria, power, accuracy, chance_efeito, descricao_efeito)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (nome_move, dados_move['type']['name'], categoria, power, dados_move.get('accuracy', 0), chance_efeito, descricao_efeito))
                
                if cursor.rowcount > 0:
                     print(f"   -> [INSERIDO MOVE] {nome_move.capitalize()} | Power: {power} | Categoria: {categoria.capitalize()}")
                     moves_salvos += 1
            if moves_salvos % 20 == 0 and moves_salvos > 0:
                conn.commit()
                print(f"   -> [COMMIT] {moves_salvos} moves salvos no disco.")

        except (requests.exceptions.RequestException, AttributeError, json.JSONDecodeError) as e:
            print(f"⚠️ Erro crítico ao processar o move {nome_move}: {e}. Pulando.")
            time.sleep(0.5) 
            continue
            
    print(f"✅ [MOVES] Lista de moves (com efeitos) salva. Total de moves inseridos: {moves_salvos}.")
    conn.commit() 

    print("\n[ABILITIES] Buscando habilidades e seus efeitos...")
    url_abilities = "https://pokeapi.co/api/v2/ability?limit=400"
    
    try:
        abilities_response = requests.get(url_abilities)
        abilities_response.raise_for_status()
        abilities_data = abilities_response.json().get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"❌ [ABILITIES] Erro ao buscar lista de abilities: {e}")
        conn.close()
        return

    abilities_salvas = 0
    for ability_info in abilities_data:
        nome_ability = ability_info['name']
        
        try:
            ability_response = requests.get(ability_info['url'])
            ability_response.raise_for_status()
            dados_ability = ability_response.json()
            
            efeito = "Descrição não encontrada." 
            curta_descricao = "Nenhuma."
            efeito_en = None
            curta_descricao_en = None
            
            for entry in dados_ability.get('effect_entries', []):
                if entry['language']['name'] == 'pt':
                    efeito = entry['effect'].replace('\n', ' ').replace('\u00ad', '')
                    curta_descricao = entry['short_effect'].replace('\n', ' ').replace('\u00ad', '')
                    break 
                elif entry['language']['name'] == 'en':
                    efeito_en = entry['effect'].replace('\n', ' ').replace('\u00ad', '')
                    curta_descricao_en = entry['short_effect'].replace('\n', ' ').replace('\u00ad', '')

            if efeito == "Descrição não encontrada." and efeito_en is not None:
                efeito = efeito_en
                curta_descricao = curta_descricao_en
            
            geracao = dados_ability.get('generation', {}).get('name', 'N/A')
            
            cursor.execute("""
                INSERT OR IGNORE INTO abilities_list (id, nome, efeito, curta_descricao, geracao)
                VALUES (?, ?, ?, ?, ?)
            """, (dados_ability['id'], nome_ability, efeito, curta_descricao, geracao))
            
            
            if cursor.rowcount == 0: 
                 cursor.execute("""
                    UPDATE abilities_list
                    SET 
                        efeito = ?, 
                        curta_descricao = ?, 
                        geracao = ?
                    WHERE nome = ? 
                        AND (efeito = 'Descrição não encontrada.' OR efeito IS NULL)
                 """, (efeito, curta_descricao, geracao, nome_ability))


            if cursor.rowcount > 0:
                 print(f"   -> [INSERIDA/ATUALIZADA ABILITY] {nome_ability.capitalize()}")
                 abilities_salvas += 1
            
            if abilities_salvas % 20 == 0 and abilities_salvas > 0:
                conn.commit()
                print(f"   -> [COMMIT] {abilities_salvas} abilities salvas no disco.")

        except (requests.exceptions.RequestException, AttributeError, json.JSONDecodeError) as e:
            print(f"⚠️ Erro crítico ao processar a ability {nome_ability}: {e}. Pulando.")
            time.sleep(0.5)
            continue

    print("✅ [ABILITIES] Lista de habilidades salva.")

    conn.commit() 
    conn.close()

def checar_e_atualizar_cache():
    """Busca e salva todos os Pokémons por Geração (com descrição em PT e moves aprendíveis)."""
    inicializar_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    for gen_id in range(1, NUM_GERACOES_PARA_CACHE + 1):
        url_gen = f"https://pokeapi.co/api/v2/generation/{gen_id}"
        print(f"\n[CACHE] Buscando dados da Geração {gen_id}...")
        
        try:
            response = requests.get(url_gen)
            response.raise_for_status()
            dados_gen = response.json()
            
            total_gen = len(dados_gen['pokemon_species'])
            
            for i, especie in enumerate(dados_gen['pokemon_species']):
                nome_pokemon = especie['name']
                cursor.execute("SELECT id FROM pokemons WHERE nome = ?", (nome_pokemon,))
                if cursor.fetchone() is not None:
                    if (i + 1) % 100 == 0: 
                        print(f"   -> [PULANDO] {nome_pokemon.capitalize()}. Já existe no DB. Item {i+1}/{total_gen}.")
                    continue 
                
                try:
                    dados_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nome_pokemon}")
                    dados_response.raise_for_status()
                    dados = dados_response.json()

                    species_response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{nome_pokemon}")
                    species_response.raise_for_status()
                    dados_species = species_response.json()
                    
                    descricao_encontrada = ""
                    for entry in dados_species.get('flavor_text_entries', []):
                        if entry['language']['name'] == 'pt':
                            descricao_encontrada = entry['flavor_text'].replace('\n', ' ').replace('\u00ad', '')
                            break
                    
                    if dados and 'stats' in dados:
                        
                        moves_list_nomes = [m['move']['name'] for m in dados.get('moves', [])]
                        moves_json = json.dumps(moves_list_nomes)
                        tipos_json = json.dumps([t['type']['name'] for t in dados['types']])
                        stats_base = {stat['stat']['name']: stat['base_stat'] for stat in dados['stats']}
                        stats_json = json.dumps(stats_base)
                        
                        cursor.execute("""
                            INSERT OR IGNORE INTO pokemons (id, nome, tipos, stats_base, hp_atual, sprite_url, geracao, descricao, moves_aprendiveis)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (dados['id'], dados['name'].capitalize(), tipos_json, stats_json, stats_base.get('hp'), dados['sprites']['front_default'], gen_id, descricao_encontrada, moves_json))
                        
                        if cursor.rowcount > 0:
                            print(f"   -> [INSERIDO POKÉMON] {nome_pokemon.capitalize()} da Geração {gen_id}. Moves: {len(moves_list_nomes)}")

                        if (i + 1) % 50 == 0:
                            conn.commit()
                            print(f"  {i+1}/{total_gen} Pokémon da Geração {gen_id} processados. Commit salvo.")
                    
                    time.sleep(0.05) 
                    
                except requests.exceptions.RequestException as e:
                    print(f"⚠️ Erro de rede/JSON para {nome_pokemon}: {e}. Pulando e tentando continuar.")
                    time.sleep(1) 
                    continue

            conn.commit()
            print(f"✅ Geração {gen_id} processada. Total de Pokémon nessa Geração: {total_gen}.")

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro crítico ao buscar a LISTA da Geração {gen_id}: {e}. Tentando continuar da próxima Geração após 5 segundos...")
            time.sleep(5)
            continue

    conn.close()

def carregar_todos_pokemons():  
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT nome, tipos, stats_base, hp_atual, sprite_url, geracao, descricao FROM pokemons ORDER BY id ASC")
    
    pokemons = []
    for nome, tipos_json, stats_json, hp, sprite, gen, desc in cursor.fetchall():
        pokemons.append({
            "nome": nome,
            "tipos": json.loads(tipos_json),
            "stats": json.loads(stats_json),
            "hp_atual": hp,
            "sprite_url": sprite,
            "geracao": gen,
            "descricao": desc 
        })
    conn.close()
    return pokemons

if __name__ == "__main__":
    print("Iniciando o cache de dados (MODO DEBUG COM LOGS COMPLETOS)....")
    try:
        inicializar_db() 
        
        checar_e_atualizar_tipos_e_moves_e_abilities()
        
        checar_e_atualizar_cache()
        
        total = len(carregar_todos_pokemons())
        print(f"\n✨ CACHE FINALIZADO! Total de Pokémon no DB: {total}")
        
    except Exception as e:
        print(f"Ocorreu um erro crítico no final do processo: {e}")