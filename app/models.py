import requests
import pandas as pd
import jsonify

def fetch_pokemon_data(generation):
    """
    Fetches Pokémon data for a given generation and returns it as a DataFrame.

    """
    ...
    base_url = 'https://pokeapi.co/api/v2/'
    pokemon_data = []
    if generation < 1 or generation > 8:
            return jsonify({'error': 'Invalid generation number'}), 400
    else:
        generation_data = fetch_generation_data(base_url, generation)
        for pokemon in generation_data:
            pokemon_details = fetch_pokemon_details(pokemon['url'])
            new_row = extract_pokemon_info(pokemon_details, generation)
            pokemon_data.append(new_row)

        df = pd.DataFrame(pokemon_data)
        return df

#指定した世代のポケモンデータを取得
def fetch_generation_data(base_url, generation):
    try:
        response = requests.get(f'{base_url}generation/{generation}')
        response.raise_for_status()
        data = response.json()
        return data['pokemon_species']
    except requests.RequestException as e:
        print(f"Error fetching generation data: {e}")
        return []


#データをJSON化
def fetch_pokemon_details(pokemon_url):
    response = requests.get(pokemon_url)
    return response.json()


#日本語、韓国語ポケモン名を取得
def get_name_in_language(pokemon_details, lang):
    for name_entry in pokemon_details['names']:
        if name_entry['language']['name'] == lang:
            return name_entry['name']
    return None

#Dataframeのスキマ作成
def extract_pokemon_info(pokemon_details, generation):
    return {
        'generation': generation,
        'pokemon_id': pokemon_details['id'],
        'name_en': pokemon_details['name'],
        'name_ja': get_name_in_language(pokemon_details, 'ja'),
        'name_ko': get_name_in_language(pokemon_details, 'ko'),
        'capture_rate': pokemon_details.get('capture_rate'),
        'base_happiness': pokemon_details.get('base_happiness'),
        'is_baby': pokemon_details.get('is_baby', False),
        'is_legendary': pokemon_details.get('is_legendary', False),
        'is_mythical': pokemon_details.get('is_mythical', False),
    }

