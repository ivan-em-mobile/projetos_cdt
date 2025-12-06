import requests

def buscar_dados_pokemon(nome_pokemon):
    nome_pokemon = nome_pokemon.lower()
    url_base = f"https://pokeapi.co/api/v2/pokemon/{nome_pokemon}"
    
    try:
        response = requests.get(url_base)
        response.raise_for_status() 
        dados = response.json()
        
        stats_base = {stat['stat']['name']: stat['base_stat'] for stat in dados['stats']}
        tipos = [t['type']['name'] for t in dados['types']]
        
        resultado = {
            "nome": dados['name'].capitalize(),
            "tipos": tipos,
            "stats": stats_base,
            "hp_atual": stats_base.get('hp'),
            "sprite_url": dados['sprites']['front_default']
        }
        
        return resultado

    except requests.exceptions.HTTPError:
        return None
    except requests.exceptions.RequestException:
        return None

def buscar_efetividade(tipo_ataque, tipos_defesa):
    url_base = f"https://pokeapi.co/api/v2/type/{tipo_ataque.lower()}"
    
    try:
        response = requests.get(url_base)
        response.raise_for_status()
        dados_tipo = response.json()
        
        multiplicador = 1.0

        dobro_dano = [t['name'] for t in dados_tipo['damage_relations']['double_damage_to']]
        metade_dano = [t['name'] for t in dados_tipo['damage_relations']['half_damage_to']]
        sem_dano = [t['name'] for t in dados_tipo['damage_relations']['no_damage_to']]

        for tipo_defesa in tipos_defesa:
            if tipo_defesa in sem_dano:
                return 0.0
            if tipo_defesa in dobro_dano:
                multiplicador *= 2.0
            elif tipo_defesa in metade_dano:
                multiplicador *= 0.5

        return multiplicador

    except requests.exceptions.RequestException:
        return 1.0