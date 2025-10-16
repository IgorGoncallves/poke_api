import requests
import pandas as pd
import time
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from etl.extracao.extrct_auth_save import get_token, auth_header, save_raw
from configuracoes.variaveis_env import api_url


def get_battles_page(token, page, per_page):
    headers = auth_header(token)
    params = {"page": page, "per_page": per_page}
    url = f"{api_url}/combats"

    for attempt in range(3):
        res = requests.get(url, headers=headers, params=params)

        if res.status_code == 429:
            print(f" Rate-limit na página {page}. Aguardando 10s...")
            time.sleep(10)
            continue

        try:
            res.raise_for_status()
        except Exception as e:
            print(f" Erro ao buscar página {page}: {e}")
            time.sleep(2)
            continue

        data = res.json()

        if isinstance(data, dict) and "combats" in data:
            registros = data["combats"]
            print(f" Página {page} - {len(registros)} batalhas")
            return registros

        return []

    print(f" Falha definitiva ao buscar página {page} após 3 tentativas.")
    return []


def extract_battles_history_batch(token, per_page=100, batch_size=30, max_workers=6, resume=False):
    output_path = Path("data/raw/battles_history.json")
    battles_history = []
    start_page = 1

    if resume and output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            battles_history = json.load(f)
        start_page = len(battles_history) // per_page + 1
        print(f" Retomando extração a partir da página {start_page}")

    headers = auth_header(token)
    params = {"page": 1, "per_page": per_page}
    url = f"{api_url}/combats"
    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()
    meta = res.json()
    total = meta.get("total", 0)
    total_pages = (total // per_page) + (1 if total % per_page else 0)

    print(f" Total de combates: {total:,} | Páginas: {total_pages}")
    print(f" Executando em batches de {batch_size} páginas com {max_workers} threads.\n")

    while start_page <= total_pages:
        end_page = min(start_page + batch_size - 1, total_pages)
        pages_to_fetch = list(range(start_page, end_page + 1))

        print(f" Coletando páginas {start_page}–{end_page}.")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(get_battles_page, token, page, per_page): page
                for page in pages_to_fetch
            }

            for future in as_completed(futures):
                page = futures[future]
                try:
                    result = future.result()
                    if result:
                        battles_history.extend(result)
                except Exception as e:
                    print(f" Erro na página {page}: {e}")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(battles_history, f, ensure_ascii=False, indent=2)
        print(f" Progresso salvo após batch {start_page}-{end_page} (Total: {len(battles_history)} batalhas)\n")

        start_page = end_page + 1
        time.sleep(1) 

    save_raw(battles_history, "battles_history")
    print(f"Extração finalizada. Total: {len(battles_history)} batalhas coletadas.")
    return battles_history


if __name__ == "__main__":
    start = time.time()
    token = get_token()

    battles = extract_battles_history_batch(
        token,
        per_page=100,   
        batch_size=30,  
        max_workers=6,  
        resume=True
    )

    df = pd.DataFrame(battles)
    print("\n Prévia dos combates detalhados:")
    print(df.head())
    end = time.time()
    print(f"\n Tempo total de execução: {end - start:.2f} segundos")
