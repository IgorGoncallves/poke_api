"""
Executa as rotinas de coleta em sequência:
1- Lista de Pokémons
2- Atributos detalhados
3- Histórico de combates
"""

import time
from etl.extracao.extrct_auth_save import get_token
from etl.extracao.extracao_pokemon import extract_pokemons
from etl.extracao.extracao_pokemon_atributos import extract_pokemon_attributes
from etl.extracao.extracao_pokemon_batalhas_batch import extract_battles_history_batch


def run_all_extractions():
    print(" Iniciando pipeline de extrações Pokémon Kaizen...\n")
    start_global = time.time()

    token = get_token()
    print(" Token JWT obtido com sucesso.\n")

    try:
        print(" Etapa 1 — Extraindo lista de Pokémons...")
        pokemons = extract_pokemons(token, per_page=50, max_pages=17)
        print(f" Lista extraída ({len(pokemons)} pokémons).\n")
    except Exception as e:
        print(f" Falha na extração de lista de Pokémons: {e}\n")

    try:
        print(" Etapa 2 — Extraindo atributos detalhados...")
        attributes = extract_pokemon_attributes(token, total_pokemons=799, resume=True)
        print(f" Atributos extraídos ({len(attributes)} registros).\n")
    except Exception as e:
        print(f" Falha na extração de atributos: {e}\n")

    try:
        print(" Etapa 3 — Extraindo histórico de combates...")
        battles = extract_battles_history_batch(
            token,
            per_page=100,
            batch_size=30,
            max_workers=6,
            resume=True
        )
        print(f" Combates extraídos ({len(battles)} registros).\n")
    except Exception as e:
        print(f" Falha na extração de combates: {e}\n")

    end_global = time.time()
    print(f" Pipeline concluído em {(end_global - start_global):.2f} segundos.")
    print(" Dados brutos salvos na pasta data/raw/.\n")

if __name__ == "__main__":
    run_all_extractions()
