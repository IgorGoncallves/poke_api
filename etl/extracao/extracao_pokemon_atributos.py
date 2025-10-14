import requests
import pandas as pd
import time
import json
from pathlib import Path
from etl.extracao.extrct_auth_save import get_token, auth_header, save_raw
from configuracoes.variaveis_env import api_url


def get_pokemon_details(token, pokemon_id):
    headers = auth_header(token)
    url = f"{api_url}/pokemon/{pokemon_id}"

    for attempt in range(2):
        res = requests.get(url, headers=headers)

        if res.status_code == 429:
            print(f"Rate-limit atingido no Pokémon {pokemon_id}. Aguardando 10s...")
            time.sleep(10)
            continue

        if res.status_code == 404:
            print(f"Pokémon ID {pokemon_id} não encontrado.")
            return None

        try:
            res.raise_for_status()
        except Exception as e:
            print(f"Erro ao buscar Pokémon {pokemon_id}: {e}")
            time.sleep(2)
            continue

        return res.json()

    print(f"Falha definitiva ao buscar Pokémon {pokemon_id} após 2 tentativas.")
    return None


def extract_pokemon_attributes(token, total_pokemons=799, resume=False):
    output_path = Path("data/raw/pokemon_attributes.json")
    pokemons_details = []

    if resume and output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            pokemons_details = json.load(f)
        print(f"Retomando extração a partir do ID {len(pokemons_details)+1}")

    start_id = len(pokemons_details) + 1

    for pid in range(start_id, total_pokemons + 1):
        data = get_pokemon_details(token, pid)
        if data:
            pokemons_details.append(data)
            print(f"Pokémon {pid}/{total_pokemons} — {data.get('name')}")

        if pid % 100 == 0:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(pokemons_details, f, ensure_ascii=False, indent=2)
            print(f"Progresso salvo até o Pokémon {pid}")

    save_raw(pokemons_details, "pokemon_attributes")
    print(f"Extração finalizada. Total: {len(pokemons_details)} Pokémons detalhados.")
    return pokemons_details


if __name__ == "__main__":
    start = time.time()
    token = get_token()
    pokemons_details = extract_pokemon_attributes(token, total_pokemons=799, resume=True)
    df = pd.DataFrame(pokemons_details)
    print("\n Prévia dos dados detalhados:")
    print(df.head())
    end = time.time()
    print(f"\n Tempo total de execução: {end - start:.2f} segundos")
