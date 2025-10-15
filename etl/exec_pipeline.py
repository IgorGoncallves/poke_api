"""
Executa as rotinas de coleta em sequência:
1- Lista de Pokémons
2- Atributos detalhados
3- Histórico de combates
4- Carga para Stage
5- Transformação Dbt Stage to Dw
"""

import time
import subprocess
import os
from etl.extracao.extrct_auth_save import get_token
from etl.extracao.extracao_pokemon import extract_pokemons
from etl.extracao.extracao_pokemon_atributos import extract_pokemon_attributes
from etl.extracao.extracao_pokemon_batalhas_batch import extract_battles_history_batch
from etl.carga.carga_json_stage import carregar_batalhas, carregar_pokemons


def run_all_extractions():
    print(" Iniciando pipeline de extrações Pokémon Kaizen...\n")
    start_global = time.time()

    token = get_token()
    print(" Token JWT obtido com sucesso.\n")

    #########################ETAPA POKEMONS#####################################
    try:
        print(" Etapa 1 — Extraindo lista de Pokémons...")
        pokemons = extract_pokemons(token, per_page=50, max_pages=17)
        print(f" Lista extraída ({len(pokemons)} pokémons).\n")
    except Exception as e:
        print(f" Falha na extração de lista de Pokémons: {e}\n")

    #########################ETAPA ATRIBUTOS#####################################
    try:
        print(" Etapa 2 — Extraindo atributos detalhados...")
        attributes = extract_pokemon_attributes(token, total_pokemons=799, resume=True)
        print(f" Atributos extraídos ({len(attributes)} registros).\n")
    except Exception as e:
        print(f" Falha na extração de atributos: {e}\n")


    #########################ETAPA BATALHAS######################################
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

    
    print(" Dados brutos salvos na pasta data/raw/.\n")

    #########################ETAPA STAGE#########################################

    try:
        print(" Etapa 4 — Carga para camada STAGE...\n")
        start_stage = time.time()
        carregar_pokemons()
        carregar_batalhas()
        end_stage = time.time()
        print(f" Carga STAGE concluída em {(end_stage - start_stage):.2f} segundos.\n")
    except Exception as e:
        print(f" Erro ao carregar dados para STAGE: {e}\n")

    #########################ETAPA DBT###########################################
    try:
        print(" Etapa 5 — Executando transformação DBT...\n")
        dbt_project_path = os.path.abspath("etl/dbt_poke/dbt_poke")


        process = subprocess.Popen(
            ["dbt", "run", "--full-refresh", "--project-dir", dbt_project_path],
            stdout=None,     
            stderr=None,     
            shell=True
        )

        process.wait()  

        if process.returncode == 0:
            print(" DBT executado com sucesso! Modelos DW atualizados.\n")
        else:
            print(f" DBT terminou com erro. Código: {process.returncode}\n")

    except Exception as e:
        print(f" Falha ao executar o DBT: {e}\n")

    end_global = time.time()
    print(f" Pipeline concluído em {(end_global - start_global):.2f} segundos.")

if __name__ == "__main__":
    run_all_extractions()
    