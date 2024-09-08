import jsonify
import requests
from models import extract_pokemon_info
from pandas import DataFrame


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

        df = DataFrame(pokemon_data)
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