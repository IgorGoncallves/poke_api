from etl.extracao.extrct_auth_save import get_token, auth_header, save_raw
from configuracoes.variaveis_env import api_url
import requests
import pandas as pd
import time

def extract_pokemons(token, per_page=50, max_pages=17):
    all_pokemons = []
    for page in range(1, max_pages + 1):
        res = requests.get(
            f"{api_url}/pokemon",
            headers=auth_header(token),
            params={"page": page, "per_page": per_page}
        )

        if res.status_code == 429:
            print(" Limite atingido, esperando 10 segundos antes de continuar")
            time.sleep(10)
            page -= 1
            continue

        if res.status_code == 404:
            print(f" Página {page} não encontrada.")
            break

        res.raise_for_status()
        response = res.json()
        pokemons_page = response.get("pokemons", [])
        total = response.get("total")

        if not pokemons_page:
            break

        all_pokemons.extend(pokemons_page)
        print(f" Página {page} extraída ({len(pokemons_page)} registros)")
        time.sleep(0.5)
    save_raw(all_pokemons, "pokemon_list")
    print(f" Total final extraído: {len(all_pokemons)} registros")
    return all_pokemons

if __name__ == "__main__":
    start = time.time()
    token = get_token()
    all_pokemons = extract_pokemons(token, per_page=50, max_pages=17)
    save_raw(all_pokemons, "pokemon_list")
    print(pd.DataFrame(all_pokemons).head())
    end = time.time()
    print(f"\n Tempo total de execução: {end - start:.2f} segundos")
