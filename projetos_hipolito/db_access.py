import sqlite3
import json

DB_NAME = "pokemons.db"

def _get_db_connection():
    """Função interna para conectar e retornar a conexão com o DB."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn

# --- FUNÇÕES DE BUSCA BÁSICA ---

def get_all_pokemon_names():
    """Retorna uma lista de todos os nomes de Pokémon para o Autocomplete."""
    conn = _get_db_connection()
    cursor = conn.cursor()
    
    # Selecionamos o nome e ordenamos para que o autocomplete seja mais intuitivo
    cursor.execute("SELECT nome FROM pokemons ORDER BY nome")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names

def get_pokemon_data(nome: str):
    """
    Retorna todos os dados essenciais de um Pokémon (Tipos, Stats, Descrição).
    Retorna None se o Pokémon não for encontrado.
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    
    # Busca o Pokémon pelo nome (case-insensitive)
    cursor.execute("SELECT * FROM pokemons WHERE nome LIKE ?", (nome.capitalize(),))
    pokemon_row = cursor.fetchone()
    conn.close()
    
    if pokemon_row is None:
        return None
        
    # Converte os campos JSON para dicionários/listas Python
    pokemon_data = dict(pokemon_row)
    pokemon_data['tipos'] = json.loads(pokemon_data['tipos'])
    pokemon_data['stats_base'] = json.loads(pokemon_data['stats_base'])
    pokemon_data['moves_aprendiveis'] = json.loads(pokemon_data['moves_aprendiveis'])
    
    return pokemon_data

# --- FUNÇÕES DE LÓGICA DE BATALHA ---

def get_effectiveness(tipo_atacante: str, tipo_defensor: str) -> float:
    """
    Retorna o multiplicador de dano (x2.0, x0.5, x0.0) entre dois tipos.
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT multiplicador 
        FROM tipos_efetividades 
        WHERE tipo_atacante = ? AND tipo_defensor = ?
    """, (tipo_atacante, tipo_defensor))
    
    result = cursor.fetchone()
    conn.close()
    
    # Se não houver regra específica, o multiplicador é 1.0 (dano normal)
    if result:
        return result[0]
    else:
        return 1.0
        
def calculate_damage_multiplier(ataque_tipos: list, defesa_tipos: list) -> float:
    """
    Calcula o multiplicador total de dano (Ex: Gelo vs Gelo/Voador = x0.5 * x2.0 = x1.0).
    """
    if not ataque_tipos or not defesa_tipos:
        return 1.0 # Garante que não quebre se algum tipo estiver faltando
        
    multiplicador_total = 1.0
    
    # Para cada tipo de ataque
    for tipo_ataque in ataque_tipos:
        # Verifica a efetividade contra CADA tipo de defesa do Pokémon
        for tipo_defesa in defesa_tipos:
            multiplicador = get_effectiveness(tipo_ataque.lower(), tipo_defesa.lower())
            multiplicador_total *= multiplicador
            
    return multiplicador_total


def get_random_pokemon_data():
    """Retorna dados de um Pokémon aleatório do DB."""
    conn = _get_db_connection()
    cursor = conn.cursor()
    
    # Seleciona um Pokémon aleatório com base no ID
    cursor.execute("SELECT * FROM pokemons ORDER BY RANDOM() LIMIT 1")
    pokemon_row = cursor.fetchone()
    conn.close()
    
    if pokemon_row is None:
        return None
        
    # Reutiliza a lógica de conversão de JSON
    pokemon_data = dict(pokemon_row)
    pokemon_data['tipos'] = json.loads(pokemon_data['tipos'])
    pokemon_data['stats_base'] = json.loads(pokemon_data['stats_base'])
    pokemon_data['moves_aprendiveis'] = json.loads(pokemon_data['moves_aprendiveis'])
    
    return pokemon_data

# --- Exemplo de Teste ---
if __name__ == '__main__':
    # Teste 1: Autocomplete
    print("--- Teste de Nomes ---")
    nomes = get_all_pokemon_names()
    print(f"Total de nomes encontrados: {len(nomes)}")
    print(f"Alguns nomes: {nomes[:5]}")
    
    # Teste 2: Dados de um Pokémon
    print("\n--- Teste de Pokémon (Pikachu) ---")
    pikachu_data = get_pokemon_data("Pikachu")
    if pikachu_data:
        print(f"Nome: {pikachu_data['nome']}")
        print(f"Tipos: {pikachu_data['tipos']}")
        print(f"HP Base: {pikachu_data['stats_base'].get('hp')}")
    
    # Teste 3: Cálculo de Efetividade (Fogo vs Planta/Voar)
    print("\n--- Teste de Efetividade (Fogo vs Bulbasaur) ---")
    # Bulbasaur é Tipo: ['grass', 'poison']
    tipos_defesa_bulbasaur = ['grass', 'poison'] 
    
    # Fogo vs Planta (x0.5)
    fogo_vs_planta = get_effectiveness('fire', 'grass')
    
    # Fogo vs Veneno (x1.0, se não houver regra na tabela)
    fogo_vs_veneno = get_effectiveness('fire', 'poison')
    
    print(f"Fogo vs Planta: x{fogo_vs_planta}")
    print(f"Fogo vs Veneno: x{fogo_vs_veneno}")
    
    # Multiplicador total (Fogo vs Bulbasaur)
    total_mult = calculate_damage_multiplier(['fire'], tipos_defesa_bulbasaur)
    print(f"Multiplicador Total: x{total_mult} (Esperado: 0.5)")