#日本語、韓国語ポケモン名を取得
def get_name_in_language(pokemon_details, lang):
    for name_entry in pokemon_details['names']:
        if name_entry['language']['name'] == lang:
            return name_entry['name']
    return None

#Dataframeスキマ
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

