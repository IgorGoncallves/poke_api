import json
from pathlib import Path
from configuracoes.conexao_db import get_connection
import time
from configuracoes.sprites import get_sprite_url  

def carregar_pokemons():
    caminho = Path("data/raw/pokemon_attributes.json")
    if not caminho.exists():
        print(" Arquivo pokemons.json não encontrado")
        return

    with open(caminho, "r", encoding="utf-8") as f:
        pokemons = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    for p in pokemons:
        sprite_url = get_sprite_url(p.get("name"))

        cur.execute("""
            INSERT INTO stage.stg_pokemon (
                id, name, hp, attack, defense,
                sp_attack, sp_defense, speed,
                generation, legendary, types, sprite_url
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (id) DO UPDATE SET
                sprite_url = EXCLUDED.sprite_url;
        """, (
            p.get("id"),
            p.get("name"),
            p.get("hp"),
            p.get("attack"),
            p.get("defense"),
            p.get("sp_attack"),
            p.get("sp_defense"),
            p.get("speed"),
            p.get("generation"),
            p.get("legendary"),
            p.get("types"),
            sprite_url
        ))

    conn.commit()
    cur.close()
    conn.close()
    print(" Dados de Pokémon carregados com sucesso para stage.stg_pokemon")


def carregar_batalhas():
    caminho = Path("data/raw/battles_history.json")
    if not caminho.exists():
        print(" Arquivo batalhas.json não encontrado")
        return
    
    with open(caminho, "r", encoding="utf-8") as f:
        batalhas = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    for b in batalhas:
        cur.execute("""
            INSERT INTO stage.stg_batalha (
                first_pokemon, second_pokemon, winner
            )
            VALUES (%s,%s,%s);
        """, (
            b.get("first_pokemon"),
            b.get("second_pokemon"),
            b.get("winner")
        ))
    
    conn.commit()
    cur.close()
    conn.close()
    print(" Dados de batalhas carregados com sucesso para stage.stg_batalha")


if __name__ == "__main__":
    
    print(" Iniciando carga para camada STAGE")
    start1 = time.time()
    carregar_pokemons()
    end1 = time.time()

    print(f"\n Carga pokemons em: {end1 - start1:.2f} segundos")

    start2 = time.time()
    carregar_batalhas()
    end2 = time.time()

    print(f"\n Carga batalhas em: {end2 - start2:.2f} segundos")

    print(f"\n Processo total finalizado em: {end2 - start1:.2f} segundos")


