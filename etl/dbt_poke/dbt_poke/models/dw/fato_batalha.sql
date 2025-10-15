{{ config(materialized='incremental', unique_key='id_batalha') }}

SELECT
    ROW_NUMBER() OVER () AS id_batalha,
    b.first_pokemon AS id_pokemon_1,
    b.second_pokemon AS id_pokemon_2,
    b.winner AS id_vencedor
FROM {{ ref('stg_batalha') }} b
JOIN {{ ref('dim_pokemon') }} p1 ON b.first_pokemon = p1.id_pokemon
JOIN {{ ref('dim_pokemon') }} p2 ON b.second_pokemon = p2.id_pokemon
JOIN {{ ref('dim_pokemon') }} p3 ON b.winner = p3.id_pokemon
WHERE b.first_pokemon IS NOT NULL
  AND b.second_pokemon IS NOT NULL
  AND b.winner IS NOT NULL
